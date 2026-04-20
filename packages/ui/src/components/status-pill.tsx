import { cn } from "../lib/utils";

const palette: Record<string, string> = {
  healthy: "border-emerald-400/30 bg-emerald-400/10 text-emerald-200",
  passed: "border-emerald-400/30 bg-emerald-400/10 text-emerald-200",
  grounded: "border-emerald-400/30 bg-emerald-400/10 text-emerald-200",
  degraded: "border-amber-400/30 bg-amber-400/10 text-amber-100",
  insufficient_evidence: "border-amber-400/30 bg-amber-400/10 text-amber-100",
  failed: "border-rose-400/30 bg-rose-400/10 text-rose-200",
  provider_unavailable: "border-rose-400/30 bg-rose-400/10 text-rose-200",
};

export function StatusPill({ status }: { status: string }) {
  return (
    <span
      className={cn(
        "inline-flex items-center rounded-full border px-2.5 py-1 text-xs font-medium capitalize tracking-wide",
        palette[status] ?? "border-white/15 bg-white/5 text-slate-200",
      )}
    >
      {status.replaceAll("_", " ")}
    </span>
  );
}

