# Smart Hire — web rebuild

Production HTML/Tailwind/SCSS/JS rebuild of the `design_files/` hi-fi handoff (see `../README.md` for the original design spec). 26 screens: auth, customer (8), provider (5), admin (5), mobile (5), plus the design-system reference page.

## Stack

- **Eleventy** — Nunjucks templates + macros compile to flat static `.html` pages (`src/pages/**` → `_site/**`). Shared chrome (topnav, sidebar shell, mobile phone frame, icon set, buttons/chips/cards/etc.) lives in `src/_includes/macros/*.njk` so it isn't hand-duplicated across 26 files.
- **SCSS** (`src/scss/`) — the design-system component layer, ported from the handoff's `ds.css` tokens (colors, type scale, buttons, chips, cards, nav, stepper, etc.). Compiles to `_site/assets/css/main.css`.
- **Tailwind** (`src/css/tailwind.css` + `tailwind.config.js`) — utility classes for one-off layout, plus the brand palette/fonts exposed as Tailwind theme tokens. Compiles to `_site/assets/css/tailwind.css`.
- **Vanilla JS** (`src/js/`) — no framework. `main.js` (chip groups, toggle buttons) loads everywhere; `auth.js`, `booking.js`, `review.js`, `queue.js` load only on the pages that need them (see each page's front-matter `extraScripts`).

## Commands

```
npm install
npm run build   # one-shot production build → _site/
npm run dev     # eleventy + sass + tailwind, all in watch mode, in parallel
```

`npm run dev` does **not** serve the site — pair it with any static server pointed at `_site/`, e.g. `npx serve _site` or `python3 -m http.server -d _site`.

## Structure

```
src/
  _data/            cats.js, pros.js, icons.js — shared mock data + icon paths
  _includes/
    layouts/        base.njk (HTML shell), customer.njk (topnav wrapper)
    macros/         ds.njk (buttons/chips/cards/etc.), shell.njk (provider/admin sidebar+topbar), mobile.njk (phone frame)
    partials/       auth-content.njk (shared login/register markup)
  scss/             design tokens + component CSS, one partial per component family
  css/              tailwind.css entry (@tailwind directives only)
  js/               per-feature vanilla JS modules
  pages/            one .html per screen, organized by section (auth/, customer/, provider/, admin/, mobile/)
```

## Notes for whoever picks this up

- Internal links are flat `.html` paths (`/customer/home.html`), not Eleventy's default pretty-URL directories — see the `eleventyComputed.permalink` override in `.eleventy.js`. Keep writing links that way.
- `bodyClass: frame` in a page's front matter makes the body fill the viewport with `overflow: hidden` so the sidebar/topbar stay fixed while `.content` scrolls independently (used on provider/admin dashboards and implicitly by the mobile phone frame). Omit it for pages that should scroll normally (customer marketing-ish pages, auth).
- A few nav targets fall back to the nearest real page because the original handoff didn't design a dedicated screen for them (e.g. mobile's "Browse" tab reuses the desktop `/customer/browse.html`, "Account" falls back to home) — see `mobileTabbar` in `macros/ds.njk`.

## Responsive behavior

The handoff itself was fixed-width desktop screens plus a separate 390×844 mobile reference set (see the original `README.md`). This rebuild makes the *desktop* screens genuinely responsive too, in `src/scss/_responsive.scss`:

- **Customer topnav** collapses its links into a hamburger panel below 760px (`nav.js` + `[data-nav-toggle]` / `[data-nav-panel]`).
- **Provider/admin sidebar** becomes an off-canvas drawer below 860px, opened via a hamburger in the topbar (`[data-menu-toggle]` / `[data-sidebar]` / `[data-sidebar-backdrop]`), and `bodyClass: frame`'s fixed-viewport app-shell behavior is disabled below that same breakpoint so the page just scrolls normally.
- **Auth split screen** drops the dark brand panel below 760px; the form card goes full-width.
- **Two-column layouts** (booking summary, filter sidebars, profile preview rails, etc.) use a `.rail` class that collapses the fixed-width column to `width:100%` and un-stickies it below 860px — pair it with `.grow` on the sibling (already the default everywhere) so both stack cleanly.
- **Grids** use `.grid-2` / `.grid-3` / `.grid-4` / `.grid-6` classes (not raw inline `grid-template-columns`) so column counts step down at 860px/560px automatically.
- Any row of chips/buttons that can overflow on a narrow phone needs the `wrap` class — this bit us during testing (see below), so when adding new rows of inline controls, default to including it.

**Verifying no regressions**: there's no CI for this yet. The fastest way to catch a new fixed-width leak is a scripted check — build, serve `_site/`, then in a headless browser at 375/768/1280px widths assert `document.documentElement.scrollWidth <= clientWidth` on every page. That's how the current responsive pass was validated (an off-canvas drawer, a topbar with page-specific controls, and one specificity bug where a class-based `.col.center` selector accidentally matched two unrelated elements were all caught this way, not by eyeballing screenshots).

## Backend integration (Python)

Run `npm run build` and hand off the `_site/` directory — it's plain, flat HTML/CSS/JS with no template syntax left in it. Point Flask/Django/FastAPI's static file serving at it (or copy the `.html` files straight into a `templates/` folder — the markup has no Nunjucks tags left post-build, so it's safe to re-template later if you want server-side rendering instead of static files).

**Forms** — all real `<form>` submissions in the site (there are 4; everything else is JS-driven buttons/chips, not a submit):

| Page | Action | Method | Notes |
|---|---|---|---|
| `auth/login.html` | `/api/auth/login` | POST | fields: `email`, `password`, `remember` (checkbox), `role` (hidden, kept in sync with the customer/provider/admin tab by `auth.js`) |
| `auth/register.html` | `/api/auth/register` | POST | fields: `name`, `email`, `password`, `terms`, `role` (hidden, same as login), plus `trade`/`area` (provider) or `invite` (admin) — those two blocks are only visible for their role but still submit if left in the DOM, so ignore fields that don't match the submitted `role` |
| `provider/add-service.html` | `/api/provider/services` | POST | fields: `title`, `category`, `subcategory`, `description`, `price_model`, `rate`, `duration` |
| `customer/review.html` | `/api/reviews` | POST | fields: `overall_rating`, `rating_quality`, `rating_punctuality`, `rating_value`, `rating_comm` + free-text/chip fields — no booking id is wired in yet since the static demo has no session, add one (hidden input or route param) when you integrate |

The AI search boxes (`customer/home.html`, `mobile/home.html`) submit `GET` with a single `q` field straight to `/customer/ai-result.html` / `/mobile/result.html` — left as-is since a query-string GET to a server-rendered results page is the natural shape once those pages are driven by a real search endpoint instead of the mock data below.

**Mock data to replace** — `src/_data/cats.js` (service categories) and `src/_data/pros.js` (provider cards) are baked into the HTML at build time via Eleventy. There's no client-side fetch anywhere; every listing/grid/dashboard number you see is static demo content compiled in. Once real endpoints exist, either re-point those two files at your API during the Eleventy build, or (simpler, no rebuild needed per request) add `fetch()` calls in `src/js/` and swap the server-rendered placeholders for JS-populated containers.
