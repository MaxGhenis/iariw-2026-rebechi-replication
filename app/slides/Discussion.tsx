import React from 'react';
import Slide from '@/components/Slide';
import SlideTitle from '@/components/SlideTitle';
import SlideSubtitle from '@/components/SlideSubtitle';
import { assetPath } from '@/lib/assetPath';

/* ------------------------------------------------------------------ */
/* Comment 1 — the result is conditional on the union ban              */
/* ------------------------------------------------------------------ */
export function Comment1Slide() {
  return (
    <Slide>
      <SlideTitle>1 · The finding is about the union ban — say so up front</SlideTitle>
      <SlideSubtitle>
        Every significant coefficient sits in the 13 states where the <em>union</em> ban
        was also lifted; the abstract describes a general effect
      </SlideSubtitle>
      <div className="flex-1 min-h-0 grid grid-cols-2 gap-10 pb-8 content-center text-xl text-slate-700 leading-snug">
        <div className="space-y-5">
          <div className="bg-slate-50 border border-slate-200 rounded-xl px-7 py-5">
            <p className="font-semibold text-slate-900 mb-1">Table 4, read as a triple difference</p>
            <p>
              Corporate-&amp;-union ban: top 1% <span className="font-semibold">−0.53**</span>, RS{' '}
              <span className="font-semibold">−0.11**</span>. Corporate-only: +0.30, +0.07 (n.s.).
              The −0.83** difference is, under DiD logic, <em>the extra effect of also lifting the
              union ban</em> — the opposite of what a unions-fund-Democrats story predicts.
            </p>
          </div>
          <div className="bg-slate-50 border border-slate-200 rounded-xl px-7 py-5">
            <p className="font-semibold text-slate-900 mb-1">The detectable political first stage is in the corporate-only group (Table A-4)</p>
            <p>
              By ban type, Republican vote share is n.s. in both groups (0.05, 0.01); the ideology
              shift is significant only in the <em>corporate-only</em> states (+0.27**) — where
              taxes moved up — and the cross-group differences are n.s. Residualizing on vote share
              or ideology barely moves the tax coefficients (Table 8: −0.47 to −0.56).
            </p>
          </div>
          <p className="text-slate-600">
            The authors’ resolution — corporate-&amp;-union states had weaker unions — rests on a
            ~1pp density gap (Fig. 6). In our public-data replication pre-2010 density is 11.5%
            vs 12.4% vs 11.5% across the three groups.
          </p>
        </div>
        <div className="space-y-5">
          <div className="border-l-4 border-pe-teal pl-6 py-4 bg-teal-50 rounded-r-lg">
            <p className="font-semibold text-slate-900 mb-2">What would convince me</p>
            <ul className="list-disc pl-5 space-y-2.5">
              <li>
                State the conditionality in the abstract and title the mechanism section after it.
              </li>
              <li>
                A dose-response test: CU × pre-2010 union density, within ban groups. In our
                replication the corporate-&amp;-union effect does <em>not</em> scale with density
                (interaction −0.02, p = 0.57), and CU × density is <em>positive</em> — high-union
                states raised top taxes after 2010.
              </li>
              <li>
                We ran the obvious horse race: adding post × Republican-trifecta acquisition
                (2011–13; 8 of your 13 states, 1 of 8 corporate-only, 6 of 26 controls) moves the
                coefficient only 16–20% (top 1% −0.57*, RS −0.07*); REDMAP targeting, ≈ 0. So the
                contrast is not just the 2010 wave — which leaves the question sharper: what is it?
                A theory of change with names would answer it.
              </li>
            </ul>
          </div>
          <p className="text-lg text-slate-500">
            Replication: SCF 2010 public extract → TAXSIM-35 (local), 47 units × 18 years; union
            density from Hirsch–Macpherson (unionstats.com). Everything is open: github.com/MaxGhenis/iariw-2026-rebechi-replication
          </p>
        </div>
      </div>
    </Slide>
  );
}

/* ------------------------------------------------------------------ */
/* Comment 2 — which −0.53 do you believe                              */
/* ------------------------------------------------------------------ */
export function Comment2Slide() {
  return (
    <Slide>
      <SlideTitle>2 · Which −0.53 do you believe?</SlideTitle>
      <SlideSubtitle>
        The treated–control gap was already widening before 2010 — replication from public
        data (SCF 2010 → TAXSIM-35, same design), group means by year
      </SlideSubtitle>
      <div className="flex-1 min-h-0 flex gap-8 items-center pb-4">
        <div className="flex-1 h-full flex items-center justify-center">
          <img
            src={assetPath('/figures/repl-group-means.png')}
            alt="Top-1% state ATR group means by year, replication"
            className="max-h-full max-w-full object-contain"
          />
        </div>
        <div className="w-[36%] space-y-3.5 text-lg text-slate-700 leading-snug">
          <p>
            Gap −1.56 (2004) → −2.03 (2009) → −2.55 (2021). A differential linear pre-trend
            test rejects at 10% (−0.09 pp/yr, p = 0.09; −0.13/yr, p = 0.06 among income-tax
            states) and three of five individual leads are significant at 5%; the joint lead
            test (p = 0.40) has no power against a drift.
          </p>
          <p>
            Consistent with the paper’s own checks: state-specific trends pull the effect
            “much closer to zero” (Fig. 4; −0.27, n.s., in our panel); SDID group estimates are
            n.s. (Table 6: −0.40, −0.07).
          </p>
          <div className="border-l-4 border-pe-teal pl-4 py-1.5 bg-teal-50 rounded-r-lg">
            <p className="font-semibold text-slate-900">Asks</p>
            <p>
              Report the trends specification as co-equal, and bound the estimate with
              Rambachan–Roth pre-trend sensitivity.
            </p>
          </div>
          <p className="text-base text-slate-500">
            In fairness: the stars are not a few-cluster artifact. In our replication the
            top-1% effect survives randomization inference (p = 0.013) and a wild cluster
            bootstrap (p = 0.030).
          </p>
        </div>
      </div>
    </Slide>
  );
}

/* ------------------------------------------------------------------ */
/* Comment 3 — five reforms, not thirteen states                       */
/* ------------------------------------------------------------------ */
export function Comment3Slide() {
  return (
    <Slide>
      <SlideTitle>3 · Five tax reforms, not thirteen states</SlideTitle>
      <SlideSubtitle>
        Per-state contributions to the corporate-&amp;-union coefficient (replication; the paper’s
        Fig. 5 shows the same ranking with SDID)
      </SlideSubtitle>
      <div className="flex-1 min-h-0 flex gap-8 items-center pb-4">
        <div className="flex-1 h-full flex items-center justify-center">
          <img
            src={assetPath('/figures/repl-per-state.png')}
            alt="Per-state DiD contributions, top-1% ATR"
            className="max-h-full max-w-full object-contain"
          />
        </div>
        <div className="w-[36%] space-y-3.5 text-lg text-slate-700 leading-snug">
          <p>
            Ohio, North Dakota, North Carolina, Rhode Island and Oklahoma carry the estimate.
            Four treated states have no broad income tax and Pennsylvania’s is flat — they cannot
            respond. Michigan and Wisconsin moved the other way.
          </p>
          <p>
            Drop NC, ND and OH together: <span className="font-semibold">−0.29 (SE 0.24, p = 0.22)</span>.
            Leave-one-out alone cannot show this.
          </p>
          <div className="border-l-4 border-pe-teal pl-4 py-1.5 bg-teal-50 rounded-r-lg">
            <p className="font-semibold text-slate-900">Asks</p>
            <p>
              Consider making the income-tax-states sample (Table B-1) the main one; report
              leave-three-out; and tell the story of the five reforms — North Dakota’s cuts began in
              May 2009, during the oil boom: a plausible confounder, not a channel.
            </p>
          </div>
        </div>
      </div>
    </Slide>
  );
}

/* ------------------------------------------------------------------ */
/* Comment 4 — model the tax function, not its summaries               */
/* ------------------------------------------------------------------ */
export function Comment4Slide() {
  return (
    <Slide>
      <SlideTitle>4 · Model the tax function, not six summaries of it</SlideTitle>
      <SlideSubtitle>
        The same 900 simulated datasets support a household-level incidence regression (here
        in its group-level equivalent) — who got the cut, in dollars (replication,
        corporate-&amp;-union states)
      </SlideSubtitle>
      <div className="flex-1 min-h-0 flex gap-8 items-center pb-4">
        <div className="flex-1 h-full flex items-center justify-center">
          <img
            src={assetPath('/figures/repl-incidence.png')}
            alt="Incidence gradient by AGI group, replication"
            className="max-h-full max-w-full object-contain"
          />
        </div>
        <div className="w-[36%] space-y-3.5 text-lg text-slate-700 leading-snug">
          <p>
            A monotone gradient: nothing at the bottom, about −$9,000 a year for the average
            top-1% household (2010 dollars). Capital-heavy and wage-heavy top households are hit
            alike — across-the-board top-rate cuts, not capital carve-outs.
          </p>
          <p>
            With a fixed sample, the saturated micro regression <em>is</em> the paper’s Φ by
            subgroup — so this costs nothing new and turns “RS −0.11” into an incidence table.
            And contrasts difference out common schedule shocks: the β the paper defines in
            eq. (5) but never reports — ATR(top 20%) − ATR(bottom 20%) — is its most precise
            outcome in our replication: −0.68 (SE 0.22, t = 3.1).
          </p>
          <div className="border-l-4 border-pe-teal pl-4 py-1.5 bg-teal-50 rounded-r-lg">
            <p className="font-semibold text-slate-900">Asks</p>
            <p>
              Report β (eq. 5, defined but never shown) and the dollar incidence; say that
              RS −0.11 is −0.0011 Gini points on a state-tax redistribution of about 0.004 — and
              say whether benefits B (eq. 1) enter the simulation at all.
            </p>
          </div>
        </div>
      </div>
    </Slide>
  );
}

/* ------------------------------------------------------------------ */
/* Replication slide                                                    */
/* ------------------------------------------------------------------ */
const REPL = [
  { row: 'Top-1% ATR, corporate & union ban', paper: '−0.53** (0.24)', mine: '−0.67** (0.29)' },
  { row: 'Reynolds–Smolensky, corporate & union ban', paper: '−0.11** (0.04)', mine: '−0.09** (0.03)' },
  { row: 'Difference (both − corporate only), top 1%', paper: '−0.83** (0.35)', mine: '−0.87** (0.38)' },
  { row: 'Corporate-only arm', paper: 'positive, n.s.', mine: 'positive, n.s.' },
  { row: 'Income-tax states only (Table B-1), top 1%', paper: '−0.77** (0.30)', mine: '−0.95** (0.36)' },
  { row: 'Overall ATR, corporate & union ban', paper: '−0.01 (0.13)', mine: '−0.35** (0.17)' },
];

export function ReplicationSlide() {
  return (
    <Slide>
      <SlideTitle>The headline reproduces from public data</SlideTitle>
      <SlideSubtitle>
        SCF 2010 public extract → NBER TAXSIM-35 (run locally) → 51 jurisdictions × 18 years ×
        6,482 households → eq. (7). Coefficients × 100, SEs clustered by state
      </SlideSubtitle>
      <div className="flex-1 min-h-0 grid grid-cols-[1.35fr_1fr] gap-10 pb-6 items-center">
        <table className="w-full text-xl">
          <thead>
            <tr className="border-b-2 border-slate-800 text-slate-900">
              <th className="text-left py-2 font-semibold">Table 4 row</th>
              <th className="text-right py-2 font-semibold">Paper</th>
              <th className="text-right py-2 font-semibold text-pe-teal">Replication</th>
            </tr>
          </thead>
          <tbody>
            {REPL.map((r) => (
              <tr key={r.row} className="border-b border-slate-200">
                <td className="py-3.5 text-slate-700">{r.row}</td>
                <td className="py-3.5 text-right tabular-nums text-slate-700">{r.paper}</td>
                <td className="py-3.5 text-right tabular-nums text-slate-900 font-medium">{r.mine}</td>
              </tr>
            ))}
          </tbody>
        </table>
        <div className="space-y-4 text-xl text-slate-700 leading-snug">
          <p>
            N = 846 only with DC in the panel (47 × 18) — the text says 46 states. “SCF 2011”
            is the 2010 wave (LWS US10; income year 2009): the SCF is triennial.
          </p>
          <p>
            What does not reproduce: the clean zero on the overall ATR. The public extract
            forces no itemized deductions and taxes Social Security as pensions, which inflates
            middle-class liabilities. The top-1% and RS rows are insensitive to this.
          </p>
          <p className="text-lg text-slate-500">
            Full pipeline ≈ 25 minutes of compute; one SCF implicate; TAXSIM vintage differs.
            Scripts, panel and results: github.com/MaxGhenis/iariw-2026-rebechi-replication. A released 47 × 18 panel plus code would make
            the core table reproducible in an afternoon.
          </p>
        </div>
      </div>
    </Slide>
  );
}

/* ------------------------------------------------------------------ */
/* Literature slide (filled from the verified survey)                  */
/* ------------------------------------------------------------------ */
export const LIT: { paper: string; finds: string }[] = [
  {
    paper: 'Gilens, Patterson & Haines (2021, APSR) — not cited',
    finds:
      'Same natural experiment, generalized synthetic control: top corporate tax −2.83 (p = 0.01; 0–100 index), and twice as large in the eight corporate-only states (−5.55, vs all treated) — the union counterweight hypothesized ex ante, in the mirror image of this paper.',
  },
  {
    paper: 'Slattery, Tazhitdinova & Robinson (2023, JPubE) — cited as “a moderate effect”',
    finds:
      'A precise null on top corporate, top personal-income and sales rates, incentives and revenues (top PIT ≈ −0.46pp, n.s.); corporate-only restriction: a tighter null. Parallel trends fail in levels, so they use logs.',
  },
  {
    paper: 'Klumpp, Mialon & Williams (2016, JLE)',
    finds:
      'CU raised Republican House-race wins ≈ 4pp; descriptively largest in MN, MT, MI, OH, IA — three of them corporate-only states (no ban-type test reported). The corporate-funded 2010 REDMAP drive targeted MI, OH, PA, TX, NC, WI for redistricting, not for ban type.',
  },
  {
    paper: 'Abdul-Razzak, Prato & Wolton (2020, Electoral Studies)',
    finds:
      'Vote-share effect ≈ 4–5pp (trend-dependent); ≈ 8pp where unions are weak, ≈ 0 where strong — by density, not ban type. In treated disclosure states Democratic-aligned groups still outspent Republican-aligned ones after CU; fn. 12: no effect on public goods.',
  },
  {
    paper: 'Hansen, Rocca & Ortiz (2015, JOP); Spencer & Wood (2014)',
    finds:
      'Major corporations “were not a source of the dramatic increase in independent spending” (federal, 2012); the state-level surge ran through 501(c)/527 vehicles whose donors are unobservable — ≈ $1.6M per treated state over 2010–12.',
  },
  {
    paper: 'Akey et al. (2023, NBER); Werner & Coleman (2015, JLEO); Farver (2024)',
    finds:
      'The policy record is mixed, not “mostly null”: enforcement and antitakeover effects exist; tax rates negative but n.s. (PIT ≈ −0.3pp); no effect on environmental policy or overall policy liberalism; turnover rose in both parties.',
  },
];

export function LiteratureSlide() {
  return (
    <Slide>
      <SlideTitle>Where this sits in the Citizens United evidence</SlideTitle>
      <SlideSubtitle>
        What the cited and uncited empirical work actually finds — every entry retrieved and checked
      </SlideSubtitle>
      <div className="flex-1 min-h-0 flex flex-col justify-center pb-6">
        <table className="w-full text-xl leading-snug">
          <tbody>
            {LIT.map((r) => (
              <tr key={r.paper} className="border-b border-slate-200 align-top">
                <td className="py-4 pr-8 font-semibold text-slate-900 w-[30%]">{r.paper}</td>
                <td className="py-4 text-slate-700">{r.finds}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </Slide>
  );
}
