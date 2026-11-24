// The JSON the plugin expects from `scat check --json`. See JSON-CONTRACT.md. No `obsidian` import.

export type Severity = "error" | "warning";

export interface Problem {
  rule: string;
  severity: Severity;
  file: string;
  where: string;
  what: string;
  fix: string;
  line: number | null;
  column: number | null;
  repeat: number;
}

export interface Report {
  schemaVersion: number;
  ok: boolean;
  problems: Problem[];
}

export type ParseResult = { ok: true; report: Report } | { ok: false; error: string };

export const SUPPORTED_SCHEMA = 1;

const isObj = (v: unknown): v is Record<string, unknown> =>
  typeof v === "object" && v !== null && !Array.isArray(v);

const str = (v: unknown, d = ""): string => (typeof v === "string" ? v : d);
const posInt = (v: unknown): number | null =>
  typeof v === "number" && Number.isInteger(v) && v >= 1 ? v : null;

/** Tolerant: a problem needs `rule` and `file`; every other field falls back. Unknown fields are ignored. */
export function parseProblem(v: unknown): Problem | null {
  if (!isObj(v)) return null;
  const rule = str(v.rule);
  const file = str(v.file);
  if (!rule || !file) return null;
  return {
    rule,
    severity: v.severity === "warning" ? "warning" : "error", // unknown severity is treated as blocking
    file,
    where: str(v.where),
    what: str(v.what),
    fix: str(v.fix),
    line: posInt(v.line),
    column: posInt(v.column),
    repeat: posInt(v.repeat) ?? 1,
  };
}

export function parseReport(raw: string): ParseResult {
  let data: unknown;
  try {
    data = JSON.parse(raw);
  } catch (e) {
    return { ok: false, error: `output is not JSON (${(e as Error).message})` };
  }
  if (!isObj(data)) return { ok: false, error: "output is not a JSON object" };
  if (!Array.isArray(data.problems)) return { ok: false, error: "output has no `problems` list" };
  const schemaVersion = typeof data.schema_version === "number" ? data.schema_version : SUPPORTED_SCHEMA;
  if (schemaVersion > SUPPORTED_SCHEMA) {
    return { ok: false, error: `scat reports schema ${schemaVersion}; this plugin reads ${SUPPORTED_SCHEMA}` };
  }
  const problems = data.problems.map(parseProblem).filter((p): p is Problem => p !== null);
  const ok = typeof data.ok === "boolean" ? data.ok : !problems.some((p) => p.severity === "error");
  return { ok: true, report: { schemaVersion, ok, problems } };
}
