export function SectionHeading({
  kicker,
  title,
  body,
}: {
  kicker: string;
  title: string;
  body: string;
}) {
  return (
    <div className="space-y-2">
      <div className="text-xs uppercase tracking-[0.24em] text-cyan-200/70">{kicker}</div>
      <h2 className="text-2xl font-semibold tracking-tight text-white">{title}</h2>
      <p className="max-w-3xl text-sm leading-7 text-slate-400">{body}</p>
    </div>
  );
}

