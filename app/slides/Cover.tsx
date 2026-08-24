import React from 'react';
import Slide from '@/components/Slide';

export function CoverSlide() {
  return (
    <Slide isCover>
      <div className="text-center space-y-10">
        <div>
          <h1 className="text-5xl font-bold leading-tight mb-4">
            What Can Money Buy?
          </h1>
          <h2 className="text-3xl font-medium text-slate-200 leading-snug">
            Inequality and Fiscal Policy Implications of
            <br />
            Citizens United v. Federal Election Commission
          </h2>
        </div>

        <div className="text-xl text-slate-200 leading-relaxed">
          <p className="font-semibold">
            Alessio Rebechi¹ · Philippe Van Kerm²³ · Piotr Paradowski³ ·
            Anthony Lepinteur² · Nicholas Rohde⁴
          </p>
          <p className="text-lg text-slate-400 mt-2">
            ¹University of Tasmania · ²University of Luxembourg ·
            ³Luxembourg Income Study · ⁴Griffith University
          </p>
        </div>

        <div className="space-y-2">
          <p className="text-xl text-slate-100">
            IARIW General Conference · Brussels · 28 August 2026
          </p>
          <p className="text-lg text-slate-400">
            Session: Recent laws and their inequality implications
          </p>
        </div>

        <div className="pt-4 border-t border-slate-600 inline-block px-12">
          <p className="text-xl">
            Presented by the discussant:{' '}
            <span className="font-semibold text-teal-300">Max Ghenis</span>{' '}
            (PolicyEngine)
          </p>
          <p className="text-base text-slate-400 mt-1">
            Author response: Philippe Van Kerm
          </p>
        </div>
      </div>
    </Slide>
  );
}

export function DiscussionDividerSlide() {
  return (
    <Slide isSection>
      <div className="text-center space-y-6">
        <h1 className="text-6xl font-bold">Discussion</h1>
        <p className="text-2xl text-slate-300">
          First, a replication — then four comments, from a tax-microsimulation seat
        </p>
      </div>
    </Slide>
  );
}

export function CloseSlide() {
  return (
    <Slide isEnd>
      <div className="space-y-12">
        <h1 className="text-5xl font-bold text-center">
          Questions to open the floor
        </h1>
        <div className="space-y-6 text-2xl text-slate-200 leading-relaxed max-w-5xl mx-auto">
          <p>
            <span className="text-teal-300 font-semibold">Federal analogue.</span>{' '}
            There is no US-without-Citizens-United counterfactual at the federal
            level. Do these state results bound what happened in Congress?
          </p>
          <p>
            <span className="text-teal-300 font-semibold">The 2021–2023 tax-cut wave.</span>{' '}
            Many corporate-and-union-ban states cut income taxes after the
            sample ends in 2021. Does extending the panel sharpen the effect?
          </p>
          <p>
            <span className="text-teal-300 font-semibold">Who actually spent?</span>{' '}
            Your Table 1 shows the two sides near parity by 2020–24 at the federal
            level. What does the state-level ledger look like in the 13 states that
            drive the result?
          </p>
        </div>
        <div className="text-center pt-8 border-t border-slate-600">
          <p className="text-2xl">
            Thank you — and over to <span className="font-semibold">Philippe Van Kerm</span>
          </p>
          <p className="text-lg text-slate-400 mt-2">
            Max Ghenis · max@policyengine.org · slides, memo, replication: github.com/MaxGhenis/iariw-2026-rebechi-replication
          </p>
        </div>
      </div>
    </Slide>
  );
}
