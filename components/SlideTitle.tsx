import React, { ReactNode } from 'react';

interface SlideTitleProps {
  children: ReactNode;
  className?: string;
}

export default function SlideTitle({ children, className = '' }: SlideTitleProps) {
  return (
    <h1 className={`text-4xl font-bold text-slate-800 leading-tight tracking-tight mb-2 ${className}`}>
      {children}
    </h1>
  );
}
