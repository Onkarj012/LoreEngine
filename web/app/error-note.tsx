type ErrorNoteProps = { msg: string };

export function ErrorNote({ msg }: ErrorNoteProps) {
  return (
    <p className="m-4 rounded-xl border border-seal/40 bg-seal/10 px-4 py-3 text-sm text-seal">
      {msg}
    </p>
  );
}
