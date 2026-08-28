#!/usr/bin/env node
// ============================================================
// pruefe.mjs — validates ALL generated data of the method page:
// decodings (complete? text intact? pairs reproduce the text? romanization?),
// audio timings (word counts match token counts, texts match), explanation
// texts and UI strings (complete). Exit 0 = everything green.
//
// Prüft ALLE erzeugten Daten der Methoden-Seite: Dekodierungen (vollständig?
// Text unversehrt? Paare ergeben den Text? Umschrift?), Audio-Zeitstempel
// (Wortzahlen passen, Texte stimmen), Erklärtexte und UI-Strings. Exit 0 = grün.
//
// Usage: node scripts/methode/pruefe.mjs
// ============================================================
import { readFileSync, existsSync, readdirSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const __here = dirname(fileURLToPath(import.meta.url));
const root = join(__here, "..", "..");
const dataDir = join(root, "methode-daten");

const config = JSON.parse(readFileSync(join(dataDir, "sprachen.json"), "utf8"));
const byCode = Object.fromEntries(config.languages.map((l) => [l.code, l]));
const codes = config.languages.map((l) => l.code);
const texts = JSON.parse(readFileSync(join(dataDir, "texte", "beispieltext.json"), "utf8"));
const textFor = (c) => (c === "de" ? texts.de : texts.translations[c]);

const errors = [];
const warns = [];
const err = (m) => errors.push(m);
const warn = (m) => warns.push(m);
const strip = (s) => s.replace(/\s+/g, "");
const tokens = (s) => s.split(/\s+/).filter((t) => t.length > 0).length;

// ---- 1. Decodings / Dekodierungen ----
let decOk = 0;
for (const t of codes) {
  for (const n of codes) {
    if (t === n) continue;
    const f = join(dataDir, "dekodierungen", `${t}_${n}.json`);
    if (!existsSync(f)) { err(`Dekodierung fehlt: ${t}_${n}`); continue; }
    let d;
    try { d = JSON.parse(readFileSync(f, "utf8")); } catch { err(`${t}_${n}: kaputtes JSON`); continue; }
    const canonical = textFor(t);
    if (strip(d.text) !== strip(canonical)) {
      warn(`${t}_${n}: dekodierter Text weicht vom Beispieltext ab`);
    }
    for (const s of d.sentences) {
      if (strip(s.pairs.map((p) => p.w).join("")) !== strip(s.text)) {
        err(`${t}_${n}: Paare ergeben nicht den Satztext („${s.text.slice(0, 30)}…")`);
      }
      const symbolOnly = (w) => typeof w === "string" && /^[\p{P}\p{S}ๆ]+$/u.test(w);
      if (byCode[t].nonLatin && s.pairs.some((p) => !p.r && !symbolOnly(p.w))) err(`${t}_${n}: Umschrift fehlt`);
      if (s.pairs.some((p) => (!p.t || !p.t.trim()) && !symbolOnly(p.w))) err(`${t}_${n}: leere Bedeutung`);
    }
    decOk++;
  }
}

// ---- 2. Example audio / Beispiel-Audio ----
let exOk = 0;
for (const t of codes) {
  const mp3 = join(dataDir, "audio", "beispiel", `${t}.mp3`);
  const jf = join(dataDir, "audio", "beispiel", `${t}.json`);
  if (!existsSync(mp3) || !existsSync(jf)) { err(`Beispiel-Audio fehlt: ${t}`); continue; }
  const tim = JSON.parse(readFileSync(jf, "utf8"));
  const canonical = textFor(t);
  if (strip(tim.text) !== strip(canonical)) err(`Beispiel-Audio ${t}: Text weicht ab`);
  if (byCode[t].noSpaces) {
    if (tim.mode !== "chars") err(`Beispiel-Audio ${t}: mode sollte chars sein`);
    else if (strip(tim.chars.map((c) => c.ch).join("")) !== strip(canonical)) {
      err(`Beispiel-Audio ${t}: Zeichen-Timing deckt Text nicht`);
    }
  } else {
    if (tim.mode !== "words") err(`Beispiel-Audio ${t}: mode sollte words sein`);
    else if (tim.words.length !== tokens(canonical)) {
      err(`Beispiel-Audio ${t}: ${tim.words.length} Wort-Timings vs ${tokens(canonical)} Tokens`);
    }
  }
  exOk++;
}

// ---- 3. Explanation texts + audio / Erklärtexte + Audio ----
let chapOk = 0, chapAudioOk = 0;
const master = JSON.parse(readFileSync(join(dataDir, "texte", "erklaertext", "de.json"), "utf8"));
const chapterIds = master.chapters.map((c) => c.id);
for (const n of codes) {
  const f = join(dataDir, "texte", "erklaertext", `${n}.json`);
  if (!existsSync(f)) { err(`Erklärtext fehlt: ${n}`); continue; }
  const d = JSON.parse(readFileSync(f, "utf8"));
  if (d.chapters.length !== chapterIds.length) err(`Erklärtext ${n}: ${d.chapters.length} Kapitel statt ${chapterIds.length}`);
  if (d.chapters.some((c) => !c.title.trim() || !c.text.trim())) err(`Erklärtext ${n}: leeres Kapitel`);
  chapOk++;
  for (const ch of d.chapters) {
    const mp3 = join(dataDir, "audio", "erklaerung", n, `${ch.id}.mp3`);
    const jf = join(dataDir, "audio", "erklaerung", n, `${ch.id}.json`);
    if (!existsSync(mp3) || !existsSync(jf)) { err(`Kapitel-Audio fehlt: ${n}/${ch.id}`); continue; }
    const tim = JSON.parse(readFileSync(jf, "utf8"));
    if (strip(tim.text) !== strip(ch.text)) err(`Kapitel-Audio ${n}/${ch.id}: Text weicht ab`);
    if (tim.mode === "words" && tim.words.length !== tokens(ch.text)) {
      warn(`Kapitel-Audio ${n}/${ch.id}: ${tim.words.length} Timings vs ${tokens(ch.text)} Tokens`);
    }
    chapAudioOk++;
  }
}

// ---- 4. UI strings / UI-Texte ----
const uiAll = JSON.parse(readFileSync(join(dataDir, "texte", "ui.json"), "utf8"));
const uiKeys = Object.keys(uiAll.de);
for (const n of codes) {
  if (!uiAll[n]) { err(`UI-Texte fehlen: ${n}`); continue; }
  for (const k of uiKeys) if (!uiAll[n][k] || !uiAll[n][k].trim()) err(`UI ${n}: Schlüssel ${k} leer`);
}

const totalDec = codes.length * (codes.length - 1);
console.log(`Dekodierungen: ${decOk}/${totalDec} vorhanden und geprüft`);
console.log(`Beispiel-Audio: ${exOk}/${codes.length}`);
console.log(`Erklärtexte: ${chapOk}/${codes.length} · Kapitel-Audio: ${chapAudioOk}/${codes.length * chapterIds.length}`);
console.log(`Fehler: ${errors.length} · Warnungen: ${warns.length}`);
if (warns.length) { console.log("\nWarnungen:"); warns.slice(0, 40).forEach((w) => console.log("  ⚠️ " + w)); }
if (errors.length) { console.log("\nFehler:"); errors.slice(0, 60).forEach((e) => console.log("  ❌ " + e)); process.exit(1); }
console.log("\n✅ Alles grün.");
