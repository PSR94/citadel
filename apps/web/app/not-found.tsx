import Link from "next/link";

export default function NotFound() {
  return (
    <div className="rounded-[32px] border border-white/10 bg-slate-950/70 p-8 backdrop-blur-xl">
      <div className="text-xs uppercase tracking-[0.24em] text-slate-500">Not found</div>
      <h1 className="mt-3 text-3xl font-semibold tracking-tight text-white">The requested source or page does not exist.</h1>
      <p className="mt-3 max-w-2xl text-sm leading-7 text-slate-400">
        The current route did not resolve to a real CITADEL surface or document record.
      </p>
      <Link href="/documents" className="mt-6 inline-flex rounded-full border border-white/10 px-4 py-2 text-sm text-slate-200 transition hover:bg-white/5">
        Return to documents
      </Link>
    </div>
  );
}
