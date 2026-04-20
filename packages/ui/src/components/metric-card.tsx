import type { ReactNode } from "react";

import { Panel } from "./panel";

export function MetricCard({
  label,
  value,
  detail,
  icon,
}: {
  label: string;
  value: string;
  detail: string;
  icon?: ReactNode;
}) {
  return (
    <Panel className="space-y-3">
      <div className="flex items-center justify-between">
        <span className="text-xs uppercase tracking-[0.24em] text-slate-400">{label}</span>
        <span className="text-slate-300">{icon}</span>
      </div>
      <div className="text-3xl font-semibold tracking-tight text-white">{value}</div>
      <p className="text-sm text-slate-400">{detail}</p>
    </Panel>
  );
}

