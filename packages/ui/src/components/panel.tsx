import type { HTMLAttributes, ReactNode } from "react";

import { cn } from "../lib/utils";

export function Panel({
  className,
  children,
  ...props
}: HTMLAttributes<HTMLDivElement> & { children: ReactNode }) {
  return (
    <div
      className={cn(
        "rounded-3xl border border-white/10 bg-slate-950/70 p-5 shadow-[0_0_0_1px_rgba(255,255,255,0.04),0_30px_80px_rgba(3,7,18,0.6)] backdrop-blur-xl",
        className,
      )}
      {...props}
    >
      {children}
    </div>
  );
}

