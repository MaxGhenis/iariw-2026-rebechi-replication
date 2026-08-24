import React from 'react';
import Slide from '@/components/Slide';
import SlideTitle from '@/components/SlideTitle';
import SlideSubtitle from '@/components/SlideSubtitle';

export function ThisPaperSlide() {
  return (
    <Slide>
      <SlideTitle>This paper</SlideTitle>
      <SlideSubtitle>
        From vote shares to tax schedules to inequality
      </SlideSubtitle>
      <div className="flex-1 flex flex-col justify-center pb-10 space-y-8 max-w-5xl w-full mx-auto">
        <div className="bg-slate-800 text-white rounded-xl px-8 py-6">
          <p className="text-sm uppercase tracking-wide text-teal-300 font-semibold mb-2">
            Research question
          </p>
          <p className="text-2xl leading-relaxed">
            Did lifting bans on independent political expenditures change the
            size and progressivity of state income taxes — and post-tax income
            inequality?
          </p>
        </div>
        <div className="space-y-5 text-2xl text-slate-700 leading-relaxed">
          <p>
            Closest prior work (Slattery, Tazhitdinova &amp; Robinson 2023,{' '}
            <em>J. Public Economics</em>) studies statutory rates and aggregate
            revenues — the tax system{' '}
            <span className="italic">in the books</span>.
          </p>
          <p>
            This paper measures the tax system{' '}
            <span className="font-semibold text-slate-900">
              as households experience it
            </span>
            : average rates by income and wealth group, and the redistribution
            the schedule actually delivers.
          </p>
          <div className="border-l-4 border-pe-teal pl-6 py-2 bg-teal-50 rounded-r-lg">
            <p className="text-slate-800">
              Preview: where states had banned{' '}
              <span className="font-semibold">both corporate and union</span>{' '}
              spending, top-group tax rates and redistribution fell after the
              ruling. Where only corporations had been banned, they did not.
            </p>
          </div>
        </div>
      </div>
    </Slide>
  );
}

export function DataSlide() {
  return (
    <Slide>
      <SlideTitle>
        Measurement: 900 simulated tax systems, one fixed population
      </SlideTitle>
      <SlideSubtitle>
        SCF microdata through NBER TAXSIM — only the law varies
      </SlideSubtitle>
      <div className="flex-1 content-center pb-10 grid grid-cols-2 gap-10 max-w-6xl w-full mx-auto">
        <div className="space-y-5 text-xl text-slate-700 leading-relaxed">
          <p>
            <span className="font-semibold text-slate-900">
              Survey of Consumer Finances 2011
            </span>{' '}
            (LWS-harmonized): the household survey that oversamples the wealthy
            — credible top-5% and top-1% incomes <em>and net worth</em>.
          </p>
          <p>
            <span className="font-semibold text-slate-900">NBER TAXSIM</span>:
            federal and state income tax law for all 50 states, 2004–2021.
          </p>
          <p>
            The same households are run through{' '}
            <span className="font-semibold text-slate-900">
              every state-year schedule
            </span>{' '}
            (incomes CPI-deflated to each year):
          </p>
          <p className="text-3xl font-bold text-pe-teal text-center py-2">
            “50 states × 18 years = 900 datasets”
          </p>
          <p className="text-base text-slate-500 text-center -mt-1">
            (as written — the estimation panel’s N = 846 implies DC too: 51 × 18 = 918)
          </p>
        </div>
        <div className="space-y-5">
          <div className="bg-slate-50 border border-slate-200 rounded-xl px-7 py-6 text-xl text-slate-700 leading-relaxed">
            <p className="font-semibold text-slate-900 mb-2">
              Why this is clean
            </p>
            <p>
              With the population held fixed, no composition change, migration,
              or behavioral response contaminates the measure. What moves is{' '}
              <span className="font-semibold">tax legislation itself</span> — a
              pure <em>de jure</em> policy panel.
            </p>
          </div>
          <div className="text-lg text-slate-500 leading-relaxed">
            <p>
              Main text: state taxes assessed on pre-federal income (AGI).
              Appendix D repeats everything on after-federal-tax income —
              results are larger and sharper there.
            </p>
            <p className="mt-3">
              (The SCF is triennial: “2011” is the 2010 wave, LWS US10, with
              incomes for 2009 — see the replication slide.)
            </p>
          </div>
        </div>
      </div>
    </Slide>
  );
}

const OUTCOMES = [
  {
    name: 'Average tax rate (ATR)',
    def: 'Total state income tax over total pre-tax income',
    role: 'Size of the tax',
  },
  {
    name: 'ATR, top 5% and top 1%',
    def: 'By income — and, using SCF strengths, by net worth',
    role: 'Burden at the top',
  },
  {
    name: 'Progressivity (β)',
    def: 'ATR of top 20% minus ATR of bottom 20% — defined (eq. 5) but reported in no table',
    role: 'Shape of the schedule',
  },
  {
    name: 'Reynolds–Smolensky index',
    def: 'Gini(pre-tax) − Gini(post-tax)',
    role: 'Redistribution delivered',
  },
];

export function OutcomesSlide() {
  return (
    <Slide>
      <SlideTitle>Summarizing schedules, not statutory parameters</SlideTitle>
      <SlideSubtitle>
        Top marginal rates miss deductions, exemptions, and the base — these
        indicators capture the whole shape
      </SlideSubtitle>
      <div className="flex-1 flex flex-col justify-center pb-10 max-w-6xl w-full mx-auto">
        <table className="w-full text-xl">
          <thead>
            <tr className="border-b-2 border-slate-800 text-slate-900 text-left">
              <th className="py-3 pr-6 font-semibold w-[30%]">Indicator</th>
              <th className="py-3 pr-6 font-semibold">Definition</th>
              <th className="py-3 font-semibold w-[24%]">Captures</th>
            </tr>
          </thead>
          <tbody>
            {OUTCOMES.map((o) => (
              <tr key={o.name} className="border-b border-slate-200 align-top">
                <td className="py-4 pr-6 font-semibold text-slate-900">
                  {o.name}
                </td>
                <td className="py-4 pr-6 text-slate-700">{o.def}</td>
                <td className="py-4 text-slate-500">{o.role}</td>
              </tr>
            ))}
          </tbody>
        </table>
        <p className="mt-6 text-lg text-slate-500 leading-relaxed">
          Each indicator Φ is evaluated on the fixed household sample for every
          state-year law — turning 900 simulated tax systems into a 900-cell
          panel of schedule characteristics.
        </p>
      </div>
    </Slide>
  );
}

export function DesignSlide() {
  return (
    <Slide>
      <SlideTitle>Identification: three complementary designs</SlideTitle>
      <SlideSubtitle>
        “46 states”, 2004–2021, N = 846 (= 47 units × 18 years: DC is in the panel) · treated =
        pre-2010 ban states · controls = never banned
      </SlideSubtitle>
      <div className="flex-1 flex flex-col justify-center pb-10 space-y-6 max-w-6xl w-full mx-auto">
        <div className="bg-slate-50 border border-slate-200 rounded-xl px-8 py-5 font-mono text-xl text-slate-800 text-center">
          Outcome<sub>st</sub> = β₁(CU<sub>t</sub> × CorpBan<sub>s</sub>) +
          β₂(CU<sub>t</sub> × CorpUnionBan<sub>s</sub>) + γ<sub>s</sub> + δ
          <sub>t</sub> + ε<sub>st</sub>
        </div>
        <div className="grid grid-cols-3 gap-6 text-xl text-slate-700 leading-relaxed">
          <div>
            <p className="font-semibold text-slate-900 mb-2">
              Two-way fixed effects
            </p>
            <p>
              Separate treatment effects by pre-existing ban type — the paper’s
              key refinement over pooled designs.
            </p>
          </div>
          <div>
            <p className="font-semibold text-slate-900 mb-2">Event studies</p>
            <p>
              Leads and lags around 2010 (2009 omitted): pre-trend tests plus
              the time path of effects.
            </p>
          </div>
          <div>
            <p className="font-semibold text-slate-900 mb-2">Synthetic DiD</p>
            <p>
              Arkhangelsky et al. (2021) reweighting, group-level and
              state-by-state ATETs; plus a Wooldridge (2025) TWFE check.
            </p>
          </div>
        </div>
        <p className="text-lg text-slate-500 leading-relaxed border-t border-slate-200 pt-4">
          Exclusions: CO and SD (bans adopted only in 2002 and 2007), NE
          (nonpartisan unicameral legislature), LA (nonpartisan blanket
          primaries). Standard errors clustered by state; coefficients ×100
          (percentage points).
        </p>
      </div>
    </Slide>
  );
}
