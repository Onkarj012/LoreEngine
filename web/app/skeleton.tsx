export function Skeleton() {
  return (
    <div className="m-4 animate-pulse space-y-3 rounded-xl border border-white/10 bg-white/5 p-5">
      <div className="h-4 w-3/4 rounded bg-white/10" />
      <div className="h-4 w-full rounded bg-white/10" />
      <div className="h-4 w-5/6 rounded bg-white/10" />
    </div>
  );
}
