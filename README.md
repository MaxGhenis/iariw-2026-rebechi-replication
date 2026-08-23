# Rebechi et al. (2026), "What Can Money Buy?" — discussant slides, review and replication

Discussant presentation (flipped format: discussant presents, author responds) for
Rebechi, Van Kerm, Paradowski, Lepinteur & Rohde (2026), *What Can Money Buy?
Inequality and Fiscal Policy Implications of Citizens United v. FEC*, IARIW General
Conference, Brussels, Fri 28 Aug 2026 4:00pm, Room A1, session "Recent laws and their
inequality implications". Discussant: Max Ghenis (PolicyEngine). Author response:
Philippe Van Kerm.

Public repository: https://github.com/MaxGhenis/iariw-2026-rebechi-replication (MIT). Everything here — slides, review memo,
verification audit, replication scripts and results — is open.

- `app/slides/*.tsx` — 26 slides (Next.js + Tailwind): 1–18 present the paper, 20–23 four
  comments, 24 replication, 25 literature, 26 close
- `SPEAKER-NOTES.md` — talk track with every number sourced to a paper table or a file here
- `REVIEW.md` — adversarial review memo: findings with CONFIRMED / PLAUSIBLE / REFUTED status,
  ranked discussant questions, what held up
- `review/lenses/` — source-by-source evidence behind the memo (literature survey, citations,
  red team, econometrics, magnitudes, mechanism, replication availability)
- [`replication/README.md`](replication/README.md) — package quick start and full pipeline.
- [`replication/report/index.qmd`](replication/report/index.qmd) — executable Quarto report.
- `public/figures/` — figures cropped from the authors' PDF plus `repl-*.png` from the replication
- `export/discussant-slides.pdf` — PDF for the Oxford Abstracts upload

```bash
bun install
bun run dev                      # http://localhost:3000  (arrow keys; ?slide=N deep-links)
PORT=3311 bun run export         # Playwright → export/slide-NN.png (PORT optional)
uv run --with pillow python make_pdf.py   # PNGs → export/discussant-slides.pdf
```
