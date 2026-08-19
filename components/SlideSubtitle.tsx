import React, { ReactNode } from 'react';

interface SlideSubtitleProps {
  children: ReactNode;
  className?: string;
}

export default function SlideSubtitle({ children, className = '' }: SlideSubtitleProps) {
  return (
    <p className={`text-xl text-slate-500 mb-8 ${className}`}>
      {children}
    </p>
  );
}
