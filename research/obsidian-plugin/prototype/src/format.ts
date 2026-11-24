import type { Problem } from "./contract";
import { counts } from "./group";

export function location(p: Problem): string {
  if (p.line === null) return p.file;
  return p.column === null ? `${p.file}:${p.line}` : `${p.file}:${p.line}:${p.column}`;
}

/** One-line message for a notice or a panel row head. */
export function formatHead(p: Problem): string {
  const again = p.repeat > 1 ? ` (x${p.repeat})` : "";
  const where = p.where ? ` ${p.where}:` : "";
  return `${p.severity} [${p.rule}] ${location(p)}${where} ${p.what}${again}`.trim();
}

/** Status-bar text. `null` means no check has run for this note. */
export function statusText(problems: Problem[] | null, failed = false): string {
  if (failed) return "SCAT: check failed";
  if (problems === null) return "SCAT: -";
  const { errors, warnings } = counts(problems);
  if (errors === 0 && warnings === 0) return "SCAT: clean";
  return `SCAT: ${errors} error${errors === 1 ? "" : "s"}, ${warnings} warning${warnings === 1 ? "" : "s"}`;
}

/** Notice text: the summary plus the first few heads. */
export function noticeText(problems: Problem[], max = 3): string {
  if (problems.length === 0) return "SCAT: clean";
  const shown = problems.slice(0, max).map(formatHead);
  const more = problems.length > max ? [`... and ${problems.length - max} more (see the SCAT panel)`] : [];
  return [statusText(problems), ...shown, ...more].join("\n");
}
