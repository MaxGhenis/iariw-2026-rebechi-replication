import React, { ReactNode } from 'react';

export interface SlideProps {
  children: ReactNode;
  className?: string;
  showFooter?: boolean;
  isCover?: boolean;
  isEnd?: boolean;
  isSection?: boolean;
}

export default function Slide({
  children,
  className = '',
  showFooter = true,
  isCover = false,
  isEnd = false,
  isSection = false,
}: SlideProps) {
  const isSpecial = isCover || isEnd || isSection;

  return (
    <div className={`
      relative w-screen h-screen flex flex-col
      ${isSpecial ? 'bg-gradient-to-br from-slate-900 via-slate-800 to-pe-darker text-white justify-center items-center' : 'bg-white'}
      ${className}
    `}>
      {/* Content area */}
      <div className={`
        absolute inset-0
        ${isSpecial ? 'flex items-center justify-center' : 'pt-14 pb-20'}
      `}>
        <div className={`
          w-full h-full
          ${isSpecial ? 'max-w-6xl px-20 flex flex-col justify-center' : 'px-16 flex flex-col'}
        `}>
          {children}
        </div>
      </div>

      {/* Footer */}
      {showFooter && !isSpecial && (
        <div className="absolute bottom-0 left-0 right-0 h-12 bg-slate-800 flex items-center justify-between px-16">
          <div className="text-white text-sm opacity-90 font-medium">
            Discussant: Max Ghenis · PolicyEngine
          </div>
          <div className="text-white text-sm opacity-70">
            Rebechi, Van Kerm, Paradowski, Lepinteur &amp; Rohde · IARIW 2026
          </div>
        </div>
      )}
    </div>
  );
}
