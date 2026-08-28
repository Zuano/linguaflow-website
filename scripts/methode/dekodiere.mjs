#!/usr/bin/env node
// ============================================================
// dekodiere.mjs — generates the word-for-word decodings of the method page's
// example text for every language pair, using the EXACT prompts, schema and
// model choice of the app's production decode pipeline (functions/src/
// decodeText.ts in the app repo, ported verbatim 2026-08-28). Mode "input",
// romanization for non-Latin learning languages (4-line system).
//
// Erzeugt die Wort-für-Wort-Dekodierungen des Beispieltexts für alle
// Sprachpaare — mit den EXAKTEN Prompts, dem Schema und der Modellwahl der
// App-Dekodier-Pipeline (1:1 portiert am 2026-08-28).
//
// Usage:
//   node scripts/methode/dekodiere.mjs --pair de:en     (one pair)
//   node scripts/methode/dekodiere.mjs --target de      (one learning language)
//   node scripts/methode/dekodiere.mjs --all            (all 33×32 pairs)
// Resume-safe: existing valid output files are skipped.
// Output: methode-daten/dekodierungen/<target>_<native>.json
// ============================================================
import { readFileSync, writeFileSync, mkdirSync, existsSync } from "node:fs";
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const __here = dirname(fileURLToPath(import.meta.url));
const root = join(__here, "..", "..");
const outDir = join(root, "methode-daten", "dekodierungen");
mkdirSync(outDir, { recursive: true });

const KEY = execFileSync("security", [
  "find-generic-password", "-s", "ANTHROPIC_API_KEY", "-a", "linguaflow", "-w",
]).toString().trim();

// Same models as the app backend / dieselben Modelle wie das App-Backend.
const DECODE_MODEL_INPUT = "claude-sonnet-5";
const DECODE_MODEL_VERBATIM = "claude-haiku-4-5";

// Spelled-out names (subset of the app's LANGUAGE_NAMES) — the prompt needs
// names, not codes ("write in Romanian" beats "write in RO").
const LANGUAGE_NAMES = {
  AR: "Arabic", BG: "Bulgarian", CS: "Czech", DA: "Danish", DE: "German",
  EL: "Greek", EN: "English", ES: "Spanish", ET: "Estonian", FI: "Finnish",
  FR: "French", HE: "Hebrew", HU: "Hungarian", ID: "Indonesian", IT: "Italian",
  JA: "Japanese", KO: "Korean", LT: "Lithuanian", LV: "Latvian",
  NB: "Norwegian (Bokmål)", NL: "Dutch", PL: "Polish", PT: "Portuguese",
  RO: "Romanian", RU: "Russian", SK: "Slovak", SL: "Slovenian", SV: "Swedish",
  TH: "Thai", TR: "Turkish", UK: "Ukrainian", VI: "Vietnamese",
  ZH: "Chinese (Simplified)",
};

const config = JSON.parse(readFileSync(join(root, "methode-daten", "sprachen.json"), "utf8"));
const LANGS = config.languages;
const byCode = Object.fromEntries(LANGS.map((l) => [l.code, l]));

const texts = JSON.parse(readFileSync(join(root, "methode-daten", "texte", "beispieltext.json"), "utf8"));
const textFor = (code) => (code === "de" ? texts.de : texts.translations[code]);

// ---- Prompt builder, ported VERBATIM from decodeText.ts (mode "input") ----
function buildSystemPrompt(sourceLang, targetLang, includeRomanization, noSpaces) {
  const modeRule = `INPUT HANDLING (mode "input" — text typed by the user):
- If the text is NOT in the learning language: first translate it faithfully into the learning language (correcting obvious spelling/grammar slips along the way), then decode THAT learning-language text.
- If the text IS in the learning language: silently fix spelling, grammar and punctuation mistakes, then decode the corrected text.
- Never change the meaning, tone or content — only correct and/or translate.`;

  const learningName = LANGUAGE_NAMES[sourceLang.toUpperCase()] ?? sourceLang.toUpperCase();
  const nativeName = LANGUAGE_NAMES[targetLang.toUpperCase()] ?? targetLang.toUpperCase();

  return `You are the translation engine of a Birkenbihl-method language-learning app. The learning language is ${learningName} (ISO code "${sourceLang}"); the user's native language is ${nativeName} (ISO code "${targetLang}").

${modeRule}

STRUCTURE:
- Split the decoded text into sentences at sentence-ending punctuation (. ! ? …), keeping each terminator with its sentence. If the text has no sentence-ending punctuation, treat the whole text as one sentence.
- Concatenating all "sentences[].text" values (joined with single spaces) must reproduce the full decoded text — never drop or reorder anything.
- "translation" per sentence: a natural, FLUENT translation of that sentence into the native language ("${targetLang}"). This is deliberately different from the word-for-word pairs.

DECODING RULES — for each sentence produce "pairs", a Birkenbihl-style word-for-word decoding into the native language:
1. ${noSpaces
      ? `"pairs" has one entry per WORD of the sentence, in the EXACT order of the sentence. This language does not put spaces between words — a space marks a phrase or sentence end, never a word boundary. So split each sentence into its REAL words; never treat a whole space-delimited run as one word. Never reorder and never skip anything; concatenating all "w" values of a sentence must reproduce that sentence exactly.`
      : `"pairs" has EXACTLY one entry per whitespace-separated token of the sentence, in the EXACT order of the sentence. Never reorder, never skip, never merge or split tokens.`}
2. "w" is the token verbatim, INCLUDING any attached punctuation (e.g. "right," stays "right,"); "t" is its meaning in the native language IN THIS CONTEXT, with the same punctuation attached (e.g. English "right," in "you are right," → German "richtig,"). NEVER the out-of-context meaning ("rechts").
2b. EVERY "t" must be written in ${nativeName}. If a "t" comes out identical to its "w", you have put the learning language into the meaning column — that is wrong except for proper names and numbers. Watch this especially when the input text is ALREADY in ${learningName}: the text itself then needs no translation, but the "t" values must still be ${nativeName}. Decide this per word, at the start: you are explaining ${learningName} to someone who reads ${nativeName}.
3. Contractions stay ONE token; in "t", join the meaning parts with an apostrophe (English "isn't" → German "ist'nicht"; French "J'ai" → German "Ich'habe").
4. If ONE token needs several words in the native language (polite forms, reflexives, idioms), join them with hyphens so it stays ONE cell (French "Bonjour" → German "Guten-Tag").
5. Inflect articles, cases and endings correctly in the native language; NEVER leave a learning-language function word untranslated.
6. Add a clarifying second reading in round brackets only when genuinely helpful (German example: "richtig (recht)"), and a bracketed helper word where the native language needs one the learning language lacks. Always use ROUND brackets ( ), never square brackets.
6a. NEVER use grammatical terminology as a meaning — no "nominalizer", "classifier", "particle", "marker", "Nominalisierungs-Marker" or similar. The learner is not a linguist and must be able to read the line without knowing grammar terms. If a token has no meaning of its own in the native language, give the closest everyday word it contributes to the phrase, or a plain short hint such as "(Wortteil)" in the native language.
7. Proper names stay unchanged.
8. The decoding deliberately mirrors the STRUCTURE of the learning language — it reads "bumpy" and is NOT a fluent translation; the fluent version belongs in "translation" only.
${includeRomanization ? `
ROMANIZATION — the learning language is not written in Latin script, so each pair additionally gets "r", the Latin romanization of "w":
- Use the standard scheme for the learning language: Hanyu Pinyin WITH tone marks (Chinese), Hepburn romaji (Japanese), Revised Romanization (Korean), RTGS (Thai), and the common practical transliteration for Cyrillic, Greek, Arabic, Hebrew and other scripts.
- "r" transcribes the SOUND/READING of the token in this context — it never translates.
- Keep attached punctuation in "r" exactly as in "w".
- If a token is already in Latin script (names, numbers), "r" is the token unchanged.
` : ""}
Content must always be family-friendly, neutral and unambiguous.`;
}

// ---- JSON schema, ported verbatim / Schema 1:1 übernommen ----
function buildDecodeSchema(includeRomanization) {
  const pairProperties = {
    w: { type: "string", description: "Token in the learning language." },
    t: { type: "string", description: "Contextual meaning in the native language." },
  };
  const pairRequired = ["w", "t"];
  if (includeRomanization) {
    pairProperties.r = {
      type: "string",
      description: "Latin romanization of the token (transcription, not translation).",
    };
    pairRequired.push("r");
  }
  return {
    type: "object",
    properties: {
      text: {
        type: "string",
        description:
          "The learning-language text that was decoded (input mode: corrected/translated; verbatim mode: the input unchanged).",
      },
      sentences: {
        type: "array",
        description: "One entry per sentence of the decoded text, in order.",
        items: {
          type: "object",
          properties: {
            text: { type: "string", description: "The sentence in the learning language." },
            translation: { type: "string", description: "Fluent translation of the sentence into the native language." },
            pairs: {
              type: "array",
              description: "Birkenbihl word-for-word decoding: one entry per whitespace token of the sentence, in order.",
              items: { type: "object", properties: pairProperties, required: pairRequired, additionalProperties: false },
            },
          },
          required: ["text", "translation", "pairs"],
          additionalProperties: false,
        },
      },
    },
    required: ["text", "sentences"],
    additionalProperties: false,
  };
}

// ---- One decode call with retries / Ein Aufruf mit Wiederholungen ----
let usageIn = 0, usageOut = 0;
async function decodePair(target, native) {
  const text = textFor(target);
  if (!text) throw new Error(`Kein Beispieltext für Zielsprache ${target}`);
  const tl = byCode[target];
  const includeRomanization = tl.nonLatin;
  // Own-script shortcut of the backend: TH/JA/ZH texts already in their script
  // use the cheap model (modelForMode in decodeText.ts).
  const model = tl.noSpaces ? DECODE_MODEL_VERBATIM : DECODE_MODEL_INPUT;
  const system = buildSystemPrompt(target.toUpperCase(), native.toUpperCase(), includeRomanization, tl.noSpaces);
  const schema = buildDecodeSchema(includeRomanization);

  for (let attempt = 1; attempt <= 5; attempt++) {
    const res = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: {
        "x-api-key": KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
      },
      body: JSON.stringify({
        model,
        max_tokens: includeRomanization ? 16000 : 12000,
        thinking: { type: "disabled" },
        system,
        messages: [{ role: "user", content: text }],
        output_config: { format: { type: "json_schema", schema } },
      }),
    });
    if (res.status === 429 || res.status >= 500) {
      const wait = attempt * 5000;
      console.warn(`  ${target}_${native}: HTTP ${res.status}, warte ${wait / 1000}s (Versuch ${attempt})`);
      await new Promise((r) => setTimeout(r, wait));
      continue;
    }
    if (!res.ok) throw new Error(`${target}_${native}: HTTP ${res.status} ${(await res.text()).slice(0, 300)}`);
    const data = await res.json();
    if (data.stop_reason === "refusal") throw new Error(`${target}_${native}: refusal`);
    if (data.stop_reason === "max_tokens") throw new Error(`${target}_${native}: truncated`);
    usageIn += data.usage?.input_tokens ?? 0;
    usageOut += data.usage?.output_tokens ?? 0;
    const block = data.content.find((b) => b.type === "text");
    return JSON.parse(block.text);
  }
  throw new Error(`${target}_${native}: aufgegeben nach 5 Versuchen`);
}

// ---- Validation / Prüfung ----
// Pure punctuation/symbol tokens (Japanese 、。 or the Thai repetition mark ๆ)
// legitimately have no meaning and no romanization of their own.
// Reine Satzzeichen-/Symbol-Tokens haben zu Recht keine eigene Bedeutung/Umschrift.
const symbolOnly = (w) => typeof w === "string" && /^[\p{P}\p{S}ๆ]+$/u.test(w);

function validate(parsed, target, native) {
  const problems = [];
  const tl = byCode[target];
  if (!parsed.text || typeof parsed.text !== "string") problems.push("text fehlt");
  if (!Array.isArray(parsed.sentences) || parsed.sentences.length < 2 || parsed.sentences.length > 6) {
    problems.push(`Satzzahl ${parsed.sentences?.length}`);
  }
  for (const s of parsed.sentences ?? []) {
    if (!s.text || !s.translation) problems.push("Satz ohne text/translation");
    if (!Array.isArray(s.pairs) || s.pairs.length === 0) problems.push("Satz ohne pairs");
    for (const p of s.pairs ?? []) {
      if (!p.w) problems.push("Paar ohne w");
      if (!p.t && !symbolOnly(p.w)) problems.push(`Paar ohne Bedeutung bei "${p.w}"`);
      if (tl.nonLatin && !p.r && !symbolOnly(p.w)) problems.push(`Umschrift fehlt bei "${p.w}"`);
    }
  }
  return problems;
}

// ---- CLI ----
const args = process.argv.slice(2);
const argVal = (n) => { const i = args.indexOf(n); return i >= 0 ? args[i + 1] : null; };
const codes = LANGS.map((l) => l.code);
let pairs = [];
if (argVal("--pair")) {
  const [t, n] = argVal("--pair").split(":");
  pairs = [[t, n]];
} else if (argVal("--target")) {
  const t = argVal("--target");
  pairs = codes.filter((n) => n !== t).map((n) => [t, n]);
} else if (args.includes("--all")) {
  for (const t of codes) for (const n of codes) if (t !== n) pairs.push([t, n]);
} else {
  console.error("Usage: --pair t:n | --target t | --all");
  process.exit(1);
}

// Skip pairs whose target text is missing (DeepL not run yet) and existing files.
pairs = pairs.filter(([t]) => textFor(t));

const CONCURRENCY = 4;
let done = 0, skipped = 0, failed = [];
async function worker(queue) {
  while (queue.length > 0) {
    const [t, n] = queue.shift();
    const file = join(outDir, `${t}_${n}.json`);
    if (existsSync(file)) { skipped++; continue; }
    try {
      const parsed = await decodePair(t, n);
      const problems = validate(parsed, t, n);
      if (problems.length > 0) throw new Error(`Validierung: ${problems.join("; ")}`);
      writeFileSync(file, JSON.stringify({
        formatVersion: 1, target: t, native: n,
        text: parsed.text, sentences: parsed.sentences,
      }, null, 1) + "\n");
      done++;
      if (done % 25 === 0) console.log(`  …${done} Paare fertig`);
    } catch (e) {
      failed.push(`${t}_${n}: ${e.message.slice(0, 160)}`);
    }
  }
}
const queue = [...pairs];
await Promise.all(Array.from({ length: CONCURRENCY }, () => worker(queue)));

console.log(`\nFertig: ${done} neu, ${skipped} übersprungen, ${failed.length} fehlgeschlagen.`);
console.log(`Tokens: ${usageIn} rein / ${usageOut} raus.`);
if (failed.length > 0) { console.log("Fehlgeschlagen:"); failed.forEach((f) => console.log("  " + f)); process.exit(2); }
