import type { Problem, Severity } from "./contract";

export interface Group {
  severity: Severity;
  problems: Problem[];
}

/** Errors first, then warnings; empty groups are omitted; order within a group is kept (scat sorts it). */
export function groupBySeverity(problems: Problem[]): Group[] {
  const out: Group[] = [];
  for (const severity of ["error", "warning"] as Severity[]) {
    const ps = problems.filter((p) => p.severity === severity);
    if (ps.length > 0) out.push({ severity, problems: ps });
  }
  return out;
}

export function counts(problems: Problem[]): { errors: number; warnings: number } {
  return {
    errors: problems.filter((p) => p.severity === "error").length,
    warnings: problems.filter((p) => p.severity === "warning").length,
  };
}
