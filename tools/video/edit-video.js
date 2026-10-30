// Edita um vídeo bruto da Destaca: legendas palavra a palavra + final animado da marca.
//
// Uso (na pasta onde instalaste as fontes, como no render-slides.js):
//   npm i @fontsource/archivo@5.0.19 @fontsource/inter@5.0.18
//   node <repo>/tools/video/edit-video.js <bruto.mp4> <config.json> <saida.mp4>
//
// config.json = o JSON do transcribe.py (já revisto) com campos opcionais:
//   "tipo": "reel" | "story"          (por omissão: >15 s = reel, senão story)
//   "fim": 7.9                        (corta o bruto neste segundo; omissão = vídeo todo)
//   "outro": { "titulo": "Aparece <em>primeiro</em> no Google.",
//              "sub": "Sites de apresentação e SEO local, feitos à medida do teu negócio.",
//              "cta": "Fala connosco" }   (<em> = palavra a laranja)
//   "sem_legendas": true              (se o bruto já vier legendado)
// Gera também <saida>-capa.jpg (frame do meio com legenda) para usar como capa do Reel.
const { chromium } = require('playwright');
const { execFileSync } = require('child_process');
const fs = require('fs');
const os = require('os');
const path = require('path');

const [src, cfgPath, out] = process.argv.slice(2);
if (!src || !cfgPath || !out) { console.error('uso: node edit-video.js <bruto.mp4> <config.json> <saida.mp4>'); process.exit(1); }
const cfg = JSON.parse(fs.readFileSync(cfgPath, 'utf8'));
const W = 1080, H = 1920, FPS = 30, OUTRO = 2.0;
const ff = (args) => execFileSync('ffmpeg', ['-v', 'error', '-y', ...args], { stdio: 'inherit' });
const probe = (f) => parseFloat(execFileSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f]).toString());

const rawDur = probe(src);
const dur = Math.min(cfg.fim || rawDur, rawDur);
const tipo = cfg.tipo || (dur + OUTRO > 15 ? 'reel' : 'story');
const outro = Object.assign({
  titulo: 'Aparece <em>primeiro</em> no Google.',
  sub: 'Sites de apresentação e SEO local, feitos à medida do teu negócio.',
  cta: tipo === 'story' ? 'Manda SITE por mensagem' : 'Fala connosco',
}, cfg.outro || {});

// ---------- fontes ----------
const fontRoot = path.join(process.cwd(), 'node_modules', '@fontsource');
const face = (file, fam, w) =>
  `@font-face{font-family:${fam};font-weight:${w};src:url(data:font/woff2;base64,${fs.readFileSync(path.join(fontRoot, file)).toString('base64')}) format('woff2')}`;
const FONTS = [700, 800, 900].map(w => face(`archivo/files/archivo-latin-${w}-normal.woff2`, 'Archivo', w)).join('') +
  [400, 500, 700].map(w => face(`inter/files/inter-latin-${w}-normal.woff2`, 'Inter', w)).join('');
const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;');

// ---------- legendas: agrupar palavras em blocos curtos ----------
const words = (cfg.words || []).filter(w => w.s < dur);
const chunks = [];
let cur = [];
for (const w of words) {
  const len = cur.map(x => x.w).join(' ').length + w.w.length;
  const gap = cur.length ? w.s - cur[cur.length - 1].e : 0;
  if (cur.length && (cur.length >= 3 || len > 18 || gap > 0.45)) { chunks.push(cur); cur = []; }
  cur.push(w);
  if (/[.,!?;:]$/.test(w.w)) { chunks.push(cur); cur = []; }
}
if (cur.length) chunks.push(cur);
const lastWord = words[words.length - 1];

// estados: [inicio, fim, html]
const states = [];
chunks.forEach((c, ci) => {
  const next = chunks[ci + 1];
  const end = Math.min(next ? next[0].s : dur, c[c.length - 1].e + 0.6, dur);
  c.forEach((w, wi) => {
    const s = wi === 0 ? c[0].s : w.s;
    const e = wi + 1 < c.length ? c[wi + 1].s : end;
    const html = c.map((x, xi) => {
      if (xi !== wi) return `<span>${esc(x.w)}</span>`;
      return (x === lastWord || /[.!?]$/.test(x.w)) ? `<span class="box">${esc(x.w)}</span>` : `<span class="on">${esc(x.w)}</span>`;
    }).join(' ');
    if (e > s) states.push([s, e, html]);
  });
});

// Logo da Destaca por cima da marca de água do Gemini (canto inferior direito).
// Posição por omissão medida nos vídeos do Gemini/Veo 1080x1920; ajustável com "logo": {"x":910,"y":1768,"tam":128}
// (x,y = centro). "logo": false desliga.
const LOGO_SVG = (s) => `<svg viewBox="0 0 844 845" width="${s}" height="${s}"><rect width="844" height="845" fill="#FF7A1F"/><circle cx="355" cy="517" r="146" fill="none" stroke="#050F16" stroke-width="93"/><rect x="455" y="147" width="92" height="516" fill="#050F16"/><rect x="620" y="570" width="92" height="92" fill="#050F16"/></svg>`;
const lg = cfg.logo === false ? null : Object.assign({ x: 910, y: 1768, tam: 128 }, cfg.logo || {});
const logoHtml = lg ? `<div style="position:absolute;left:${lg.x - lg.tam / 2}px;top:${lg.y - lg.tam / 2}px;width:${lg.tam}px;height:${lg.tam}px;line-height:0;box-shadow:0 4px 18px rgba(5,15,22,.35)">${LOGO_SVG(lg.tam)}</div>` : '';

const capPage = (inner) => `<html><head><style>${FONTS}
body{margin:0;width:${W}px;height:${H}px;background:transparent}
.cap{position:absolute;left:90px;right:90px;top:1240px;transform:translateY(-50%);text-align:center;
font-family:Archivo;font-weight:900;font-size:84px;line-height:1.14;letter-spacing:-0.02em;color:#FFF4EA;
text-shadow:0 3px 6px rgba(5,15,22,.55),0 6px 28px rgba(5,15,22,.55)}
.on{color:#FF7A1F}.box{background:#FF7A1F;color:#050F16;padding:0 14px;text-shadow:none;box-decoration-break:clone;-webkit-box-decoration-break:clone}
</style></head><body>${inner ? `<div class="cap">${inner}</div>` : ''}${logoHtml}</body></html>`;

const outroPage = () => `<html><head><style>${FONTS}
*{box-sizing:border-box}body{margin:0;width:${W}px;height:${H}px;background:#050F16;overflow:hidden;position:relative;font-family:Inter;color:#FFF4EA}
@keyframes wipe{from{transform:scale(1)}to{transform:scale(0)}}
@keyframes up{from{opacity:0;transform:translateY(40px)}to{opacity:1;transform:none}}
@keyframes fade{from{opacity:0}to{opacity:1}}
.wipe{position:absolute;inset:0;background:#FF7A1F;transform-origin:0 0;animation:wipe .4s cubic-bezier(.7,0,.3,1) both;z-index:5}
.ring{position:absolute;width:640px;height:640px;border:110px solid #10232F;border-radius:50%;right:-250px;top:-250px;animation:fade .5s .2s both}
.sq{position:absolute;width:110px;height:150px;background:#FF7A1F;right:0;top:1520px}
.wrap{position:absolute;left:110px;right:110px;top:560px}
.a{animation:up .45s cubic-bezier(.2,.7,.2,1) both}
.logo{display:flex;align-items:center;gap:24px;animation-delay:.3s}
.logo span{font-family:Archivo;font-weight:800;font-size:34px;letter-spacing:.22em;color:#FF7A1F}
h1{margin:64px 0 0;font-family:Archivo;font-weight:900;font-size:128px;line-height:1.0;letter-spacing:-0.035em;animation-delay:.42s}
h1 em{font-style:normal;color:#FF7A1F}
p{margin:44px 0 0;font-size:40px;line-height:1.4;color:#C3CBD0;max-width:800px;animation-delay:.6s}
.cta{display:inline-block;margin-top:110px;background:#FF7A1F;color:#050F16;font-family:Archivo;font-weight:800;font-size:42px;padding:24px 40px;animation-delay:.74s}
.hd{margin-top:40px;font-family:Archivo;font-weight:700;font-size:36px;animation-delay:.86s}.hd b{color:#FF7A1F;font-weight:700}
</style></head><body>
<div class="ring"></div><div class="sq"></div>
<div class="wrap">
 <div class="a logo"><svg viewBox="0 0 844 845" width="96" height="96"><rect width="844" height="845" fill="#FF7A1F"/><circle cx="355" cy="517" r="146" fill="none" stroke="#050F16" stroke-width="93"/><rect x="455" y="147" width="92" height="516" fill="#050F16"/><rect x="620" y="570" width="92" height="92" fill="#050F16"/></svg><span>DESTACA</span></div>
 <h1 class="a">${outro.titulo}</h1>
 <p class="a">${esc(outro.sub)}</p>
 <div class="a cta">${esc(outro.cta)} →</div>
 <div class="a hd"><b>@destacasite</b> · destaca.site</div>
</div>
<div class="wipe"></div></body></html>`;

(async () => {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'destaca-video-'));
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: W, height: H } });

  // 1) PNGs das legendas + lista de concat
  const list = [];
  const shot = async (html, name) => {
    await page.setContent(html, { waitUntil: 'load' });
    await page.evaluate(() => document.fonts.ready);
    const f = path.join(tmp, name);
    await page.screenshot({ path: f, omitBackground: true });
    return f;
  };
  const blank = await shot(capPage(''), 'blank.png');
  if (cfg.so_logo) await browser.close();
  const norm = `scale=${W}:${H}:force_original_aspect_ratio=increase,crop=${W}:${H},fps=${FPS},setsar=1`;
  // Modo "so_logo": o vídeo já vem editado (legendas + final). Só põe o logo por cima da marca
  // do Gemini até "logo_ate" segundos (omissão: vídeo todo) e mantém o resto.
  if (cfg.so_logo) {
    const ate = cfg.logo_ate || rawDur;
    ff(['-i', src, '-i', blank, '-filter_complex',
      `[0:v]${norm}[b];[b][1:v]overlay=0:0:enable='lt(t,${ate})',format=yuv420p[v]`,
      '-map', '[v]', '-map', '0:a?', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-profile:v', 'high',
      '-c:a', 'aac', '-b:a', '160k', '-ar', '48000', '-movflags', '+faststart', out]);
    const capa = out.replace(/\.mp4$/, '') + '-capa.jpg';
    ff(['-ss', String((rawDur * 0.4).toFixed(2)), '-i', out, '-frames:v', '1', '-q:v', '3', capa]);
    fs.rmSync(tmp, { recursive: true, force: true });
    console.log(JSON.stringify({ out, capa, tipo: cfg.tipo || (rawDur > 15 ? 'reel' : 'story'), duracao: +rawDur.toFixed(2) }));
    return;
  }

  let t = 0, i = 0;
  const states2 = cfg.sem_legendas ? [] : states;
  for (const [s, e, html] of states2) {
    if (s > t + 0.01) list.push([blank, s - t]);
    const f = await shot(capPage(html), `c${String(i++).padStart(4, '0')}.png`);
    list.push([f, e - Math.max(s, t)]);
    t = e;
  }
  if (dur > t) list.push([blank, dur - t]);
  const concat = list.map(([f, d]) => `file '${f}'\nduration ${d.toFixed(3)}`).join('\n') + `\nfile '${list[list.length - 1][0]}'\n`;
  fs.writeFileSync(path.join(tmp, 'caps.txt'), concat);

  // 2) frames do final
  await page.setContent(outroPage(), { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  const nOut = Math.round(OUTRO * FPS);
  for (let k = 0; k < nOut; k++) {
    await page.evaluate((ms) => document.getAnimations().forEach(a => { a.pause(); a.currentTime = ms; }), (k / FPS) * 1000);
    await page.screenshot({ path: path.join(tmp, `o${String(k).padStart(3, '0')}.png`) });
  }
  await browser.close();

  // 3) montagem
  ff(['-i', src, '-f', 'concat', '-safe', '0', '-i', path.join(tmp, 'caps.txt'),
    '-framerate', String(FPS), '-i', path.join(tmp, 'o%03d.png'),
    '-f', 'lavfi', '-t', String(OUTRO), '-i', 'anullsrc=r=48000:cl=stereo',
    '-filter_complex',
    `[0:v]trim=0:${dur},setpts=PTS-STARTPTS,${norm}[v0];` +
    `[1:v]fps=${FPS},format=rgba,setpts=PTS-STARTPTS[cap];` +
    `[v0][cap]overlay=0:0:shortest=0:eof_action=pass,format=yuv420p[vm];` +
    `[2:v]${norm},format=yuv420p[vo];` +
    `[0:a]atrim=0:${dur},asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo,afade=t=out:st=${Math.max(0, dur - 0.25)}:d=0.25[am];` +
    `[vm][am][vo][3:a]concat=n=2:v=1:a=1[v][a]`,
    '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-profile:v', 'high',
    '-pix_fmt', 'yuv420p', '-r', String(FPS), '-c:a', 'aac', '-b:a', '160k', '-ar', '48000', '-movflags', '+faststart', out]);

  // 4) capa (frame com legenda a ~40% do vídeo)
  const capa = out.replace(/\.mp4$/, '') + '-capa.jpg';
  ff(['-ss', String((dur * 0.4).toFixed(2)), '-i', out, '-frames:v', '1', '-q:v', '3', capa]);
  fs.rmSync(tmp, { recursive: true, force: true });
  console.log(JSON.stringify({ out, capa, tipo, duracao: +(dur + OUTRO).toFixed(2) }));
})();
