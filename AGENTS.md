# AGENTS.md

Guidance for AI agents (and humans) working in this repo.

## What this repo is

`talks.gkt.sh` is George K. Thiruvathukal's talks site: a GitHub Pages
site (see `CNAME`) that hosts a landing page plus one self-contained
reveal.js deck per talk, each living in its own top-level directory.

```
talks.gkt.sh/
├── index.html                    # landing page (card grid of talks)
├── theme.js                      # shared light/dark toggle, loaded by every page
├── CNAME                         # GitHub Pages custom domain
└── luc-digital-ethics-2026/      # one talk = one self-contained deck
    ├── index.html                #   the deck itself (markdown slides inline)
    ├── serve.sh                  #   local dev server for this deck
    ├── README.md                 #   talk-specific notes (sourcing, structure, gaps)
    ├── images/                   #   images used by this deck only
    └── reveal/                   #   vendored reveal.js (dist/ + plugin/)
```

Each talk directory is deliberately self-contained (own vendored
reveal.js, own images, own `serve.sh`) so it can be presented offline,
zipped up, or split into its own repo without touching anything else.

## The landing page (`index.html` at repo root)

- A plain static HTML page — no build step, no framework.
- Renders a grid of `.card` links, one per talk, each with a year,
  title, one-line description, and a "View talk →" call to action.
- Below each card, an `.entry__event` link points at the venue/event
  page for that talk (conference, symposium, etc.).
- To add a new talk: create its top-level deck directory (see below),
  then add one `.entry` block to `.cards` in `index.html` linking to
  `<deck-dir>/`.
- Loads `theme.js` for the light/dark toggle (see next section).

## Light/dark theming (`theme.js`)

- One shared script, loaded by both the landing page and every deck
  (`<script src="../theme.js">` from inside a deck directory).
- Stores an explicit user choice in `localStorage` under `gkt-theme`
  (`"light"` | `"dark"`); with no explicit choice it falls back to
  `prefers-color-scheme`.
- Since the landing page and every deck are served from the same
  origin, a theme choice made anywhere applies everywhere.
- Mounts a floating circular toggle button (`.gkt-theme-toggle`) and
  sets `data-theme` on `<html>`, which pages key their CSS custom
  properties off of. Also calls `Reveal.sync()` after a toggle so an
  open deck re-renders immediately.
- Each page defines its own `--bg`, `--ink`, `--accent`, etc. as CSS
  custom properties under `:root` (default/dark) and again under a
  `@media (prefers-color-scheme: light)` guard plus a
  `:root[data-theme="..."]` override — `theme.js` only flips the
  attribute, it doesn't own the palette.

## How a deck is built (reveal.js, markdown-in-HTML)

Each deck is a single `index.html` using [reveal.js](https://revealjs.com):

- **Vendored, not fetched**: `reveal/dist/` (`reveal.js`/`reveal.css`
  plus themes) and `reveal/plugin/` (`markdown/`, `notes/`, etc.) are
  copied into the deck directory, so the deck has zero network
  dependencies — it works offline and on unreliable conference Wi-Fi.
- **Slides are Markdown**, written inline inside one
  `<section data-markdown><textarea data-template>...</textarea></section>`
  block in `index.html`, not separate files. Horizontal slides are
  separated by a line containing only `---`; vertical slides (if used)
  by `--`; speaker notes start at a line beginning `Note:`. These
  separators are configured via `data-separator*` attributes on the
  `<section>` — see the top of `luc-digital-ethics-2026/index.html`.
- **Speaker notes** live under `Note:` in the same slide and are shown
  via the Notes plugin (press <kbd>S</kbd>) — used here to carry
  sourcing/argument detail that doesn't belong on-slide.
- **Styling**: a `<style>` block in `<head>` defines the deck's color
  palette as CSS custom properties (dark-first, with a light override),
  plus small helper classes used throughout the markdown
  (`.lead`, `.chapter-tag`, `.cols`, `.small`, `img.shot`, etc.).
  Swap `--accent`/`--accent2` to retheme a deck without touching slide
  content.
- **Plugins loaded**: `RevealMarkdown` and `RevealNotes` only, wired up
  in the `Reveal.initialize({...})` call at the bottom of the file.
  Add other vendored plugins (highlight, math, zoom, search, ...) the
  same way if a future deck needs them — `reveal/plugin/` already
  ships several unused ones.
- To start a new deck, copy an existing talk directory (index.html,
  reveal/, serve.sh, images/) as a template and edit the markdown,
  palette, and images for the new talk.

## Viewing a deck locally (`serve.sh`)

Each deck directory has its own `serve.sh`, run from inside that
directory:

```bash
cd luc-digital-ethics-2026
./serve.sh          # serves this folder on :8000, opens it in the browser
./serve.sh 8080      # choose a different port
./serve.sh --pdf     # opens the ?print-pdf view, for exporting to PDF
```

It's a thin wrapper around `python3 -m http.server`, bound to
`localhost` and rooted at the deck's own directory (not the repo
root) — this matters because the deck references `reveal/` and
`images/` with paths relative to itself, and `../theme.js` relative to
the repo root one level up. Serving from the wrong directory breaks
those relative paths. Requires `python3` on `PATH`; no other tooling
or install step is needed.

Useful keys once the deck is open: <kbd>S</kbd> speaker view/notes,
<kbd>Esc</kbd>/<kbd>O</kbd> overview map, <kbd>F</kbd> fullscreen,
arrows/space to navigate.

## Source material: the CHOC book

The `luc-digital-ethics-2026` deck is drawn from *History of Computing
and Its Cultures: From Calculating to Convergence* (in press,
2026–2027) by David B. Dennis and George K. Thiruvathukal — referred to
as "CHOC" in that deck's README and in the deck's `.chapter-tag`
annotations, which cite the specific book section each slide draws on.

The book's own repo is a sibling project, not part of this site:

- `../choc-book` locally (relative to this repo's parent directory)
- `git@github.com:ZettelGeist/choc-book.git` — currently private,
  pending publication alongside the book

That deck's `images/` directory is a **frozen snapshot** copied from
`choc-book/images/`, not a live link — if the book's source images are
revised, re-copy the relevant files by hand; there is no automated
sync. Image attributions live in each slide's `<figcaption>`, matching
the book's own credit lines.

When building a new deck from another part of CHOC (or from a
different source project), follow the same pattern: vendor a frozen
copy of whatever images are needed into that deck's own `images/`,
and note the source and copy date in that deck's README.

## Conventions when adding or editing a deck

- Keep each deck fully self-contained — don't share `reveal/` or
  `images/` across deck directories; copy instead of symlinking, so
  a deck can still be zipped up or split into its own repo.
- Give every deck its own `README.md` (see
  `luc-digital-ethics-2026/README.md` for the expected shape): what
  the talk covers, how it's structured, sourcing/attribution notes,
  and any known gaps.
- Give every deck its own `serve.sh` (copy the existing one verbatim —
  it's generic, not talk-specific).
- Reuse `../theme.js` rather than duplicating the toggle logic; add
  new CSS custom properties to a deck's palette instead of hardcoding
  colors so the light/dark toggle keeps working.
