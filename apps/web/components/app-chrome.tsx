"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { ReactNode } from "react";

import { navigation } from "@citadel/config";
import { cn } from "@/lib/utils";

export function AppChrome({
  children,
}: {
  children: ReactNode;
}) {
  const pathname = usePathname();
  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top,#10304f,transparent_32%),linear-gradient(180deg,#020814,#071423_38%,#030611)] text-white">
      <div className="pointer-events-none fixed inset-0 bg-grid bg-[size:72px_72px] opacity-[0.08]" />
      <div className="relative mx-auto flex min-h-screen max-w-[1500px] gap-6 px-4 pb-10 pt-5 sm:px-6 lg:px-8">
        <aside className="hidden w-72 shrink-0 flex-col rounded-[32px] border border-white/10 bg-slate-950/70 p-5 backdrop-blur-xl lg:flex">
          <div className="mb-10 space-y-3">
            <div className="inline-flex rounded-full border border-cyan-400/20 bg-cyan-400/10 px-3 py-1 text-[11px] uppercase tracking-[0.34em] text-cyan-100">
              Citadel
            </div>
            <div>
              <div className="text-xl font-semibold tracking-tight">Enterprise Retrieval Intelligence</div>
              <p className="mt-2 text-sm leading-6 text-slate-400">
                Hybrid retrieval, graph expansion, strict citations, and eval-gated delivery.
              </p>
            </div>
          </div>
          <nav className="space-y-2">
            {navigation.map((item) => {
              const active =
                item.href === "/"
                  ? pathname === item.href
                  : pathname === item.href || pathname.startsWith(`${item.href}/`);
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={cn(
                    "flex items-center justify-between rounded-2xl px-4 py-3 text-sm text-slate-300 transition hover:bg-white/5 hover:text-white",
                    active && "bg-white/8 text-white shadow-halo",
                  )}
                >
                  <span>{item.label}</span>
                  <span className="text-xs uppercase tracking-[0.2em] text-slate-500">/</span>
                </Link>
              );
            })}
          </nav>
          <div className="mt-auto rounded-3xl border border-white/10 bg-white/5 p-4 text-sm text-slate-300">
            <div className="mb-2 text-xs uppercase tracking-[0.22em] text-cyan-100/70">
              Operator Notes
            </div>
            Retrieval stays citation-bound even when generation is unavailable. Evidence panels never disappear.
          </div>
        </aside>
        <main className="flex-1 space-y-6">
          <header className="flex flex-col gap-4 rounded-[32px] border border-white/10 bg-slate-950/70 px-5 py-4 backdrop-blur-xl sm:flex-row sm:items-center sm:justify-between">
            <div>
              <div className="text-xs uppercase tracking-[0.26em] text-slate-500">CITADEL // Enterprise Retrieval Intelligence Platform</div>
              <div className="mt-1 text-lg font-medium tracking-tight text-white">Governed knowledge operations for internal docs</div>
            </div>
            <div className="flex gap-2">
              <Link href="/ask" className="rounded-full border border-cyan-300/30 bg-cyan-300/10 px-4 py-2 text-sm text-cyan-50 transition hover:bg-cyan-300/20">
                Open Ask
              </Link>
              <Link href="/status" className="rounded-full border border-white/10 px-4 py-2 text-sm text-slate-200 transition hover:bg-white/5">
                Dependency Status
              </Link>
            </div>
          </header>
          {children}
        </main>
      </div>
    </div>
  );
}
