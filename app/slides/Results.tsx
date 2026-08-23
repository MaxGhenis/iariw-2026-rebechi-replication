import React from 'react';
import Slide from '@/components/Slide';
import SlideTitle from '@/components/SlideTitle';
import SlideSubtitle from '@/components/SlideSubtitle';
import { assetPath } from '@/lib/assetPath';

export function PoliticsSlide() {
  return (
    <Slide>
      <SlideTitle>First stage confirmed: legislatures moved right</SlideTitle>
      <SlideSubtitle>
        Replicates Abdul-Razzak et al. (2020) and extends it through the 2022
        elections (paper Appendix A)
      </SlideSubtitle>
      <div className="flex-1 min-h-0 flex gap-10 items-center pb-6">
        <div className="w-[46%] space-y-5 text-xl text-slate-700 leading-relaxed">
          <p>
            <span className="font-semibold text-slate-900">
              Republican vote share
            </span>
            : ≈ +4–5pp in ban states after 2010, both chambers (significant
            with trend controls).
          </p>
          <p>
            <span className="font-semibold text-slate-900">
              Median legislator ideology
            </span>{' '}
            (Shor–McCarty): +0.20 to +0.41 toward conservative.
          </p>
          <p>
            <span className="font-semibold text-slate-900">Party control</span>
            : Democratic legislative control −21pp** and Republican trifectas
            +15pp* — each significant in one of six specifications (Tables A-5,
            A-7).
          </p>
          <p>
            Majority parties became more extreme; minority parties moderated.
            Polarization itself moved little.
          </p>
          <p className="text-lg text-slate-500 border-l-4 border-slate-300 pl-4">
            By ban type (Table A-4): vote-share effects are not significant in
            either group, and the ideology shift is significant only in
            corporate-only-ban states (+0.27**).
          </p>
        </div>
        <div className="flex-1 h-full flex items-center justify-center">
          <img
            src={assetPath('/figures/figA3-ideology.png')}
            alt="Median ideology trends by chamber"
            className="max-h-full max-w-full object-contain"
          />
        </div>
      </div>
    </Slide>
  );
}

const TABLE4 = {
  cols: ['ATR', 'Top 5%', 'Top 1%', 'Top 5% (wealth)', 'Top 1% (wealth)', 'Reynolds–Smolensky'],
  rows: [
    {
      label: 'Corporate ban only',
      vals: ['0.01', '0.14', '0.30', '0.07', '0.10', '0.07'],
      sig: [false, false, false, false, false, false],
    },
    {
      label: 'Corporate & union ban',
      vals: ['−0.01', '−0.33', '−0.53**', '−0.25', '−0.36*', '−0.11**'],
      sig: [false, false, true, false, true, true],
    },
    {
      label: 'Difference (both − corp. only)',
      vals: ['−0.02', '−0.47**', '−0.83**', '−0.32*', '−0.46*', '−0.18**'],
      sig: [false, true, true, true, true, true],
    },
  ],
};

export function MainResultsSlide() {
  return (
    <Slide>
      <SlideTitle>
        Main result: top rates and redistribution fell — only where both bans
        fell
      </SlideTitle>
      <SlideSubtitle>
        DiD estimates × 100 (percentage points), state income taxes, 2004–2021
        (paper Table 4)
      </SlideSubtitle>
      <div className="flex-1 flex flex-col justify-center pb-8 w-full">
        <table className="w-full text-2xl">
          <thead>
            <tr className="border-b-2 border-slate-800 text-slate-900">
              <th className="text-left py-3 pr-4 font-semibold w-[26%]">
                Citizens United ×
              </th>
              {TABLE4.cols.map((c) => (
                <th key={c} className="text-right py-3 px-2 font-semibold">
                  {c}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {TABLE4.rows.map((r, i) => (
              <tr
                key={r.label}
                className={`border-b border-slate-200 ${i === 2 ? 'bg-teal-50' : ''}`}
              >
                <td className="py-4 pr-4 text-slate-700 font-medium">
                  {r.label}
                </td>
                {r.vals.map((v, j) => (
                  <td
                    key={j}
                    className={`py-4 px-2 text-right tabular-nums ${r.sig[j] ? 'font-bold text-slate-900' : 'text-slate-500'}`}
                  >
                    {v}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
        <div className="mt-6 grid grid-cols-3 gap-6 text-lg text-slate-700 leading-snug">
          <p>
            <span className="font-semibold text-slate-900">
              Concentrated at the top.
            </span>{' '}
            The overall ATR barely moves; top-1% rates fall 0.53pp.
          </p>
          <p>
            <span className="font-semibold text-slate-900">Asymmetric.</span>{' '}
            Corporate-only-ban states drift (insignificantly) the other way.
          </p>
          <p>
            <span className="font-semibold text-slate-900">
              Redistribution falls.
            </span>{' '}
            Reynolds–Smolensky drops where both bans lifted.
          </p>
        </div>
        <p className="mt-4 text-base text-slate-400">
          N = 846; SEs clustered by state; * p&lt;0.10, ** p&lt;0.05.
        </p>
      </div>
    </Slide>
  );
}

export function EventStudySlide() {
  return (
    <Slide>
      <SlideTitle>No significant pre-trends; gradual divergence after 2010</SlideTitle>
      <SlideSubtitle>
        Event studies by pre-existing ban type (paper Figure 3) — joint
        pre-trend tests pass for every outcome
      </SlideSubtitle>
      <div className="flex-1 min-h-0 flex gap-8 items-center pb-6">
        <div className="flex-1 h-full flex items-center justify-center">
          <img
            src={assetPath('/figures/fig3-eventstudy.png')}
            alt="Event study graphs for state-level taxes by ban type"
            className="max-h-full max-w-full object-contain"
          />
        </div>
        <div className="w-[26%] space-y-5 text-xl text-slate-700 leading-relaxed">
          <p>
            Corporate-and-union-ban states (yellow) drift steadily down; the
            gap builds over a decade rather than jumping.
          </p>
          <p>
            Post-2010 coefficients jointly significant for that group: top 1%{' '}
            <span className="tabular-nums">p = 0.025</span>,
            Reynolds–Smolensky <span className="tabular-nums">p = 0.049</span>{' '}
            (paper Table 5).
          </p>
          <p>
            Ban-type differences jointly significant for every outcome except
            the overall ATR.
          </p>
        </div>
      </div>
    </Slide>
  );
}

const ROBUSTNESS = [
  {
    name: 'Synthetic DiD',
    result: 'Same signs; group estimates smaller and not significant (top 1% −0.40, RS −0.07); ban-type differences hold at 10% (−0.72*, −0.13*)',
  },
  {
    name: 'Wooldridge (2025) TWFE',
    result: 'Identical to baseline (top 1% −0.53**, RS −0.11**) — expected with one treatment date and never-treated controls',
  },
  {
    name: 'Leave-one-out',
    result: 'No single treated state drives either group',
  },
  {
    name: 'Drop 8 no-income-tax states',
    result: 'Effects grow (difference: top 1% −1.13***, RS −0.20**) — the authors read the baseline as a lower bound',
  },
  {
    name: 'After-federal-tax income (App. D)',
    result: 'Larger and sharper (top 1% −0.93***; difference −1.27***, RS −0.24***)',
  },
];

export function RobustnessSlide() {
  return (
    <Slide>
      <SlideTitle>The same signs under stress — with two caveats</SlideTitle>
      <SlideSubtitle>
        Alternative estimators, samples, and income concepts
      </SlideSubtitle>
      <div className="flex-1 flex flex-col justify-center pb-10 max-w-6xl w-full mx-auto">
        <table className="w-full text-xl">
          <tbody>
            {ROBUSTNESS.map((r) => (
              <tr key={r.name} className="border-b border-slate-200">
                <td className="py-4 pr-8 font-semibold text-slate-900 w-[34%] align-top">
                  {r.name}
                </td>
                <td className="py-4 text-slate-700">{r.result}</td>
              </tr>
            ))}
          </tbody>
        </table>
        <div className="mt-6 border-l-4 border-amber-400 pl-6 py-3 bg-amber-50 rounded-r-lg text-xl text-slate-700 leading-relaxed">
          <p>
            <span className="font-semibold text-slate-900">
              The honest caveat:
            </span>{' '}
            adding state-specific linear trends pulls the corporate-and-union
            effects “much closer to zero” (Fig. 4), and the SDID group estimates
            lose significance. The authors treat trends as a robustness check,
            since they can absorb genuinely gradual treatment effects — exactly
            the dynamics the event studies show.
          </p>
        </div>
      </div>
    </Slide>
  );
}

export function HeterogeneitySlide() {
  return (
    <Slide>
      <SlideTitle>Where the effect lives</SlideTitle>
      <SlideSubtitle>
        State-by-state synthetic DiD effects (paper Figure 5): top-1% ATR and
        Reynolds–Smolensky
      </SlideSubtitle>
      <div className="flex-1 min-h-0 flex gap-8 items-center pb-6">
        <div className="flex-1 h-full flex flex-col items-center justify-center gap-2">
          <img
            src={assetPath('/figures/fig5b-top1.png')}
            alt="State-specific SDID effects, ATR top 1%"
            className="max-h-[48%] max-w-full object-contain"
          />
          <img
            src={assetPath('/figures/fig5e-rs.png')}
            alt="State-specific SDID effects, Reynolds-Smolensky"
            className="max-h-[48%] max-w-full object-contain"
          />
        </div>
        <div className="w-[34%] space-y-5 text-xl text-slate-700 leading-relaxed">
          <p>
            <span className="font-semibold text-slate-900">
              Connecticut and Minnesota
            </span>{' '}
            pull the corporate-only group positive — states mostly under
            Democratic or divided government.
          </p>
          <p>
            <span className="font-semibold text-slate-900">
              North Carolina, North Dakota, Ohio
            </span>{' '}
            anchor the negative end — Republican-controlled after 2010.
          </p>
          <p className="border-l-4 border-slate-300 pl-4 text-lg text-slate-500">
            The authors say it plainly: “most of our results are driven by few
            outlying states” — though leave-one-out shows no <em>single</em>{' '}
            state is decisive.
          </p>
        </div>
      </div>
    </Slide>
  );
}
