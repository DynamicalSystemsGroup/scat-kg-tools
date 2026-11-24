import type { Problem, Report } from "./contract";
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

/** The sentence a state shows in the panel, or null when the note was checked. */
export function stateMessage(r: Report): string | null {
  switch (r.status) {
    case "ok": return null;
    case "not-a-vault": return "This note is not in a SCAT vault: no scat.toml in its folder or above it. Nothing is checked.";
    case "not-a-page": return "This note has no `type:` in its frontmatter, so it is not a SCAT page. Nothing is checked.";
    default: return r.message || `SCAT reported: ${r.status}`;
  }
}

const SHORT: Record<string, string> = {
  "not-a-vault": "SCAT: not a SCAT vault",
  "not-a-page": "SCAT: not a page",
  refused: "SCAT: refused",
  "no-scat-kg": "SCAT: scat_kg missing",
  error: "SCAT: check failed",
};

/** Status-bar text. `null` means no check has run for this note. */
export function statusText(report: Report | null, failed = false): string {
  if (failed) return "SCAT: check failed";
  if (report === null) return "SCAT: -";
  if (report.status !== "ok") return SHORT[report.status] ?? "SCAT: check failed";
  const { errors, warnings } = counts(report.problems);
  if (errors === 0 && warnings === 0) return "SCAT: clean";
  return `SCAT: ${errors} error${errors === 1 ? "" : "s"}, ${warnings} warning${warnings === 1 ? "" : "s"}`;
}

/** Notice text: the summary plus the first few heads, or the state message. */
export function noticeText(report: Report, max = 3): string {
  const state = stateMessage(report);
  if (state) return `${statusText(report)}\n${state}`;
  if (report.problems.length === 0) return "SCAT: clean";
  const shown = report.problems.slice(0, max).map(formatHead);
  const more = report.problems.length > max ? [`... and ${report.problems.length - max} more (see the SCAT panel)`] : [];
  return [statusText(report), ...shown, ...more].join("\n");
}
