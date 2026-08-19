import React from 'react';
import Slide from '@/components/Slide';
import SlideTitle from '@/components/SlideTitle';
import SlideSubtitle from '@/components/SlideSubtitle';
import { assetPath } from '@/lib/assetPath';

export function ChannelsSlide() {
  return (
    <Slide>
      <SlideTitle>Channels: politics predicts taxes — with a residual</SlideTitle>
      <SlideSubtitle>
        Political outcomes as transmission mechanisms (paper Tables 7, 8, C-2)
      </SlideSubtitle>
      <div className="flex-1 flex flex-col justify-center pb-10 space-y-6 max-w-6xl w-full mx-auto text-xl text-slate-700 leading-relaxed">
        <div className="grid grid-cols-2 gap-8">
          <div className="bg-slate-50 border border-slate-200 rounded-xl px-7 py-5">
            <p className="font-semibold text-slate-900 mb-2">
              Political composition moves tax outcomes
            </p>
            <p>
              Republican Senate vote share → redistribution down (RS −0.14*).
              More conservative median ideology → top-1% ATR −0.29**.
              Democratic trifectas and governors → higher top rates and more
              redistribution; Republican control → the reverse.
            </p>
          </div>
          <div className="bg-slate-50 border border-slate-200 rounded-xl px-7 py-5">
            <p className="font-semibold text-slate-900 mb-2">
              …but does not fully explain the ruling’s effect
            </p>
            <p>
              Residualize each tax outcome on vote share, ideology, or
              polarization, then re-run the DiD: corporate-and-union effects
              persist (top 1% ≈ −0.5pp, RS ≈ −0.1, still significant).
            </p>
          </div>
        </div>
        <div className="border-l-4 border-pe-teal pl-6 py-2 bg-teal-50 rounded-r-lg">
          <p>
            Reading: electoral composition carries part of the effect. The
            remainder points to influence that does not show up in seat counts
            — <span className="font-semibold">lobbying, donor pressure, agenda-setting</span>.
          </p>
        </div>
      </div>
    </Slide>
  );
}

export function UnionSlide() {
  return (
    <Slide>
      <SlideTitle>Why the asymmetry? The union counterweight</SlideTitle>
      <SlideSubtitle>
        Union density by pre-existing ban type (paper Figure 6)
      </SlideSubtitle>
      <div className="flex-1 min-h-0 flex gap-10 items-center pb-6">
        <div className="w-[44%] space-y-5 text-xl text-slate-700 leading-relaxed">
          <p>
            Unions send ≈ <span className="font-semibold">87%</span> of their
            contributions to Democrats; corporate money leans Republican
            (2023–24 cycle, OpenSecrets).
          </p>
          <p>
            <span className="font-semibold text-slate-900">
              Corporate-only-ban states
            </span>
            : unions could already spend — and are strongest there. New
            corporate money met an existing counterweight, so competition
            stayed roughly balanced.
          </p>
          <p>
            <span className="font-semibold text-slate-900">
              Corporate-and-union-ban states
            </span>
            : historically Republican-leaning, weaker unions. Lifting both bans
            favored the side with deeper pockets — the regressive tilt.
          </p>
          <p className="text-lg text-slate-500">
            In the authors’ words: the ruling “amplified pre-existing
            asymmetries in political influence.”
          </p>
        </div>
        <div className="flex-1 h-full flex items-center justify-center">
          <img
            src={assetPath('/figures/fig6-uniondensity.png')}
            alt="Union density by ban type"
            className="max-h-full max-w-full object-contain"
          />
        </div>
      </div>
    </Slide>
  );
}

export function FreedomSlide() {
  return (
    <Slide>
      <SlideTitle>Part of a broader market-oriented drift</SlideTitle>
      <SlideSubtitle>
        Economic freedom (Fraser) and regulatory policy (Cato) indices by ban
        type (paper Figure 7)
      </SlideSubtitle>
      <div className="flex-1 min-h-0 flex flex-col gap-6 pb-6">
        <div className="flex-1 flex items-center justify-center">
          <img
            src={assetPath('/figures/fig7-econfreedom.png')}
            alt="Business friendly environment indicators"
            className="max-h-full max-w-full object-contain"
          />
        </div>
        <p className="text-xl text-slate-700 leading-relaxed max-w-5xl">
          After 2010, both indices rise most in the states that had banned both
          corporate and union spending — descriptive, but consistent with the
          tax findings: a policy environment tilting toward business interests,
          not just a one-off rate cut.
        </p>
      </div>
    </Slide>
  );
}

export function ConclusionsSlide() {
  return (
    <Slide>
      <SlideTitle>The authors’ conclusions</SlideTitle>
      <SlideSubtitle>
        Citizens United changed not only who legislates, but what they
        legislate
      </SlideSubtitle>
      <div className="flex-1 flex flex-col justify-center pb-10 space-y-6 max-w-5xl w-full mx-auto text-2xl text-slate-700 leading-relaxed">
        <p>
          <span className="font-bold text-pe-teal">1.</span> Where both
          corporate and union bans fell, state income taxes became{' '}
          <span className="font-semibold text-slate-900">
            persistently less progressive
          </span>
          : lower top-group rates, less redistribution, higher post-tax
          inequality.
        </p>
        <p>
          <span className="font-bold text-pe-teal">2.</span> Effects unfolded{' '}
          <span className="font-semibold text-slate-900">gradually</span> —
          policy responds over a decade, not an election cycle.
        </p>
        <p>
          <span className="font-bold text-pe-teal">3.</span> Transmission runs
          partly through{' '}
          <span className="font-semibold text-slate-900">
            electoral composition
          </span>
          , partly through influence beyond it.
        </p>
        <div className="border-l-4 border-pe-teal pl-6 py-3 bg-teal-50 rounded-r-lg text-xl">
          <p className="text-slate-800">
            “Wealthy individuals and corporations can influence policy agendas
            by financing campaigns and supporting organizations that promote
            market-oriented and conservative ideologies, resulting in fiscal
            policies that disproportionately favor their interests (‘wingnut
            welfare’).”
          </p>
        </div>
      </div>
    </Slide>
  );
}
