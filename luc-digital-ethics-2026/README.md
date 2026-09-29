# From Disruption to Agency

A self-contained [reveal.js](https://revealjs.com) deck for the 40-minute digital-ethics talk
drawn from *History of Computing and Its Cultures: From Calculating to Convergence* (in press
for 2026–2027), by David B. Dennis and George K. Thiruvathukal (speaker). "CHOC" below refers
to that book.

Styled to match the `unreal-demo` NetTwin deck (dark theme, single accent color, markdown
slides, minimal chrome) — see that project's `docs/presentation/` for the shared structural
pattern. This deck uses a warm amber/sage palette instead of NetTwin's blue/green, since the
subject is history and culture rather than a supercomputer visualization; swap the `--accent`
and `--accent2` variables in `index.html` to match if brand consistency across talks is wanted.

- `index.html` — the deck. Slides are written in Markdown inside the file.
- `reveal/` — vendored reveal.js (originally copied from `unreal-demo/docs/presentation/reveal/`),
  so the deck works offline / on conference Wi-Fi with no network fetches.
- `images/` — local copies of the 21 CHOC illustrations this deck uses, originally copied from
  the `choc-book` repo's `images/` directory. This is a frozen snapshot, not a live link: if
  CHOC's own images are later revised, these copies won't update automatically — re-copy the
  relevant files from `choc-book/images/` by hand if that happens. Attributions for every image
  stay in each slide's `<figcaption>`, unchanged from the book's own credit lines. It also holds
  `qr-talk.svg`/`qr-keylinks.svg` (used by `index.html`) and `qr-talk.png`/`qr-keylinks.png`
  (used by `talk.tex`/`build_pptx.py`) — QR codes to this talk's URL and the speaker's keylinks
  page, generated locally with the Python `qrcode` package rather than fetched from a network
  service, keeping the deck's no-network-dependency property. To regenerate after a URL changes,
  run (after `pip install qrcode[pil]`):
  ```python
  import qrcode
  import qrcode.image.svg as svg

  URLS = {"qr-talk": "https://talks.gkt.sh/luc-digital-ethics-2026/",
          "qr-keylinks": "https://keylinks.gkt.sh"}

  for name, url in URLS.items():
      png = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=20, border=2)
      png.add_data(url); png.make(fit=True)
      png.make_image(fill_color="black", back_color="white").save(f"images/{name}.png")

      vec = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=10,
                           border=2, image_factory=svg.SvgPathFillImage)
      vec.add_data(url); vec.make(fit=True)
      vec.make_image().save(f"images/{name}.svg")
  ```

This repo is the standalone home for the talk — it was split out of `choc-book` (a peer
directory) so it can be presented, zipped, or pushed to its own remote independent of the book's
repo.

## Archival print version (LaTeX/Beamer)

`talk.tex` is a hand-kept Beamer edition of the same 35 slides, for a citable, easy-to-render
PDF (e.g. to accompany the [figshare DOI](https://doi.org/10.6084/m9.figshare.33944386) linked
from the title slide) independent of a browser or reveal.js. It reuses `images/` directly and
defaults to a light, print-friendly palette (the web deck's light-mode colors) rather than the
on-screen dark theme.

```bash
make pdf      # builds build/talk.pdf via latexmk
make open     # build, then open the PDF (macOS)
make clean    # remove latexmk's auxiliary files, keep the PDF/PPTX
make distclean  # remove build/ entirely
```

Requires a LaTeX toolchain with `latexmk` and `pdflatex` (any distribution — MacTeX, TeX Live,
etc.) plus the `csquotes` package. `make pdf` builds a 35-page `build/talk.pdf` with no LaTeX
warnings and no overfull/underfull boxes.

## PowerPoint version

`build_pptx.py` generates a `.pptx` edition of the same 35 slides, using
[python-pptx](https://python-pptx.readthedocs.io/) — for audiences or reviewers who need an
editable PowerPoint file rather than a PDF or a browser. Like `talk.tex`, it's a separate,
hand-maintained source (not generated from `index.html` or vice versa), reuses `images/`
directly, and uses the same light amber/sage palette. Slide size is 13.333in × 7.5in
(widescreen 16:9).

```bash
make pptx        # builds build/talk.pptx
make open-pptx   # build, then open it (macOS)
```

Requires `python-pptx` and `Pillow`: `python3 -m pip install --user python-pptx pillow`.

`index.html`, `talk.tex`, and `build_pptx.py` are three independent sources for the same
slides, kept in sync by hand — there is no automated conversion between any of them. When
editing the talk, update all three.

## Present it

```bash
./serve.sh          # serves this folder directly (self-contained), opens the deck
./serve.sh 8080      # choose a port
./serve.sh --pdf     # open the print-to-PDF view for export
```

### Keys
- **Speaker view / notes:** press <kbd>S</kbd> (every slide has notes with the sourcing/argument for that beat).
- **Overview map:** <kbd>Esc</kbd> or <kbd>O</kbd>.
- **Fullscreen:** <kbd>F</kbd>. **Next/prev:** arrows / space.

## What's covered

`index.html` (the web deck) holds 35 slides in presentation order: an **essential path of 22**
(20 content/structural slides plus the two QR "Follow Along" bookends) sized for a 30-minute
slot, then a "Backup Slides" divider, then **13 backup slides** held in reserve for Q&A or a
longer version of the talk. Both segments preserve the book's chronological order internally —
the backups are extra lens examples pulled out of the middle of that march, not a different
argument. `talk.tex` and `build_pptx.py` were **not** reordered and still present the original
single-pass, 35-slide chronological structure described below — a deliberate exception to the
"keep all three in sync" rule for the two archival formats, since they're meant as the
full-length record rather than a timed presentation path. If the 30-minute cut changes, update
`index.html`'s ordering; the `.tex`/`.pptx` chronological structure doesn't need to follow.

The chronological argument (as `talk.tex`/`build_pptx.py` present it, and as `index.html`
presents it internally within each of its two segments) runs in three acts, with the QR "Follow
Along" bookends sitting right after the title slide and again at the very close (frame/slide
comments "1B" and "32" in `talk.tex`/`build_pptx.py`) — like the title slide, outside the
numbered content sequence and carrying no page number:

1. **We Already Had Our Singularity** (slides 1–4) — CHOC's core thesis and the Faustian-Turing
   motif from the conclusion, planted here and resolved at the close.
2. **Six Lenses, One Continuous Argument** (slides 5–28) — a chronological march through CHOC,
   each slide tagged to the automation / agency / accountability / access / labor /
   environmental-cost lens it best evidences. Includes two augmentation-focused slides added
   deliberately so AI doesn't read as CHOC's destination: "computation gets a definition" (the
   Turing machine) and the memex/World Brain throughline — CHOC's own strongest evidence that
   augmentation of human capability predates AI by 80 years and doesn't need it. One slide is
   marked explicitly as the speaker's own voice — not book evidence — bridging to present-day
   generative/agentic AI via the `introcs-python-ai` course motivation reading, deliberately
   framed as one item in a long list rather than the list's culmination.
3. **Directing the Disruption** (slides 29–33) — resolves the Faustian-Turing motif, names
   CHOC's explicit 2020 endpoint as a hand-off to the talk, and closes on the talk abstract's own
   final line.

In `index.html`'s reordered 30-minute path, Act 2 is trimmed to one strong example per lens
(Leibniz, Lovelace, the ENIAC women, the Turing machine, UNIVAC, Hopper, the Mac/supercomputer
pairing, the memex, and the pre-AI deep-learning slide) plus the bridge slide into Act 3; the
remaining Act 2 examples (access under scribal elites, the Babbage tables crisis, census
overload, gutta-percha/cables, PDP-8/Engelbart, Altair, Walkman, Mosaic, browser wars,
WikiLeaks/NSA, iPhone, global divergence, cloud infrastructure) are the 13 backups. Acts 1 and 3, plus both QR bookends, are kept whole in
the essential path — they're short and each slide resolves or sets up something else (or, for the
QR slides, does useful work regardless of how much time is left), so cutting into them saves
little time for a large cost.

**On AI's role in the deck:** CHOC ends in 2020 and never discusses generative or agentic AI.
Most historical slides make their point without mentioning AI at all; AI appears on-slide only in
a handful of deliberately scoped places ("Data, AI, and the Edge of Automation," which is
genuinely CHOC's own material; the memex slide's closing point that augmentation didn't wait for
AI; and the final three slides, which explicitly mark the move from "computing disrupts culture"
to "so does AI" as the talk's own extension, not CHOC's claim). If future edits add more
historical examples, keep new AI callbacks rare and explicit rather than a routine sign-off on
every slide.

## Known gaps to fill before the final pass

- The gutta-percha / environmental-cost slide and the cloud-infrastructure slide are
  intentionally text-only — no matching illustration exists yet in CHOC's image library for
  either passage. The memex/World Brain slide is also text-only for the same reason.
- Every direct quotation on these slides was checked against the chapter source at draft time;
  re-verify against CHOC's final proofs before presenting, in case wording changed after this
  draft.
- Two other flagged gaps from outline discussion (a hip-hop/turntable image and any additional
  early-networking-era visuals) were resolved by substituting book-sourced alternatives (the
  Walkman passage) rather than left open — check the deck notes on the Walkman slide if that
  substitution needs revisiting.
