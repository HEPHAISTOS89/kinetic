// Render harness — do not modify.
// Usage (from your project directory):  node <HARNESS>/render.mjs [--typecheck-only]
// 1. Type-checks every .ts/.tsx file in the project against React Native 0.81 types.
// 2. Bundles Gallery.tsx with react-native-web and renders every gallery entry at
//    393×852pt (device scale 2, safe-area insets top 47 / bottom 34), light and dark,
//    into ./shots/<name>-<light|dark>.png (Chromium, prefers-color-scheme emulated).
import { build } from 'esbuild';
import { chromium } from 'playwright-core';
import { execFileSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HARNESS = path.dirname(fileURLToPath(import.meta.url));
const NM = path.join(HARNESS, 'node_modules');
const PROJECT = process.cwd();
const OUT = path.join(PROJECT, 'shots');
const W = 393, H = 852;

function typecheck() {
  const files = [];
  const walk = (d) => {
    for (const e of fs.readdirSync(d, { withFileTypes: true })) {
      if (['node_modules', 'shots', '.render', '.kinetic', '.git'].includes(e.name)) continue;
      const p = path.join(d, e.name);
      if (e.isDirectory()) walk(p);
      else if (/\.(tsx?)$/.test(e.name) && !e.name.endsWith('.d.ts')) files.push(p);
    }
  };
  walk(PROJECT);
  const cfg = {
    compilerOptions: {
      target: 'ES2022', module: 'ESNext', moduleResolution: 'bundler', jsx: 'react-jsx',
      strict: true, noEmit: true, skipLibCheck: true, esModuleInterop: true,
      baseUrl: PROJECT, typeRoots: [path.join(NM, '@types')], types: ['react'],
      paths: { '*': [path.join(NM, '@types', '*'), path.join(NM, '*')] },
    },
    files: [...files, path.join(NM, 'react-native', 'types', 'index.d.ts')],
  };
  fs.mkdirSync(path.join(PROJECT, '.render'), { recursive: true });
  const cfgPath = path.join(PROJECT, '.render', 'tsconfig.json');
  fs.writeFileSync(cfgPath, JSON.stringify(cfg, null, 2));
  try {
    execFileSync(process.execPath, [path.join(NM, 'typescript', 'bin', 'tsc'), '-p', cfgPath], { stdio: 'inherit' });
    console.log(`typecheck: OK (${files.length} files)`);
  } catch {
    console.error('typecheck: FAILED');
    process.exit(1);
  }
}

async function bundle() {
  const fontsDir = path.join(PROJECT, 'fonts');
  const fonts = fs.existsSync(fontsDir)
    ? fs.readdirSync(fontsDir).filter((f) => /\.(ttf|otf)$/i.test(f)) : [];
  const fontCss = fonts.map((f) => `@font-face{font-family:"${f.replace(/\.(ttf|otf)$/i, '')}";src:url("../fonts/${f}");}`).join('\n');
  const entry = path.join(PROJECT, '.render', 'entry.jsx');
  fs.writeFileSync(entry, `
import React from 'react';
import { createRoot } from 'react-dom/client';
import { SafeAreaInsetsContext, SafeAreaFrameContext } from 'react-native-safe-area-context';
import { gallery } from '../Gallery';
const metrics = { frame: { x: 0, y: 0, width: ${W}, height: ${H} }, insets: { top: 47, bottom: 34, left: 0, right: 0 } };
window.__names = gallery.map(([n]) => n);
window.__render = (i) => {
  const C = gallery[i][1];
  createRoot(document.getElementById('root')).render(
    <SafeAreaFrameContext.Provider value={metrics.frame}>
      <SafeAreaInsetsContext.Provider value={metrics.insets}><C /></SafeAreaInsetsContext.Provider>
    </SafeAreaFrameContext.Provider>);
};`);
  await build({
    entryPoints: [entry], bundle: true, outfile: path.join(PROJECT, '.render', 'bundle.js'),
    format: 'iife', platform: 'browser', target: 'es2022', jsx: 'automatic', logLevel: 'error',
    nodePaths: [NM], alias: { 'react-native': 'react-native-web' },
    resolveExtensions: ['.web.tsx', '.web.ts', '.web.jsx', '.web.js', '.tsx', '.ts', '.jsx', '.js', '.json'],
    mainFields: ['browser', 'module', 'main'],
    loader: { '.js': 'jsx', '.png': 'dataurl', '.jpg': 'dataurl', '.svg': 'text' },
    define: { __DEV__: 'false', 'process.env.NODE_ENV': '"production"', global: 'window' },
  });
  fs.writeFileSync(path.join(PROJECT, '.render', 'index.html'), `<!doctype html><html><head><meta charset="utf-8">
<style>${fontCss}
html,body{margin:0;padding:0;width:${W}px;height:${H}px;overflow:hidden}
#root{width:${W}px;height:${H}px;display:flex;overflow:hidden}</style></head>
<body><div id="root"></div><script src="bundle.js"></script></body></html>`);
}

function chromePath() {
  const candidates = ['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'];
  const pw = path.join(process.env.HOME, 'Library/Caches/ms-playwright');
  if (fs.existsSync(pw)) for (const d of fs.readdirSync(pw).filter((d) => d.startsWith('chromium-')).sort().reverse())
    candidates.push(path.join(pw, d, 'chrome-mac/Chromium.app/Contents/MacOS/Chromium'),
      path.join(pw, d, 'chrome-mac-arm64/Chromium.app/Contents/MacOS/Chromium'));
  return candidates.find((c) => fs.existsSync(c));
}

async function render() {
  fs.mkdirSync(OUT, { recursive: true });
  const browser = await chromium.launch({ executablePath: chromePath(), headless: true });
  const url = 'file://' + path.join(PROJECT, '.render', 'index.html');
  let errors = 0, count = 0;
  for (const scheme of ['light', 'dark']) {
    const ctx = await browser.newContext({ viewport: { width: W, height: H }, deviceScaleFactor: 2, colorScheme: scheme });
    const page = await ctx.newPage();
    page.on('pageerror', (e) => { errors++; console.error(`[${scheme}] page error: ${e.message}`); });
    page.on('console', (m) => { if (m.type() === 'error') console.error(`[${scheme}] console: ${m.text()}`); });
    await page.goto(url);
    const names = await page.evaluate(() => window.__names);
    for (let i = 0; i < names.length; i++) {
      await page.goto(url);
      await page.evaluate((i) => window.__render(i), i);
      await page.evaluate(() => document.fonts.ready);
      await page.waitForTimeout(250);
      await page.screenshot({ path: path.join(OUT, `${names[i]}-${scheme}.png`) });
      count++;
    }
    await ctx.close();
  }
  await browser.close();
  console.log(`rendered ${count} images into ./shots${errors ? ` (${errors} page errors)` : ''}`);
}

typecheck();
if (!process.argv.includes('--typecheck-only')) { await bundle(); await render(); }
