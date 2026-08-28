#!/usr/bin/env node
// ============================================================
// uebersetze-erklaertext.mjs — DeepL translation of the explanation chapters
// and the UI strings into all native languages of the method page.
// Master is German: methode-daten/texte/erklaertext/de.json + ui.json["de"].
//
// DeepL-Übersetzung der Erklär-Kapitel und UI-Texte in alle Muttersprachen.
// Meister ist Deutsch. Schlüssel aus dem macOS-Schlüsselbund.
//
// Usage: node scripts/methode/uebersetze-erklaertext.mjs [--only en,fr]
// Output: methode-daten/texte/erklaertext/<lang>.json + aktualisierte ui.json
// Resume-safe: vorhandene erklaertext/<lang>.json werden übersprungen.
// ============================================================
import { readFileSync, writeFileSync, existsSync } from "node:fs";
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const __here = dirname(fileURLToPath(import.meta.url));
const root = join(__here, "..", "..");
const textDir = join(root, "methode-daten", "texte");

const KEY = execFileSync("security", [
  "find-generic-password", "-s", "DEEPL_API_KEY", "-a", "linguaflow", "-w",
]).toString().trim();

const DEEPL_TARGET = { en: "EN-US", pt: "PT-PT", zh: "ZH-HANS" };

const config = JSON.parse(readFileSync(join(root, "methode-daten", "sprachen.json"), "utf8"));
const master = JSON.parse(readFileSync(join(textDir, "erklaertext", "de.json"), "utf8"));
const uiAll = JSON.parse(readFileSync(join(textDir, "ui.json"), "utf8"));
const uiKeys = Object.keys(uiAll.de);

const args = process.argv.slice(2);
const onlyIdx = args.indexOf("--only");
const only = onlyIdx >= 0 ? args[onlyIdx + 1].split(",") : null;

let langs = config.languages.map((l) => l.code).filter((c) => c !== "de");
if (only) langs = langs.filter((c) => only.includes(c));

async function deepl(texts, target) {
  const res = await fetch("https://api.deepl.com/v2/translate", {
    method: "POST",
    headers: { "Authorization": `DeepL-Auth-Key ${KEY}`, "Content-Type": "application/json" },
    body: JSON.stringify({
      text: texts,
      source_lang: "DE",
      target_lang: DEEPL_TARGET[target] ?? target.toUpperCase(),
    }),
  });
  if (!res.ok) throw new Error(`DeepL ${target}: ${res.status} ${(await res.text()).slice(0, 200)}`);
  const data = await res.json();
  if (data.translations.length !== texts.length) throw new Error(`DeepL ${target}: Antwortlänge weicht ab`);
  return data.translations.map((t) => t.text);
}

let chars = 0;
for (const lang of langs) {
  const outFile = join(textDir, "erklaertext", `${lang}.json`);
  const needChapters = !existsSync(outFile);
  const needUi = !uiAll[lang];
  if (!needChapters && !needUi) { console.log(`${lang}: schon vorhanden, übersprungen`); continue; }

  // One request per language: all chapter titles + texts + UI strings bundled.
  // Ein Request je Sprache: Titel, Texte und UI-Strings gebündelt.
  const batch = [];
  for (const ch of master.chapters) { batch.push(ch.title, ch.text); }
  for (const k of uiKeys) batch.push(uiAll.de[k]);
  chars += batch.join("").length;

  const out = await deepl(batch, lang);
  let i = 0;
  const chapters = master.chapters.map((ch) => ({ id: ch.id, title: out[i++], text: out[i++] }));
  const uiStrings = {};
  for (const k of uiKeys) uiStrings[k] = out[i++];

  if (needChapters) {
    writeFileSync(outFile, JSON.stringify({ formatVersion: 1, lang, chapters }, null, 2) + "\n");
  }
  if (needUi) uiAll[lang] = uiStrings;
  console.log(`${lang}: ok („${chapters[0].title}")`);
  await new Promise((r) => setTimeout(r, 200));
}

writeFileSync(join(textDir, "ui.json"), JSON.stringify(uiAll, null, 2) + "\n");
console.log(`\nFertig. ~${chars} DeepL-Zeichen (${(chars / 50000).toFixed(2)} €).`);
