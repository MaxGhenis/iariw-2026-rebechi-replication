'use client';

import React, { useEffect, useState } from 'react';
import { CoverSlide, DiscussionDividerSlide, CloseSlide } from './slides/Cover';
import {
  QuestionSlide,
  TimelineSlide,
  MapSlide,
  SpendingSlide,
} from './slides/Background';
import {
  ThisPaperSlide,
  DataSlide,
  OutcomesSlide,
  DesignSlide,
} from './slides/Approach';
import {
  PoliticsSlide,
  MainResultsSlide,
  EventStudySlide,
  RobustnessSlide,
  HeterogeneitySlide,
} from './slides/Results';
import {
  ChannelsSlide,
  UnionSlide,
  FreedomSlide,
  ConclusionsSlide,
} from './slides/Mechanisms';
import {
  Comment1Slide,
  Comment2Slide,
  Comment3Slide,
  Comment4Slide,
} from './slides/Discussion';

const slides = [
  CoverSlide,
  QuestionSlide,
  TimelineSlide,
  MapSlide,
  SpendingSlide,
  ThisPaperSlide,
  DataSlide,
  OutcomesSlide,
  DesignSlide,
  PoliticsSlide,
  MainResultsSlide,
  EventStudySlide,
  RobustnessSlide,
  HeterogeneitySlide,
  ChannelsSlide,
  UnionSlide,
  FreedomSlide,
  ConclusionsSlide,
  DiscussionDividerSlide,
  Comment1Slide,
  Comment2Slide,
  Comment3Slide,
  Comment4Slide,
  CloseSlide,
];

export default function Home() {
  const [currentSlide, setCurrentSlide] = useState(0);

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const s = params.get('slide');
    if (s !== null) {
      const idx = parseInt(s, 10);
      if (!isNaN(idx) && idx >= 0 && idx < slides.length) {
        setCurrentSlide(idx);
      }
    }
  }, []);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'ArrowRight' || e.key === 'ArrowDown' || e.key === ' ') {
        e.preventDefault();
        setCurrentSlide((prev) => Math.min(prev + 1, slides.length - 1));
      } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
        e.preventDefault();
        setCurrentSlide((prev) => Math.max(prev - 1, 0));
      } else if (e.key === 'Home') {
        e.preventDefault();
        setCurrentSlide(0);
      } else if (e.key === 'End') {
        e.preventDefault();
        setCurrentSlide(slides.length - 1);
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  const CurrentSlideComponent = slides[currentSlide];

  return (
    <main className="relative">
      <CurrentSlideComponent />

      {/* Slide counter */}
      <div className="fixed bottom-14 right-4 text-xs text-slate-400 bg-white/80 px-2 py-1 rounded">
        {currentSlide + 1} / {slides.length}
      </div>
    </main>
  );
}
