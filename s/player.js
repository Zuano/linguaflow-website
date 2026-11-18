// LinguaFlow online player: shows a shared, decoded text in the browser.
// LinguaFlow Online-Player: zeigt einen geteilten, dekodierten Text im Browser.
//
// Security rule: shared content is untrusted. It is only ever inserted with
// textContent, never as HTML, and never becomes a link.
// Sicherheitsregel: Geteilter Inhalt ist nicht vertrauenswürdig. Er wird nur
// mit textContent eingesetzt, nie als HTML, und wird nie zu einem Link.

const API_URL = 'https://europe-west1-linguaflow-firebase.cloudfunctions.net/getShare';
const APP_STORE_URL = 'https://apps.apple.com/us/app/linguaflow-decoder/id6744939323';
const PLAY_URL = 'https://play.google.com/store/apps/details?id=com.linguaflow';
const PLAY_REFERRER = 'utm_source%3Dshare%26utm_medium%3Dweb%26utm_campaign%3Donline_share';
const SITE = 'https://linguaflow.app';
const SPEEDS = [0.5, 0.75, 1];

// ---------------------------------------------------------------------------
// Pure functions (tested in player.test.mjs) / Reine Funktionen (getestet)
// ---------------------------------------------------------------------------

/** Share IDs are exactly 22 Base64-URL characters. / Genau 22 Base64-URL-Zeichen. */
export function isValidShareId(id) {
  return typeof id === 'string' && /^[A-Za-z0-9_-]{22}$/.test(id);
}

// App language codes (uppercase) → browser language tags (BCP 47).
// Sprach-Codes der App (Großbuchstaben) → Sprach-Kennungen des Browsers.
const BCP47 = {
  EN: 'en-US', 'EN-US': 'en-US', 'EN-GB': 'en-GB', DE: 'de-DE', FR: 'fr-FR', ES: 'es-ES',
  IT: 'it-IT', PT: 'pt-PT', 'PT-PT': 'pt-PT', 'PT-BR': 'pt-BR', AR: 'ar-SA', BG: 'bg-BG',
  ZH: 'zh-CN', 'ZH-HANS': 'zh-CN', 'ZH-HANT': 'zh-TW', DA: 'da-DK', NL: 'nl-NL', ET: 'et-EE',
  FI: 'fi-FI', EL: 'el-GR', HE: 'he-IL', HU: 'hu-HU', ID: 'id-ID', JA: 'ja-JP', KO: 'ko-KR',
  LV: 'lv-LV', LT: 'lt-LT', NB: 'nb-NO', PL: 'pl-PL', RO: 'ro-RO', RU: 'ru-RU', SK: 'sk-SK',
  SL: 'sl-SI', SV: 'sv-SE', TH: 'th-TH', CS: 'cs-CZ', TR: 'tr-TR', UK: 'uk-UA', VI: 'vi-VN',
  FA: 'fa-IR', UR: 'ur-PK',
};

/** 'ES' → 'es-ES', 'PT-BR' → 'pt-BR'. Unknown but well-formed codes are passed on in lowercase. */
export function toBcp47(code) {
  if (typeof code !== 'string' || !/^[A-Za-z-]{2,7}$/.test(code)) return '';
  const upper = code.toUpperCase();
  if (BCP47[upper]) return BCP47[upper];
  const [primary, region] = upper.split('-');
  return region ? `${primary.toLowerCase()}-${region}` : primary.toLowerCase();
}

function primaryLanguage(tagOrCode) {
  return String(tagOrCode || '').replace('_', '-').split('-')[0].toLowerCase();
}

/** Right-to-left learning languages, like in the app. / Sprachen von rechts nach links. */
export function isRtlLanguage(code) {
  return ['ar', 'he', 'fa', 'ur'].includes(primaryLanguage(code));
}

/** German UI for German browsers, English for everyone else. */
export function uiLanguage(browserLanguage) {
  return /^de\b/i.test(String(browserLanguage || '')) ? 'de' : 'en';
}

/**
 * Checks the server answer and keeps only the known fields.
 * Prüft die Server-Antwort und übernimmt nur die bekannten Felder.
 * Returns null if the data cannot be shown.
 */
export function decodeShare(json) {
  if (!json || typeof json !== 'object' || json.v !== 1) return null;
  const isCode = (c) => typeof c === 'string' && /^[A-Za-z-]{2,7}$/.test(c);
  if (!isCode(json.learningLanguage) || !isCode(json.nativeLanguage)) return null;
  if (!Array.isArray(json.words) || json.words.length === 0) return null;

  const words = [];
  for (const w of json.words) {
    if (!w || typeof w.o !== 'string' || w.o === '') return null;
    if (w.t !== undefined && typeof w.t !== 'string') return null;
    const word = { o: w.o, t: w.t || '' };
    if (typeof w.r === 'string' && w.r !== '') word.r = w.r;
    if (typeof w.k === 'string' && w.k !== '') word.k = w.k;
    if (Number.isInteger(w.s) && w.s >= 0) word.s = w.s;
    words.push(word);
  }
  return {
    learningLanguage: json.learningLanguage,
    nativeLanguage: json.nativeLanguage,
    title: typeof json.title === 'string' ? json.title.trim() : '',
    words,
    sentences: Array.isArray(json.sentences)
      ? json.sentences.map((s) => (typeof s === 'string' ? s : ''))
      : [],
    expiresAtMs: Number.isFinite(json.expiresAtMs) ? json.expiresAtMs : null,
  };
}

// Sentence-ending punctuation, optionally followed by a closing quote or bracket.
// Satzende-Zeichen, danach eventuell ein schließendes Anführungszeichen.
const SENTENCE_END = /[.!?…。！？؟۔][»"'”’)\]]*$/;

/**
 * Splits the words into sentence groups: [{ start, end, s }] (end is exclusive).
 * - With sentence numbers (`s`): a new group starts whenever the number changes;
 *   words without a number stay in the running group.
 * - Without any sentence number (old history entries): split after sentence-ending
 *   punctuation, like the app does. A text without punctuation is one group.
 * Teilt die Wörter in Satz-Gruppen.
 */
export function groupSentences(words) {
  const groups = [];
  if (!words || words.length === 0) return groups;
  const numbered = words.some((w) => Number.isInteger(w.s));

  let start = 0;
  let current = numbered ? (Number.isInteger(words[0].s) ? words[0].s : null) : null;
  for (let i = 1; i < words.length; i++) {
    let breakHere;
    if (numbered) {
      breakHere = Number.isInteger(words[i].s) && words[i].s !== current;
    } else {
      breakHere = SENTENCE_END.test(words[i - 1].o);
    }
    if (breakHere) {
      groups.push({ start, end: i, s: current });
      start = i;
      if (numbered) current = words[i].s;
    }
  }
  groups.push({ start, end: words.length, s: current });
  return groups;
}

/**
 * The free translation that belongs to a group ('' if there is none).
 * With sentence numbers the number is the position in `sentences` (starting at 0).
 * Without numbers the lists are only matched if they have the same length.
 */
export function sentenceTranslation(groups, groupIndex, sentences) {
  const group = groups[groupIndex];
  if (!group || !Array.isArray(sentences)) return '';
  let text;
  if (group.s !== null) text = sentences[group.s];
  else if (sentences.length === groups.length) text = sentences[groupIndex];
  return typeof text === 'string' ? text.trim() : '';
}

/**
 * Builds the text that is read aloud for words[start..end) and remembers where
 * each word starts, so a "word boundary" event of the browser can be mapped back.
 * Baut den Vorlese-Text und merkt sich, an welcher Stelle jedes Wort beginnt.
 * Chinese, Japanese and Thai are written without spaces.
 */
export function buildSpeechText(words, start, end, languageCode) {
  const joiner = ['zh', 'ja', 'th'].includes(primaryLanguage(languageCode)) ? '' : ' ';
  const offsets = [];
  let text = '';
  for (let i = start; i < end; i++) {
    if (i > start) text += joiner;
    offsets.push(text.length);
    text += words[i].o;
  }
  return { text, offsets };
}

/** Character position → index of the word that contains it (binary search). */
export function wordIndexAtChar(offsets, charIndex) {
  if (!offsets.length || !Number.isFinite(charIndex)) return -1;
  let low = 0;
  let high = offsets.length - 1;
  while (low < high) {
    const mid = (low + high + 1) >> 1;
    if (offsets[mid] <= charIndex) low = mid;
    else high = mid - 1;
  }
  return low;
}

// Some systems report older or alternative language names for the same language.
// Manche Systeme melden ältere Namen für dieselbe Sprache.
const VOICE_ALIASES = { nb: ['no', 'nn'], he: ['iw'], id: ['in'] };

/**
 * Picks a device voice for the language tag: exact match first, then the same
 * language with another region. Returns null if the device has none.
 * Sucht eine Geräte-Stimme für die Sprache; null, wenn es keine gibt.
 */
export function pickVoice(voices, tag) {
  if (!tag || !voices || !voices.length) return null;
  const wanted = tag.toLowerCase();
  const primary = primaryLanguage(tag);
  const accepted = [primary, ...(VOICE_ALIASES[primary] || [])];
  const langOf = (v) => String(v.lang || '').replace('_', '-').toLowerCase();
  return (
    voices.find((v) => langOf(v) === wanted) ||
    voices.find((v) => accepted.includes(primaryLanguage(v.lang))) ||
    null
  );
}

/** Store links with the campaign label from the plan. / Store-Links mit Kampagnen-Kennung. */
export function storeLinks(ui) {
  return {
    appStore: `${APP_STORE_URL}?ct=online_share`,
    play: `${PLAY_URL}${ui === 'de' ? '&hl=de' : ''}&referrer=${PLAY_REFERRER}`,
  };
}

export function appLink(id) {
  return `linguaflow://share?id=${id}`;
}

export function reportLink(id, subjectPrefix) {
  return `mailto:hello@linguaflow.app?subject=${encodeURIComponent(`${subjectPrefix} ${id}`)}`;
}

export function formatExpiry(ms, ui) {
  return new Intl.DateTimeFormat(ui === 'de' ? 'de-AT' : 'en-GB', { dateStyle: 'long' }).format(
    new Date(ms),
  );
}

export const STRINGS = {
  de: {
    sharedText: 'Geteilter Text',
    loading: 'Text wird geladen …',
    notFound: 'Dieser Link ist abgelaufen oder ungültig.',
    notFoundHint: 'Geteilte Texte sind 90 Tage lang verfügbar.',
    invalid: 'Dieser Link ist unvollständig.',
    invalidHint: 'Öffne ihn bitte noch einmal aus der Nachricht, in der du ihn bekommen hast.',
    error:
      'Der geteilte Text konnte nicht geladen werden. Prüfe deine Internetverbindung und versuch es noch einmal.',
    retry: 'Noch einmal versuchen',
    openApp: 'In LinguaFlow öffnen',
    hideTranslation: 'Übersetzung ausblenden',
    hideForeign: 'Fremdsprache ausblenden',
    display: 'Anzeige',
    play: 'Vorlesen',
    pause: 'Pause',
    player: 'Vorlesen',
    speed: 'Tempo',
    playFrom: 'Ab Satz {n} vorlesen',
    getApp: 'Mit der LinguaFlow-App kannst du diesen Text speichern und eigene Texte dekodieren.',
    getAppMissing: 'Mit der LinguaFlow-App kannst du eigene Texte Wort für Wort dekodieren.',
    appStoreAlt: 'Laden im App Store',
    playAlt: 'Jetzt bei Google Play',
    expires: 'Dieser Text ist bis {date} verfügbar.',
    imprint: 'Impressum',
    privacy: 'Datenschutz',
    report: 'Inhalt melden',
    reportSubject: 'Inhalt melden: geteilter Text',
    imprintUrl: `${SITE}/impressum.html`,
    privacyUrl: `${SITE}/datenschutz.html`,
  },
  en: {
    sharedText: 'Shared text',
    loading: 'Loading text…',
    notFound: 'This link has expired or is invalid.',
    notFoundHint: 'Shared texts are available for 90 days.',
    invalid: 'This link is incomplete.',
    invalidHint: 'Please open it again from the message you received it in.',
    error:
      'The shared text could not be loaded. Check your internet connection and try again.',
    retry: 'Try again',
    openApp: 'Open in LinguaFlow',
    hideTranslation: 'Hide translation',
    hideForeign: 'Hide foreign language',
    display: 'Display',
    play: 'Read aloud',
    pause: 'Pause',
    player: 'Read aloud',
    speed: 'Speed',
    playFrom: 'Read aloud from sentence {n}',
    getApp: 'With the LinguaFlow app you can save this text and decode your own texts.',
    getAppMissing: 'With the LinguaFlow app you can decode your own texts word by word.',
    appStoreAlt: 'Download on the App Store',
    playAlt: 'Get it on Google Play',
    expires: 'This text is available until {date}.',
    imprint: 'Imprint',
    privacy: 'Privacy policy',
    report: 'Report content',
    reportSubject: 'Report content: shared text',
    imprintUrl: `${SITE}/en/impressum.html`,
    privacyUrl: `${SITE}/en/datenschutz.html`,
  },
};

// ---------------------------------------------------------------------------
// Page logic (browser only) / Seiten-Logik (nur im Browser)
// ---------------------------------------------------------------------------

function startPage() {
  const $ = (id) => document.getElementById(id);
  const root = document.documentElement;
  const ui = uiLanguage(navigator.language);
  const t = STRINGS[ui];
  const params = new URLSearchParams(location.search);
  const id = params.get('id');
  const isLocal = ['localhost', '127.0.0.1', '[::1]'].includes(location.hostname);

  // Local test only: ?mock=1 loads mock-share.json, ?mock=ja loads mock-share-ja.json.
  // Nur für den lokalen Test; auf der echten Website ohne Wirkung.
  const mock = isLocal ? params.get('mock') : null;
  const mockFile =
    mock && /^[a-z0-9-]{1,20}$/.test(mock)
      ? mock === '1' ? 'mock-share.json' : `mock-share-${mock}.json`
      : null;

  let share = null;
  let groups = [];
  let cards = [];
  let sections = [];

  // --- Fixed interface texts / Feste Oberflächen-Texte ---
  root.lang = ui;
  document.title = `${t.sharedText} – LinguaFlow`;
  $('open-app').textContent = t.openApp;
  $('retry').textContent = t.retry;
  $('toggles').setAttribute('aria-label', t.display);
  $('toggle-t').textContent = t.hideTranslation;
  $('toggle-o').textContent = t.hideForeign;
  $('player').setAttribute('aria-label', t.player);
  $('play-label').textContent = t.play;
  $('speeds').setAttribute('aria-label', t.speed);
  for (const button of $('speeds').querySelectorAll('button')) {
    // "0,5×" in German, "0.5×" in English
    button.textContent = `${Number(button.dataset.rate).toLocaleString(ui)}×`;
  }
  $('link-imprint').textContent = t.imprint;
  $('link-imprint').href = t.imprintUrl;
  $('link-privacy').textContent = t.privacy;
  $('link-privacy').href = t.privacyUrl;
  $('link-report').textContent = t.report;
  const links = storeLinks(ui);
  $('store-ios').href = links.appStore;
  $('store-ios-img').alt = t.appStoreAlt;
  $('store-android').href = links.play;
  $('store-android-img').alt = t.playAlt;

  // --- States: loading, ready, notfound, invalid, error / Zustände ---
  function setState(state) {
    const message = { loading: t.loading, notfound: t.notFound, invalid: t.invalid, error: t.error }[state];
    const hint = { notfound: t.notFoundHint, invalid: t.invalidHint }[state];
    $('status').hidden = state === 'ready';
    $('status').classList.toggle('is-loading', state === 'loading');
    $('status-text').textContent = message || '';
    $('status-hint').textContent = hint || '';
    $('status-hint').hidden = !hint;
    $('retry').hidden = state !== 'error';
    $('share').hidden = state !== 'ready';
    $('open-app').hidden = state !== 'ready';
    $('get-app').hidden = state === 'loading' || state === 'error';
    $('get-app-text').textContent = state === 'ready' ? t.getApp : t.getAppMissing;
  }

  async function load() {
    setState('loading');
    const url = mockFile || `${API_URL}?id=${encodeURIComponent(id)}`;
    const abort = new AbortController();
    const timer = setTimeout(() => abort.abort(), 15000);
    try {
      const response = await fetch(url, {
        credentials: 'omit',
        referrerPolicy: 'no-referrer',
        signal: abort.signal,
      });
      if (response.status === 404) return setState('notfound');
      if (response.status === 400) return setState('invalid');
      if (!response.ok) return setState('error');
      share = decodeShare(await response.json());
      if (!share) return setState('error');
      // The server checks this too; the answer may come from a 5-minute cache.
      // Der Server prüft das auch; die Antwort kann 5 Minuten alt sein.
      if (share.expiresAtMs !== null && share.expiresAtMs < Date.now()) return setState('notfound');
      render();
      setState('ready');
      setUpSpeech();
    } catch {
      setState('error');
    } finally {
      clearTimeout(timer);
    }
  }

  // --- Rendering / Anzeige ---
  function element(tag, className, text) {
    const node = document.createElement(tag);
    node.className = className;
    if (text !== undefined) node.textContent = text;
    return node;
  }

  function render() {
    const learnTag = toBcp47(share.learningLanguage);
    const nativeTag = toBcp47(share.nativeLanguage);
    const rowDirection = isRtlLanguage(share.learningLanguage) ? 'rtl' : 'ltr';
    groups = groupSentences(share.words);
    cards = [];
    sections = [];

    $('title').textContent = share.title || t.sharedText;
    if (share.title) document.title = `${share.title} – LinguaFlow`;

    const fragment = document.createDocumentFragment();
    groups.forEach((group, groupIndex) => {
      const section = element('section', 'sent');
      section.dataset.g = String(groupIndex);

      const playButton = element('button', 'sent-play');
      playButton.type = 'button';
      playButton.setAttribute('aria-label', t.playFrom.replace('{n}', String(groupIndex + 1)));
      section.appendChild(playButton);

      const row = element('div', 'row');
      row.lang = learnTag;
      row.dir = rowDirection;
      for (let i = group.start; i < group.end; i++) {
        const word = share.words[i];
        const card = element('span', 'card');
        card.appendChild(element('span', 'o', word.o));
        if (word.k) card.appendChild(element('span', 'k', word.k));
        if (word.r) card.appendChild(element('span', 'r', word.r));
        const meaning = element('span', 't', word.t || ' ');
        meaning.lang = nativeTag;
        meaning.dir = 'auto';
        card.appendChild(meaning);
        row.appendChild(card);
        cards.push(card);
      }
      section.appendChild(row);

      const translation = sentenceTranslation(groups, groupIndex, share.sentences);
      if (translation) {
        const line = element('p', 'sent-tr', translation);
        line.lang = nativeTag;
        line.dir = 'auto';
        section.appendChild(line);
      }
      sections.push(section);
      fragment.appendChild(section);
    });
    $('text').replaceChildren(fragment);

    $('link-report').href = reportLink(id, t.reportSubject);
    $('link-report').hidden = false;
    if (share.expiresAtMs !== null) {
      $('expires').textContent = t.expires.replace('{date}', formatExpiry(share.expiresAtMs, ui));
      $('expires').hidden = false;
    }
  }

  // --- Hide switches: only one line can be hidden at a time ---
  // --- Ausblend-Schalter: immer nur eine Zeile ausgeblendet ---
  function setHidden(which) {
    root.classList.toggle('hide-t', which === 't');
    root.classList.toggle('hide-o', which === 'o');
    $('toggle-t').setAttribute('aria-pressed', String(which === 't'));
    $('toggle-o').setAttribute('aria-pressed', String(which === 'o'));
  }
  $('toggle-t').addEventListener('click', () => setHidden(root.classList.contains('hide-t') ? null : 't'));
  $('toggle-o').addEventListener('click', () => setHidden(root.classList.contains('hide-o') ? null : 'o'));

  // --- Reading aloud with the voice built into the device ---
  // --- Vorlesen mit der im Gerät eingebauten Stimme ---
  const synth = 'speechSynthesis' in window && 'SpeechSynthesisUtterance' in window
    ? window.speechSynthesis
    : null;
  const speech = { voice: null, rate: 1, current: 0, playing: false, run: 0, utterance: null };
  let markedSection = null;
  let markedCard = null;

  function markSection(section) {
    if (markedSection) markedSection.classList.remove('speaking');
    markedSection = section;
    if (section) section.classList.add('speaking');
  }
  function markCard(card) {
    if (markedCard) markedCard.classList.remove('cur');
    markedCard = card || null;
    if (markedCard) markedCard.classList.add('cur');
  }
  function showPlaying(playing) {
    speech.playing = playing;
    $('play').classList.toggle('is-playing', playing);
    $('play-label').textContent = playing ? t.pause : t.play;
  }

  function findVoice() {
    if (!synth || !share || speech.voice) return;
    speech.voice = pickVoice(synth.getVoices(), toBcp47(share.learningLanguage));
    if (!speech.voice) return;
    // The bar and the sentence buttons only appear once a matching voice exists.
    // Leiste und Satz-Knöpfe erscheinen erst, wenn es eine passende Stimme gibt.
    $('player').hidden = false;
    root.classList.add('has-speech');
  }

  function setUpSpeech() {
    if (!synth) return;
    synth.cancel(); // stop leftovers of a previous page / Reste einer früheren Seite stoppen
    findVoice();
    if (synth.addEventListener) synth.addEventListener('voiceschanged', findVoice);
    else synth.onvoiceschanged = findVoice;
    // Some browsers never fire "voiceschanged": ask again a few times, then give up.
    // Manche Browser melden die Stimmen nie von selbst: ein paar Mal nachfragen.
    let tries = 0;
    const timer = setInterval(() => {
      findVoice();
      if (speech.voice || ++tries >= 10) clearInterval(timer);
    }, 300);
  }

  function speakFrom(groupIndex) {
    if (!speech.voice || !groups[groupIndex]) return;
    const run = ++speech.run; // events of older utterances are ignored / ältere Ereignisse ignorieren
    if (synth.speaking || synth.pending) synth.cancel();
    speech.current = groupIndex;

    const group = groups[groupIndex];
    const { text, offsets } = buildSpeechText(share.words, group.start, group.end, share.learningLanguage);
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.voice = speech.voice;
    utterance.lang = speech.voice.lang.replace('_', '-');
    utterance.rate = speech.rate;
    utterance.onboundary = (event) => {
      if (run !== speech.run || (event.name && event.name !== 'word')) return;
      const index = wordIndexAtChar(offsets, event.charIndex);
      if (index >= 0) markCard(cards[group.start + index]);
    };
    utterance.onend = () => {
      if (run !== speech.run) return;
      if (groupIndex + 1 < groups.length) speakFrom(groupIndex + 1);
      else stopSpeaking(0);
    };
    utterance.onerror = () => {
      if (run === speech.run) stopSpeaking(groupIndex);
    };
    speech.utterance = utterance; // keep a reference, some browsers lose it otherwise

    markCard(null);
    markSection(sections[groupIndex]);
    const calm = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    sections[groupIndex].scrollIntoView({ block: 'nearest', behavior: calm ? 'auto' : 'smooth' });
    showPlaying(true);
    synth.speak(utterance);
  }

  // "Pause" stops and remembers the sentence; "play" starts that sentence again.
  // (The real pause function of browsers is unreliable, mainly on Android.)
  // „Pause“ stoppt und merkt sich den Satz; „Vorlesen“ beginnt diesen Satz neu.
  function stopSpeaking(resumeAt) {
    speech.run++;
    speech.current = resumeAt;
    if (synth.speaking || synth.pending) synth.cancel();
    markCard(null);
    if (resumeAt === 0) markSection(null);
    showPlaying(false);
  }

  $('play').addEventListener('click', () => {
    if (speech.playing) stopSpeaking(speech.current);
    else speakFrom(speech.current);
  });

  // One listener for all sentences (event delegation). / Ein Listener für alle Sätze.
  $('text').addEventListener('click', (event) => {
    if (!speech.voice) return;
    const section = event.target.closest('.sent');
    if (!section) return;
    // Selecting text with the mouse must not start the voice.
    // Text markieren darf das Vorlesen nicht starten.
    if (!event.target.closest('.sent-play') && String(window.getSelection())) return;
    speakFrom(Number(section.dataset.g));
  });

  $('speeds').addEventListener('click', (event) => {
    const button = event.target.closest('button[data-rate]');
    if (!button) return;
    const rate = Number(button.dataset.rate);
    if (!SPEEDS.includes(rate)) return;
    speech.rate = rate;
    for (const other of $('speeds').querySelectorAll('button')) {
      other.setAttribute('aria-pressed', String(other === button));
    }
    if (speech.playing) speakFrom(speech.current);
  });

  // Leaving the page stops the voice. / Beim Verlassen der Seite verstummt die Stimme.
  window.addEventListener('pagehide', () => {
    if (synth) synth.cancel();
  });

  // --- Start ---
  $('retry').addEventListener('click', load);
  if (!isValidShareId(id)) {
    setState('invalid');
    return;
  }
  $('open-app').href = appLink(id);
  load();
}

if (typeof document !== 'undefined') startPage();
