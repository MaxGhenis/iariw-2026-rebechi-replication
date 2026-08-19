import React from 'react';
import Slide from '@/components/Slide';
import SlideTitle from '@/components/SlideTitle';
import SlideSubtitle from '@/components/SlideSubtitle';

export function Comment1Slide() {
  return (
    <Slide>
      <SlideTitle>
        1 · The measurement design deserves top billing
      </SlideTitle>
      <SlideSubtitle>
        The fixed-population simulated-schedule panel is the paper’s most
        exportable idea
      </SlideSubtitle>
      <div className="flex-1 flex flex-col justify-center pb-10 space-y-6 max-w-5xl w-full mx-auto text-xl text-slate-700 leading-relaxed">
        <p>
          Simulating every state-year law on one fixed sample is the right way
          to build a{' '}
          <span className="font-semibold text-slate-900">
            de jure policy panel
          </span>
          : it strips out composition, migration, and behavior by
          construction. Name the method, give it a figure, and readers will
          reuse it well beyond campaign finance.
        </p>
        <div className="bg-slate-50 border border-slate-200 rounded-xl px-7 py-5">
          <p className="font-semibold text-slate-900 mb-2">
            The flip side to state clearly
          </p>
          <p>
            Each Φ<sup>st</sup> characterizes state <em>s</em>’s law applied to
            a <span className="font-semibold">common national population</span>.
            The “top 1%” being taxed is the national top 1% — not Ohio’s. That
            is the right object for isolating legislation, but it is not the
            state’s realized tax structure.
          </p>
        </div>
        <p>
          <span className="font-semibold text-slate-900">Suggestion:</span>{' '}
          pair the de jure panel with a <em>de facto</em> companion — realized
          state ATRs from IRS SOI, or state-representative microdata (CPS/ACS)
          through TAXSIM — to show the legislated regressivity materialized,
          and price it in dollars.
        </p>
      </div>
    </Slide>
  );
}

export function Comment2Slide() {
  return (
    <Slide>
      <SlideTitle>2 · Which fiscal margins can respond?</SlideTitle>
      <SlideSubtitle>
        The outcome is the state personal income tax — one lever among several
      </SlideSubtitle>
      <div className="flex-1 flex flex-col justify-center pb-10 space-y-6 max-w-5xl w-full mx-auto text-xl text-slate-700 leading-relaxed">
        <p>
          A legislature tilting right can also move{' '}
          <span className="font-semibold text-slate-900">
            sales and excise composition
          </span>{' '}
          (regressive), <span className="font-semibold text-slate-900">corporate rates</span>{' '}
          (Slattery et al. find moderate effects),{' '}
          <span className="font-semibold text-slate-900">state EITC/CTC add-ons</span>, and
          the <span className="font-semibold text-slate-900">spending side</span> —
          benefit generosity.
        </p>
        <div className="grid grid-cols-2 gap-8">
          <div className="bg-slate-50 border border-slate-200 rounded-xl px-7 py-5">
            <p className="font-semibold text-slate-900 mb-2">
              A clarifying question
            </p>
            <p>
              Eq. (1) defines Φ over taxes <em>and</em> benefit entitlements B
              — am I right that B is unpopulated here, since TAXSIM covers
              income taxes? Worth stating either way.
            </p>
          </div>
          <div className="bg-slate-50 border border-slate-200 rounded-xl px-7 py-5">
            <p className="font-semibold text-slate-900 mb-2">Why it matters</p>
            <p>
              If other margins shifted the same way, income-tax RS{' '}
              <em>understates</em> the total regressive turn; if states
              substituted across instruments, it could overstate it.
            </p>
          </div>
        </div>
        <p>
          <span className="font-semibold text-slate-900">Suggestion:</span> a
          “total fiscal incidence” extension — LIS/LWS harmonization plus state
          benefit rules — would raise the stakes of the finding for this
          audience.
        </p>
      </div>
    </Slide>
  );
}

export function Comment3Slide() {
  return (
    <Slide>
      <SlideTitle>3 · Inference with 8 + 13 treated states</SlideTitle>
      <SlideSubtitle>
        And a way to make the union mechanism do identification work
      </SlideSubtitle>
      <div className="flex-1 flex flex-col justify-center pb-10 space-y-6 max-w-5xl w-full mx-auto text-xl text-slate-700 leading-relaxed">
        <p>
          Two treated clusters of 8 and 13 states, six correlated outcomes:{' '}
          <span className="font-semibold text-slate-900">
            wild-cluster bootstrap or randomization inference
          </span>{' '}
          on the triple-difference would firm up the stars, alongside the SDID
          placebo inference already reported.
        </p>
        <p>
          Ban type is not random:{' '}
          <span className="font-semibold text-slate-900">
            the corporate-and-union group is disproportionately
            Republican-controlled
          </span>{' '}
          (Fig. C-1), and the post-2010 decade is crowded — ACA surtaxes, ATRA,
          TCJA, state fiscal recoveries. State trends attenuate the effects;
          say plainly which specification you believe, and why.
        </p>
        <div className="border-l-4 border-pe-teal pl-6 py-3 bg-teal-50 rounded-r-lg">
          <p>
            <span className="font-semibold text-slate-900">
              The test I would most like to see:
            </span>{' '}
            interact Citizens United with{' '}
            <span className="font-semibold">pre-2010 union density</span> as a
            continuous moderator. If the counterweight story is right, effects
            should scale with density <em>within</em> ban groups — turning
            Figure 6 from description into identification.
          </p>
        </div>
      </div>
    </Slide>
  );
}

export function Comment4Slide() {
  return (
    <Slide>
      <SlideTitle>4 · Magnitudes, in policy units</SlideTitle>
      <SlideSubtitle>
        The proportions are the headline — say them in the text
      </SlideSubtitle>
      <div className="flex-1 flex flex-col justify-center pb-10 space-y-5 max-w-5xl w-full mx-auto text-xl text-slate-700 leading-relaxed">
        <div className="grid grid-cols-2 gap-8">
          <div className="bg-slate-800 text-white rounded-xl px-7 py-5">
            <p className="text-4xl font-bold text-teal-300 mb-1">≈ 1/7</p>
            <p className="text-lg text-slate-200">
              −0.53pp on a top-1% state ATR of ≈ 3.5–5% (treated-state levels,
              Figs. C-9/C-10) — roughly a seventh of the top-1% state
              income-tax burden.
            </p>
          </div>
          <div className="bg-slate-800 text-white rounded-xl px-7 py-5">
            <p className="text-4xl font-bold text-teal-300 mb-1">≈ 1/4</p>
            <p className="text-lg text-slate-200">
              −0.11 against a Reynolds–Smolensky baseline of ≈ 0.4–0.5 (×100)
              — about a quarter of the redistribution these taxes deliver.
            </p>
          </div>
        </div>
        <p>
          State income taxes redistribute little to begin with — which is
          itself worth one sentence. Dollarizing one number (per top-1%
          household, or as a share of state revenue) would make the result
          legible far beyond this room.
        </p>
        <div className="border-t border-slate-200 pt-4 text-lg text-slate-500 leading-relaxed">
          <p className="font-semibold text-slate-600 mb-1">Minor notes</p>
          <p>
            N = 846 = 47 × 18, but the text says 46 states — is DC in the
            panel? · State which income concept (pre- vs post-federal)
            headline numbers use · “353-fold” rides on a $4M base; report
            levels too · NH has no compliance date (Table 2) and no broad
            income tax — worth one footnote where it enters treatment.
          </p>
        </div>
      </div>
    </Slide>
  );
}
