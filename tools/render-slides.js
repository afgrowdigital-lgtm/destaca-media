// Renderiza slides HTML (1080x1350) para JPEG com as fontes da Destaca embutidas.
// Uso: npm i @fontsource/archivo@5.0.19 @fontsource/inter@5.0.18  (na pasta onde corres o script)
//      node render-slides.js <pasta-com-html> <pasta-de-saida> [LARGURAxALTURA]
//      Carrossel: 1080x1350 (por omissão). Story: 1080x1920.
// Nos HTML usa font-family "Archivo" e "Inter" sem <link> do Google Fonts (está bloqueado no ambiente).
// Para o logo usa o SVG inline descrito na skill destaca-carrosseis.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const [inDir, outDir, size = '1080x1350'] = process.argv.slice(2);
const [W, H] = size.split('x').map(Number);
if (!inDir || !outDir) { console.error('uso: node render-slides.js <in> <out>'); process.exit(1); }
const fontRoot = path.join(process.cwd(), 'node_modules', '@fontsource');
const face = (file, fam, w) =>
  `@font-face{font-family:${fam};font-weight:${w};src:url(data:font/woff2;base64,${fs.readFileSync(path.join(fontRoot, file)).toString('base64')}) format('woff2')}`;
const css = '<style>' +
  [500, 700, 800, 900].map(w => face(`archivo/files/archivo-latin-${w}-normal.woff2`, 'Archivo', w)).join('') +
  [400, 500, 600, 700].map(w => face(`inter/files/inter-latin-${w}-normal.woff2`, 'Inter', w)).join('') +
  'body{margin:0}</style>';

(async () => {
  fs.mkdirSync(outDir, { recursive: true });
  const files = fs.readdirSync(inDir).filter(f => f.endsWith('.html')).sort();
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: W, height: H } });
  for (const f of files) {
    let html = fs.readFileSync(path.join(inDir, f), 'utf8')
      .replace(/<link[^>]*fonts\.g[^>]*>/g, '');
    html = html.includes('</head>') ? html.replace('</head>', css + '</head>') : css + html;
    await page.setContent(html, { waitUntil: 'load' });
    await page.evaluate(() => document.fonts.ready);
    const out = path.join(outDir, f.replace(/\.html$/, '.jpg'));
    await page.screenshot({ path: out, type: 'jpeg', quality: 90, clip: { x: 0, y: 0, width: W, height: H } });
    console.log(out);
  }
  await browser.close();
})();
