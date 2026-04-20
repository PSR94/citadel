import type { ReactNode } from "react";

import { cn } from "../lib/utils";

export function PageShell({
  eyebrow,
  title,
  description,
  children,
  className,
}: {
  eyebrow: string;
  title: string;
  description: string;
  children: ReactNode;
  className?: string;
}) {
  return (
    <section className={cn("space-y-6", className)}>
      <div className="space-y-3">
        <div className="inline-flex rounded-full border border-white/10 bg-white/5 px-3 py-1 text-xs uppercase tracking-[0.28em] text-cyan-200/80">
          {eyebrow}
        </div>
        <div className="space-y-2">
          <h1 className="max-w-4xl text-4xl font-semibold tracking-tight text-white sm:text-5xl">
            {title}
          </h1>
          <p className="max-w-3xl text-sm leading-7 text-slate-300 sm:text-base">
            {description}
          </p>
        </div>
      </div>
      {children}
    </section>
  );
}

