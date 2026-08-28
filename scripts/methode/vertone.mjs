#!/usr/bin/env node
// ============================================================
// vertone.mjs — pre-generates ALL audio of the method page with word
// timestamps (ElevenLabs /with-timestamps, same voices and models as the
// app's voice catalog). No key ever ships to the browser — the website only
// serves the resulting static MP3 + timing JSON.
//
// Erzeugt sämtliches Audio der Methoden-Seite vorab mit Wort-Zeitstempeln
// (gleiche Stimmen/Modelle wie die App). Es gelangt nie ein Schlüssel in den
// Browser — die Website liefert nur fertige MP3 + Timing-JSON aus.
//
// Usage:
//   node scripts/methode/vertone.mjs --beispiel [--only de,en]   Beispieltexte
//   node scripts/methode/vertone.mjs --erklaerung [--only de]    Erklär-Kapitel
//   node scripts/methode/vertone.mjs --alles
// Resume-safe: vorhandene MP3+JSON werden übersprungen.
// Timing-JSON: {mode:"words", words:[{s,e}]} je Whitespace-Wort, oder
//              {mode:"chars", chars:[{ch,s,e}]} für Chinesisch/Japanisch/Thai.
// ============================================================
import { readFileSync, writeFileSync, mkdirSync, existsSync } from "node:fs";
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const __here = dirname(fileURLToPath(import.meta.url));
const root = join(__here, "..", "..");
const dataDir = join(root, "methode-daten");

const KEY = execFileSync("security", [
  "find-generic-password", "-s", "ELEVENLABS_API_KEY", "-w",
]).toString().trim();

const config = JSON.parse(readFileSync(join(dataDir, "sprachen.json"), "utf8"));
const byCode = Object.fromEntries(config.languages.map((l) => [l.code, l]));

const args = process.argv.slice(2);
const onlyIdx = args.indexOf("--only");
const only = onlyIdx >= 0 ? args[onlyIdx + 1].split(",") : null;
const doBeispiel = args.includes("--beispiel") || args.includes("--alles");
const doErklaerung = args.includes("--erklaerung") || args.includes("--alles");
if (!doBeispiel && !doErklaerung) {
  console.error("Usage: --beispiel | --erklaerung | --alles [--only de,en]");
  process.exit(1);
}

let totalChars = 0;

async function tts(text, lang) {
  const { voice, model } = byCode[lang];
  const res = await fetch(
    `https://api.elevenlabs.io/v1/text-to-speech/${voice}/with-timestamps?output_format=mp3_44100_128`,
    {
      method: "POST",
      headers: { "xi-api-key": KEY, "Content-Type": "application/json" },
      body: JSON.stringify({ text, model_id: model }),
    }
  );
  if (!res.ok) throw new Error(`TTS ${lang}: ${res.status} ${(await res.text()).slice(0, 200)}`);
  totalChars += text.length;
  const data = await res.json();
  return {
    audio: Buffer.from(data.audio_base64, "base64"),
    chars: data.alignment.characters,
    starts: data.alignment.character_start_times_seconds,
    ends: data.alignment.character_end_times_seconds,
  };
}

// Character timings → timing JSON. Whitespace-token words for spaced
// languages, per-character entries for zh/ja/th.
// Zeichen-Timing → Timing-JSON (Wörter bzw. Einzelzeichen).
function buildTiming(text, aln, noSpaces) {
  if (noSpaces) {
    const chars = [];
    for (let i = 0; i < aln.chars.length; i++) {
      chars.push({ ch: aln.chars[i], s: Math.round(aln.starts[i] * 1000), e: Math.round(aln.ends[i] * 1000) });
    }
    return { mode: "chars", text, chars };
  }
  const words = [];
  let cur = null;
  for (let i = 0; i < aln.chars.length; i++) {
    if (/\s/.test(aln.chars[i])) { if (cur) { words.push(cur); cur = null; } continue; }
    if (!cur) cur = { s: Math.round(aln.starts[i] * 1000), e: 0 };
    cur.e = Math.round(aln.ends[i] * 1000);
  }
  if (cur) words.push(cur);
  const tokens = text.split(/\s+/).filter((t) => t.length > 0).length;
  if (words.length !== tokens) {
    console.warn(`  ⚠️ Wort-Timings (${words.length}) ≠ Tokens (${tokens})`);
  }
  return { mode: "words", text, words };
}

async function vertoneBeispiel() {
  const texts = JSON.parse(readFileSync(join(dataDir, "texte", "beispieltext.json"), "utf8"));
  const outDir = join(dataDir, "audio", "beispiel");
  mkdirSync(outDir, { recursive: true });
  let codes = config.languages.map((l) => l.code);
  if (only) codes = codes.filter((c) => only.includes(c));
  for (const code of codes) {
    const text = code === "de" ? texts.de : texts.translations[code];
    if (!text) { console.log(`Beispiel ${code}: kein Text, übersprungen`); continue; }
    const mp3 = join(outDir, `${code}.mp3`);
    const jsonF = join(outDir, `${code}.json`);
    if (existsSync(mp3) && existsSync(jsonF)) { console.log(`Beispiel ${code}: vorhanden`); continue; }
    const aln = await tts(text, code);
    writeFileSync(mp3, aln.audio);
    writeFileSync(jsonF, JSON.stringify(buildTiming(text, aln, byCode[code].noSpaces)));
    console.log(`Beispiel ${code}: ok (${text.length} Zeichen)`);
    await new Promise((r) => setTimeout(r, 300));
  }
}

async function vertoneErklaerung() {
  let codes = config.languages.map((l) => l.code);
  if (only) codes = codes.filter((c) => only.includes(c));
  for (const code of codes) {
    const file = join(dataDir, "texte", "erklaertext", `${code}.json`);
    if (!existsSync(file)) { console.log(`Erklärung ${code}: kein Text, übersprungen`); continue; }
    const { chapters } = JSON.parse(readFileSync(file, "utf8"));
    const outDir = join(dataDir, "audio", "erklaerung", code);
    mkdirSync(outDir, { recursive: true });
    for (const ch of chapters) {
      const mp3 = join(outDir, `${ch.id}.mp3`);
      const jsonF = join(outDir, `${ch.id}.json`);
      if (existsSync(mp3) && existsSync(jsonF)) continue;
      const aln = await tts(ch.text, code);
      writeFileSync(mp3, aln.audio);
      writeFileSync(jsonF, JSON.stringify(buildTiming(ch.text, aln, byCode[code].noSpaces)));
      await new Promise((r) => setTimeout(r, 300));
    }
    console.log(`Erklärung ${code}: ok (${chapters.length} Kapitel)`);
  }
}

if (doBeispiel) await vertoneBeispiel();
if (doErklaerung) await vertoneErklaerung();
console.log(`\nFertig. ElevenLabs-Zeichen dieser Lauf: ${totalChars}`);
