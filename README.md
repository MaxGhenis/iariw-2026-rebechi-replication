# IARIW 2026 discussant slides — Rebechi et al., "What Can Money Buy?"

Discussant presentation (flipped format: discussant presents, author responds) for
Rebechi, Van Kerm, Paradowski, Lepinteur & Rohde (2026), *What Can Money Buy?
Inequality and Fiscal Policy Implications of Citizens United v. FEC*, IARIW General
Conference, Brussels, Fri 28 Aug 2026 4:00pm, session "Recent laws and their
inequality implications". Discussant: Max Ghenis (PolicyEngine). Author response:
Philippe Van Kerm.

- `app/slides/*.tsx` — 24 slides (Next.js + Tailwind)
- `public/figures/` — figures cropped from the authors' PDF
- `SPEAKER-NOTES.md` — talk track with every number sourced to a paper table
- `export/discussant-slides.pdf` — PDF for the Oxford Abstracts upload

```bash
bun install
bun run dev          # http://localhost:3000  (arrow keys; ?slide=N deep-links)
bun run export       # Playwright → export/slide-NN.png
```
Rebuild the PDF from PNGs: see the Pillow one-liner in git history / session notes.
