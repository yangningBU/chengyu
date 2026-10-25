const CSV_URL = "chengyu.csv";
const EPOCH = Date.UTC(2026, 0, 1); // day 0 of the rotation
const HISTORY = 30;                 // days before an idiom may repeat
// ?context=iframe shows only the characters and pinyin, scaled to fill the frame.
const IFRAME = new URLSearchParams(location.search).get("context") === "iframe";
if (IFRAME) document.documentElement.classList.add("iframe");

// Iframe: size the glyph row from the frame's measured box rather than vw/vh,
// which mobile Safari can resolve against the parent page. Fill the width,
// shrinking only if the row would overflow the height.
function fitIframe() {
  const row = document.querySelector(".idiom");
  if (!row) return;
  const root = document.documentElement;
  const room = root.clientHeight * 0.94;
  let size = 100;
  // Pinyin has a px floor on wider frames, so scale twice to settle.
  for (let i = 0; i < 2; i++) {
    row.style.fontSize = `${size}px`;
    const width = [...row.children].reduce((sum, col) => sum + col.offsetWidth, 0);
    size *= Math.min(root.clientWidth * 0.96 / width, room / row.offsetHeight);
  }
  row.style.fontSize = `${size}px`;
}
if (IFRAME) {
  addEventListener("resize", fitIframe);
  document.fonts.ready.then(fitIframe);
}

// Minimal RFC 4180 CSV parser (handles quoted fields, commas, "" escapes).
function parseCSV(text) {
  const rows = [];
  let row = [], field = "", quoted = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (quoted) {
      if (c === '"' && text[i + 1] === '"') { field += '"'; i++; }
      else if (c === '"') quoted = false;
      else field += c;
    } else if (c === '"') quoted = true;
    else if (c === ",") { row.push(field); field = ""; }
    else if (c === "\n" || c === "\r") {
      if (c === "\r" && text[i + 1] === "\n") i++;
      row.push(field); rows.push(row); row = []; field = "";
    } else field += c;
  }
  if (field || row.length) { row.push(field); rows.push(row); }
  const [header, ...body] = rows;
  return body
    .filter(r => r.some(Boolean))
    .map(r => Object.fromEntries(header.map((h, i) => [h.trim(), (r[i] || "").trim()])));
}

// Small deterministic PRNG so every visitor sees the same idiom on the same day.
function mulberry32(seed) {
  return function () {
    seed |= 0; seed = (seed + 0x6D2B79F5) | 0;
    let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function dayNumber(date) {
  const local = Date.UTC(date.getFullYear(), date.getMonth(), date.getDate());
  return Math.abs(Math.floor((local - EPOCH) / 86400000));
}

// Replays the rotation from the epoch, keeping a rolling record of the last
// HISTORY picks and excluding them from each day's draw. Returns today's index.
function pickForDay(day, count) {
  const windowSize = Math.min(HISTORY, count - 1);
  const recent = [];
  let pick = 0;
  for (let d = 0; d <= day; d++) {
    const excluded = new Set(recent);
    const pool = [];
    for (let i = 0; i < count; i++) if (!excluded.has(i)) pool.push(i);
    pick = pool[Math.floor(mulberry32(d * 7919 + 17)() * pool.length)];
    recent.push(pick);
    if (recent.length > windowSize) recent.shift();
  }
  return pick;
}

function el(tag, cls, text) {
  const node = document.createElement(tag);
  if (cls) node.className = cls;
  if (text != null) node.textContent = text;
  return node;
}

// Tone number (1-4) from a syllable's diacritic; 0 for neutral tone.
const TONE_MARKS = { "\u0304": 1, "\u0301": 2, "\u030C": 3, "\u0300": 4 };
function toneOf(syllable) {
  for (const c of syllable.normalize("NFD")) if (TONE_MARKS[c]) return TONE_MARKS[c];
  return 0;
}

// <span class="py">miàn<span class="tone"> · 4</span></span> (non-breaking spaces),
// the tone in its own span so narrow layouts can hide it; neutral tone gets none.
function pinyinSpan(syllable) {
  const span = el("span", "py", syllable);
  const tone = toneOf(syllable);
  if (tone) span.append(el("span", "tone", `\u00A0\u00B7\u00A0${tone}`));
  return span;
}

function render(idiom) {
  const content = document.getElementById("content");
  content.replaceChildren();
  document.title = idiom.chinese;

  const chars = [...idiom.chinese];
  const syllables = idiom.pinyin.split(/\s+/);
  const row = el("div", "idiom");
  row.lang = "zh";
  row.style.setProperty("--n", chars.length);
  chars.forEach((ch, i) => {
    const col = el("div", "char");
    col.append(pinyinSpan(syllables[i] || ""), el("span", "hz", ch));
    row.append(col);
  });
  row.setAttribute("aria-label", `${idiom.chinese} (${idiom.pinyin})`);

  if (IFRAME) {
    content.append(row);
    fitIframe();
    return;
  }

  const meaning = el("p", "meaning", idiom.meaning);
  meaning.lang = "zh";

  content.append(row, meaning, el("p", "translation", idiom.translation));

  if (idiom.explanation) content.append(el("p", "explanation", idiom.explanation));

  if (idiom.example) {
    const box = el("div", "example");
    const label = el("p", "label");
    label.append(el("span", "zh", "例句"), "Example");
    const zh = el("p", "zh-sentence");
    zh.lang = "zh";
    // Highlight the idiom inside the example sentence.
    idiom.example.split(idiom.chinese).forEach((part, i) => {
      if (i) zh.append(el("mark", null, idiom.chinese));
      zh.append(part);
    });
    box.append(label, zh, el("p", "en-sentence", idiom.example_translation));
    content.append(box);
  }
}

async function main() {
  const today = new Date();
  document.getElementById("date").textContent = today.toLocaleDateString("en-US", {
    weekday: "long", month: "long", day: "numeric", year: "numeric",
  });

  try {
    const res = await fetch(CSV_URL);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const idioms = parseCSV(await res.text());
    if (!idioms.length) throw new Error("no idioms found");
    render(idioms[pickForDay(dayNumber(today), idioms.length)]);
  } catch (err) {
    console.error(err);
    document.getElementById("content").replaceChildren(
      el("p", "status", "Couldn't load today's idiom. Serve this folder over HTTP (e.g. python3 -m http.server) rather than opening the file directly.")
    );
  }
}

main();
