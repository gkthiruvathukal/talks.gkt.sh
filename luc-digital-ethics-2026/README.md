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
  stay in each slide's `<figcaption>`, unchanged from the book's own credit lines.

This repo is the standalone home for the talk — it was split out of `choc-book` (a peer
directory) so it can be presented, zipped, or pushed to its own remote independent of the book's
repo.

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

32 content slides plus title, organized in three acts:

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
