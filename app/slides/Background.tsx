import React from 'react';
import Slide from '@/components/Slide';
import SlideTitle from '@/components/SlideTitle';
import SlideSubtitle from '@/components/SlideSubtitle';
import { assetPath } from '@/lib/assetPath';

export function QuestionSlide() {
  return (
    <Slide>
      <SlideTitle>Does money in politics change actual policy?</SlideTitle>
      <SlideSubtitle>
        The political effects of Citizens United are documented; the policy
        effects are not
      </SlideSubtitle>
      <div className="flex-1 flex flex-col justify-center pb-10 space-y-6 text-2xl text-slate-700 leading-relaxed max-w-6xl w-full mx-auto">
        <p>
          In the last presidential election, the 100 largest donors gave{' '}
          <span className="font-semibold text-slate-900">$2.4 billion</span>{' '}
          (OpenSecrets).
        </p>
        <p>
          <span className="font-semibold text-slate-900">
            Citizens United v. FEC
          </span>{' '}
          (January 2010) and{' '}
          <span className="font-semibold text-slate-900">
            SpeechNow.org v. FEC
          </span>{' '}
          (March 2010) removed limits on independent political spending by
          corporations, unions, and individuals.
        </p>
        <p>
          A decade of research finds{' '}
          <span className="font-semibold">political</span> effects: higher
          Republican vote shares, more conservative state legislatures
          (Abdul-Razzak et al. 2020; Klumpp et al. 2016; Harvey &amp; Mattia
          2022).
        </p>
        <div className="border-l-4 border-pe-teal pl-6 py-2 bg-teal-50 rounded-r-lg">
          <p className="text-slate-800">
            “What this implies for policy decisions, however, is unclear. Most
            research to date has found no impact on actual policy.”
          </p>
          <p className="text-lg text-slate-500 mt-1">
            This paper supplies the missing link: from campaign finance
            deregulation to tax schedules to inequality.
          </p>
        </div>
      </div>
    </Slide>
  );
}

const TIMELINE = [
  { year: '1947', label: 'Taft–Hartley Act', detail: 'Union contributions banned', highlight: false },
  { year: '1971–75', label: 'FECA + FEC created', detail: 'Contribution and spending limits', highlight: false },
  { year: '1976', label: 'Buckley v. Valeo', detail: 'Spending is speech; contribution limits stand', highlight: false },
  { year: '1990', label: 'Austin v. Michigan', detail: 'States may limit corporate independent expenditures', highlight: false },
  { year: '2002', label: 'BCRA (McCain–Feingold)', detail: 'Soft money and electioneering restricted', highlight: false },
  { year: 'Jan 2010', label: 'Citizens United v. FEC', detail: 'Corporate and union outside spending unlimited; state bans invalidated', highlight: true },
  { year: 'Mar 2010', label: 'SpeechNow.org v. FEC', detail: 'Unlimited contributions to independent-expenditure groups: Super PACs', highlight: true },
  { year: '2014', label: 'McCutcheon v. FEC', detail: 'Aggregate contribution limits struck down', highlight: false },
  { year: '2022', label: 'FEC v. Ted Cruz', detail: 'Post-election contribution limits struck down', highlight: false },
];

export function TimelineSlide() {
  return (
    <Slide>
      <SlideTitle>Sixty years of limits, undone in two rulings</SlideTitle>
      <SlideSubtitle>
        US campaign finance regulation, 1947–2022 (paper Figure 1)
      </SlideSubtitle>
      <div className="flex-1 flex flex-col justify-center pb-10"><div className="relative">
        <div className="absolute left-40 top-0 bottom-0 w-0.5 bg-slate-300" />
        <div className="space-y-2.5">
          {TIMELINE.map((item) => (
            <div key={item.year + item.label} className="flex items-center gap-6">
              <div
                className={`w-32 text-right text-xl font-semibold ${item.highlight ? 'text-pe-teal' : 'text-slate-500'}`}
              >
                {item.year}
              </div>
              <div
                className={`w-4 h-4 rounded-full flex-shrink-0 ${item.highlight ? 'bg-pe-teal ring-4 ring-teal-100' : 'bg-slate-400'}`}
              />
              <div className="flex items-baseline gap-4">
                <span
                  className={`text-xl font-semibold ${item.highlight ? 'text-slate-900' : 'text-slate-700'}`}
                >
                  {item.label}
                </span>
                <span className="text-lg text-slate-500">{item.detail}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
      </div>
    </Slide>
  );
}

export function MapSlide() {
  return (
    <Slide>
      <SlideTitle>
        The natural experiment: 23 states had their own bans
      </SlideTitle>
      <SlideSubtitle>
        Citizens United erased all of them within months — differentially
      </SlideSubtitle>
      <div className="flex-1 min-h-0 flex gap-10 items-center pb-6">
        <div className="w-[38%] space-y-5 text-xl text-slate-700 leading-relaxed">
          <div>
            <p className="font-semibold text-slate-900">
              Corporate <em>and</em> union ban — 13 states in sample
            </p>
            <p className="text-lg text-slate-500">
              AK, AZ, MI, NH, NC, ND, OH, OK, PA, RI, TX, WI, WY
            </p>
          </div>
          <div>
            <p className="font-semibold text-slate-900">
              Corporate ban only — 8 states
            </p>
            <p className="text-lg text-slate-500">
              CT, IA, KY, MA, MN, MT, TN, WV
            </p>
          </div>
          <div>
            <p className="font-semibold text-slate-900">No ban — controls</p>
            <p className="text-lg text-slate-500">
              The remaining states never restricted independent expenditures
            </p>
          </div>
          <p className="pt-2 border-t border-slate-200">
            All bans revised to comply by{' '}
            <span className="font-semibold">November 2010</span>: a sharp,
            court-imposed, differential deregulation. CO and SD (bans adopted
            only in 2002 and 2007) are excluded.
          </p>
        </div>
        <div className="flex-1 h-full flex items-center justify-center">
          <img
            src={assetPath('/figures/fig2-map.png')}
            alt="State campaign regulations before Citizens United"
            className="max-h-full max-w-full object-contain"
          />
        </div>
      </div>
    </Slide>
  );
}

const SPENDING = [
  { row: 'For Democrats', y2004: '60', y2024: '1,062', ratio: '×18' },
  { row: 'For Republicans', y2004: '23', y2024: '763', ratio: '×33' },
  { row: 'Against Democrats', y2004: '4', y2024: '1,411', ratio: '×353' },
  { row: 'Against Republicans', y2004: '7', y2024: '923', ratio: '×132' },
];

export function SpendingSlide() {
  return (
    <Slide>
      <SlideTitle>What followed: an explosion of outside spending</SlideTitle>
      <SlideSubtitle>
        Outside spending by recipient party, $ millions (paper Table 1;
        OpenSecrets)
      </SlideSubtitle>
      <div className="flex-1 flex flex-col justify-center pb-10 max-w-4xl w-full mx-auto">
        <table className="w-full text-2xl">
          <thead>
            <tr className="border-b-2 border-slate-800 text-slate-900">
              <th className="text-left py-3 font-semibold"> </th>
              <th className="text-right py-3 font-semibold">2004</th>
              <th className="text-right py-3 font-semibold">2024</th>
              <th className="text-right py-3 font-semibold text-pe-teal">
                Growth
              </th>
            </tr>
          </thead>
          <tbody>
            {SPENDING.map((r) => (
              <tr key={r.row} className="border-b border-slate-200">
                <td className="py-3 text-slate-700">{r.row}</td>
                <td className="py-3 text-right text-slate-700">{r.y2004}</td>
                <td className="py-3 text-right text-slate-700">{r.y2024}</td>
                <td
                  className={`py-3 text-right font-semibold ${r.ratio === '×353' ? 'text-pe-teal' : 'text-slate-900'}`}
                >
                  {r.ratio}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        <div className="mt-8 space-y-3 text-xl text-slate-700">
          <p>
            Negative spending grew fastest — money spent{' '}
            <em>against</em> Democrats rose 353-fold over twenty years.
          </p>
          <p>
            And it went dark: the share of Super PAC spending with{' '}
            <span className="font-semibold">full donor disclosure</span> fell
            from 77% (2010) to 33% (2024) (paper Table 3).
          </p>
        </div>
      </div>
    </Slide>
  );
}
