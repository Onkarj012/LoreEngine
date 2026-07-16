import { AskBox } from "./ask-box";

export default function Home() {
  return (
    <main className="relative min-h-dvh bg-black text-white">
      <div className="pointer-events-none absolute inset-0 -z-10 bg-grid" />
      <div className="pointer-events-none absolute inset-0 -z-10 bg-[radial-gradient(680px_360px_at_50%_-8%,rgba(255,255,255,0.07),transparent_70%)]" />
      <div className="mx-auto max-w-2xl px-6 py-24">
        <AskBox />
      </div>
    </main>
  );
}
