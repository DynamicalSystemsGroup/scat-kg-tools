// Runs the scat executable. Injectable so logic is testable without a process. No `obsidian` import.
import { spawn } from "node:child_process";
import { parseReport, type ParseResult } from "./contract";

export interface RunResult {
  stdout: string;
  stderr: string;
  exitCode: number | null;
  /** set when the process could not start (for example ENOENT) */
  spawnError?: string;
}

export type Runner = (exe: string, args: string[], cwd: string) => Promise<RunResult>;

export const spawnRunner: Runner = (exe, args, cwd) =>
  new Promise((resolve) => {
    let stdout = "";
    let stderr = "";
    // no shell: arguments are passed as an array, so a note name cannot inject commands
    const child = spawn(exe, args, { cwd, shell: false });
    child.stdout.on("data", (d) => (stdout += d));
    child.stderr.on("data", (d) => (stderr += d));
    child.on("error", (e) => resolve({ stdout, stderr, exitCode: null, spawnError: e.message }));
    child.on("close", (code) => resolve({ stdout, stderr, exitCode: code }));
  });

export interface CheckOptions {
  exe: string;
  vaultRoot: string;
  /** vault-relative path of the note, `/` separators */
  page: string;
  neighborhood?: boolean;
}

export function buildArgs(o: CheckOptions): string[] {
  const args = ["check", o.page, "--root", o.vaultRoot, "--json"];
  if (o.neighborhood) args.push("--neighborhood");
  return args;
}

/** scat exits 1 when there are errors, so a non-zero exit with parseable stdout is a normal result. */
export async function runCheck(run: Runner, o: CheckOptions): Promise<ParseResult> {
  const r = await run(o.exe, buildArgs(o), o.vaultRoot);
  if (r.spawnError) return { ok: false, error: `could not start \`${o.exe}\`: ${r.spawnError}. Set the path to scat in settings.` };
  const parsed = parseReport(r.stdout);
  if (parsed.ok) return parsed;
  const detail = r.stderr.trim().split("\n")[0] ?? "";
  return { ok: false, error: `${parsed.error}${detail ? `; stderr: ${detail}` : ""} (exit ${r.exitCode})` };
}
