# Web (mobile web, PWA, hybrid shells) — design ↔ code

Load when `product.stack: web`, or for Capacitor/Ionic shells and mobile-first web apps. For full marketing sites use Prismora; Kinetic covers app-like mobile surfaces.

## 1. Detect and read (code-to-design)

| Look at | Reveals |
|---|---|
| `:root { --… }` in global CSS, `tokens.css`, `theme.ts` | Custom properties = the palette/spacing system |
| `tailwind.config.*` / `@theme` block (Tailwind v4) | Colors, spacing, radius, font scale — check for untouched defaults |
| `index.html` `<meta name="viewport">`, `manifest.webmanifest` | `viewport-fit=cover`, `theme-color`, display mode |
| Components (`*.tsx`, `*.vue`, `*.svelte`) | Inline hex, `px` font sizes, arbitrary Tailwind values (`p-[13px]`), `box-shadow` stacks |

Run `kinetic dna src --json`, read the token source and 2–3 screens, fill KDL `audit`.

## 2. Token architecture

```css
:root {
  color-scheme: light dark;
  --k-bg: #F6F1EA; --k-surface: #FFFFFF; --k-text: #1E1A16; --k-text-2: #5C5249;
  --k-border: #E4DAD0; --k-accent: #8A5A2B; --k-on-accent: #FFFFFF; --k-danger: #B3261E;
  --k-space-xs: 4px; --k-space-s: 8px; --k-space-m: 12px; --k-space-l: 16px; --k-space-xl: 24px; --k-space-2xl: 32px;
  --k-radius-s: 8px; --k-radius-m: 14px; --k-radius-l: 22px;
  --k-ease-out: cubic-bezier(0.2, 0.8, 0.2, 1);
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --k-bg: #0F0D0B; --k-surface: #1A1714; --k-text: #EDE6DE; --k-text-2: #A89C90;
    --k-border: #2C2722; --k-accent: #D9A877; --k-on-accent: #1E1408; --k-danger: #F2B8B5;
  }
}
:root[data-theme="dark"] { /* same dark values, for an explicit toggle */ }
body { background: var(--k-bg); color: var(--k-text); }
```

- `oklch()` is widely supported in current browsers and makes ramps perceptual; keep hex fallbacks if old WebViews matter. `light-dark()` is an alternative to the media query when `color-scheme` is set — check target browser support.
- Type in `rem` so user font-size settings apply; KDL `track` em maps 1:1 to `letter-spacing: -0.02em`; `line-height` unitless (`44/40`).

```css
.k-display { font: 300 2.5rem/1.1 var(--k-font-display); letter-spacing: -0.02em; font-variant-numeric: tabular-nums; }
.k-body    { font: 400 1.0625rem/1.41 var(--k-font-text); }
```

## 3. Layout and responsive

- Safe areas: `<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">` then `padding: env(safe-area-inset-top) env(safe-area-inset-right) env(safe-area-inset-bottom) env(safe-area-inset-left)` where content meets edges.
- Viewport height: `100dvh` / `100svh` instead of `100vh` (mobile toolbars). Avoid fixed 100vh heroes (layout jumps).
- Keyboard: the `interactive-widget=resizes-content` viewport key changes resizing behaviour on supporting browsers — verify support; otherwise rely on scrollable containers and `scrollIntoView({ block: 'center' })` on focus.
- Never `maximum-scale=1` / `user-scalable=no` (F10 — blocks zoom).
- Targets: 44×44 px minimum for primary controls (WCAG 2.5.8 AA requires 24×24; 44 is the platform-grade target).
- Hover is not available on touch — no hover-only affordances (D23); use `@media (hover: hover)` for enhancements.
- Squircles: CSS `corner-shape` is new and not universally supported — verify; circular `border-radius` is acceptable.

## 4. Motion

Springs in CSS via `linear()` sampled from the KDL spring:

```js
// Generate a CSS linear() easing from KDL {response, damping}; duration = settle time
export function springToLinear(response, damping, samples = 40) {
  const w0 = (2 * Math.PI) / response, z = damping;
  const x = (t) => z < 1
    ? 1 - Math.exp(-z * w0 * t) * (Math.cos(w0 * Math.sqrt(1 - z * z) * t) + (z / Math.sqrt(1 - z * z)) * Math.sin(w0 * Math.sqrt(1 - z * z) * t))
    : 1 - Math.exp(-w0 * t) * (1 + w0 * t);
  const settle = Math.min(4 / (z * w0), 2);           // seconds to ~2% of the target
  const pts = Array.from({ length: samples + 1 }, (_, i) => x((i / samples) * settle).toFixed(4));
  return { easing: `linear(${pts.join(', ')})`, durationMs: Math.round(settle * 1000) };
}
```

Fallback: `cubic-bezier(0.2, 0.8, 0.2, 1)` (damped settle) for browsers without `linear()`.

- Transitions on `transform` and `opacity` first; animate layout properties only when measured cheap.
- Page/state morphs: View Transitions (`document.startViewTransition(() => update())`, `view-transition-name: card-42`) — progressive enhancement; check support.
- Reduce motion:

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; transition-duration: 0.01ms !important; scroll-behavior: auto !important; }
}
```

  Better: author decorative motion inside `@media (prefers-reduced-motion: no-preference)` and keep state feedback (color/opacity) outside it.

## 5. Haptics

The Vibration API (`navigator.vibrate`) is not supported in iOS Safari and is coarse elsewhere. Do not fake haptics; in Capacitor shells use the native Haptics plugin (`@capacitor/haptics`: `Haptics.impact({ style: ImpactStyle.Light })`, `Haptics.selectionChanged()`, `Haptics.notification({ type: NotificationType.Success })`) — verify the plugin version's API.

## 6. Accessibility

- Semantic elements first: `<button>`, `<a href>`, `<input>` + `<label>`, `<nav>`, `<main>`, headings in order.
- Icon-only: `<button aria-label="Delete entry">`; decorative SVG `aria-hidden="true"`.
- Focus visible: `:focus-visible { outline: 2px solid var(--k-accent); outline-offset: 2px; }` — never remove outlines without replacement.
- Live updates: `aria-live="polite"` for async results.

## 7. Native-like fidelity

- Respect platform expectations in shells: iOS back swipe, Android back button; avoid custom scroll physics.
- `-webkit-tap-highlight-color: transparent` only when a real pressed state replaces it.
- `overscroll-behavior: contain` on modal sheets; `touch-action` to avoid gesture conflicts.

## 8. Web-specific slop

| ID | Code signal | Fix |
|---|---|---|
| F02 | `href="#"`, `onClick={() => {}}` | Wire or remove |
| F07 | `<div onClick>` without role/keyboard; `outline: none` | `<button>`; focus styles |
| F10 | `user-scalable=no`, `maximum-scale=1`, `px` body text | Allow zoom; `rem` |
| D01 | `bg-gradient-to-r from-purple-500 to-blue-500` | Solid + accent |
| D05 | `backdrop-filter: blur()` on content cards | Tonal surface |
| D17 | Arbitrary values `p-[13px]`, `mt-[27px]` | Spacing scale |
| D23 | hover-only menus, `<table>` on phone | Touch-first patterns |
| D26 | `bg-clip-text text-transparent` gradient headings | Weight/size/color |
| D29 | `w-[375px]`, `h-screen` (100vh) frames | Fluid widths, `dvh` |

## 9. Verify

```bash
npx tsc --noEmit && npx eslint .
npx playwright test                     # if present
npx lighthouse http://localhost:5173 --preset=desktop --only-categories=accessibility,performance  # verify flags for your lighthouse version
```

Playwright screenshot matrix: viewports 320×568, 390×844, 430×932; `colorScheme: 'dark'`; `reducedMotion: 'reduce'`; 200% zoom (`deviceScaleFactor` is not zoom — set root font-size or use browser zoom). Run `@axe-core/playwright` on each state when available.
