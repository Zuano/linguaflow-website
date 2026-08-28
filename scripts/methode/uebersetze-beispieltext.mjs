#!/usr/bin/env node
// ============================================================
// uebersetze-beispieltext.mjs — one-time DeepL translation of the German
// master example text into all 33 target languages of the method page.
// Key comes from the macOS keychain, never from a file or argument.
//
// Einmalige DeepL-Übersetzung des deutschen Meister-Beispieltexts in die
// 33 Zielsprachen der Methoden-Seite. Schlüssel aus dem macOS-Schlüsselbund.
//
// Usage: node scripts/methode/uebersetze-beispieltext.mjs
// Output: methode-daten/texte/beispieltext.json
// ============================================================
import { readFileSync, writeFileSync } from "node:fs";
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const __here = dirname(fileURLToPath(import.meta.url));
const root = join(__here, "..", "..");

const KEY = execFileSync("security", [
  "find-generic-password", "-s", "DEEPL_API_KEY", "-a", "linguaflow", "-w",
]).toString().trim();

// The approved German master text (decision 2026-08-28, see plan-methode-seite.md).
// Der freigegebene deutsche Meistertext (Entscheidung 2026-08-28).
const MASTER_DE =
  "Ich habe viele Jahre in meinem Beruf gearbeitet. " +
  "Dann bin ich in ein neues Land gekommen. " +
  "Jetzt lerne ich die Sprache. " +
  "Bald arbeite ich wieder in meinem Beruf.";

// App code (lowercase) → DeepL target code. DeepL insists on regional variants
// for EN/PT/ZH; we use US English, European Portuguese and Simplified Chinese.
// App-Code → DeepL-Zielcode (EN/PT/ZH brauchen Regions-Varianten).
const DEEPL_TARGET = {
  en: "EN-US", pt: "PT-PT", zh: "ZH-HANS",
};

const config = JSON.parse(readFileSync(join(root, "methode-daten", "sprachen.json"), "utf8"));
const targets = config.languages.map((l) => l.code).filter((c) => c !== "de");

async function translate(targetCode) {
  const res = await fetch("https://api.deepl.com/v2/translate", {
    method: "POST",
    headers: {
      "Authorization": `DeepL-Auth-Key ${KEY}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      text: [MASTER_DE],
      source_lang: "DE",
      target_lang: DEEPL_TARGET[targetCode] ?? targetCode.toUpperCase(),
    }),
  });
  if (!res.ok) throw new Error(`DeepL ${targetCode}: ${res.status} ${(await res.text()).slice(0, 200)}`);
  const data = await res.json();
  return data.translations[0].text;
}

const out = { formatVersion: 1, de: MASTER_DE, translations: {} };
let chars = 0;
for (const code of targets) {
  out.translations[code] = await translate(code);
  chars += MASTER_DE.length;
  console.log(`${code}: ${out.translations[code]}`);
  await new Promise((r) => setTimeout(r, 150)); // gentle rate limit / sanftes Tempolimit
}

writeFileSync(join(root, "methode-daten", "texte", "beispieltext.json"), JSON.stringify(out, null, 2) + "\n");
console.log(`\nFertig: ${targets.length} Sprachen, ~${chars} DeepL-Zeichen.`);
