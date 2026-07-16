type ChipProps = { index: number; source: string; score: number };

export function CitationChip({ index, source, score }: ChipProps) {
  return (
    <span className="chip">
      <b>[{index}]</b> {source} . {score.toFixed(2)}
    </span>
  );
}
