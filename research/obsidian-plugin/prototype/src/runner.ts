// Runs the shim through uv. Injectable so logic is testable without a process. No `obsidian` import.
import { spawn } from "node:child_process";
import { parseReport, type ParseResult } from "./contract";

export interface RunResult {
  stdout: string;
  stderr: string;
  exitCode: number | null;
  /** set when the process could not start (for example ENOENT) */
  spawnError?: string;
  timedOut?: boolean;
}

export type Runner = (exe: string, args: string[], cwd: string) => Promise<RunResult>;

/** The first `uv run` in a vault may build the environment, so the limit is generous. */
export const TIMEOUT_MS = 180_000;

export const spawnRunner: Runner = (exe, args, cwd) =>
  new Promise((resolve) => {
    let stdout = "";
    let stderr = "";
    let timedOut = false;
    // no shell: arguments are passed as an array, so a note name cannot inject commands
    const child = spawn(exe, args, { cwd, shell: false });
    const timer = setTimeout(() => { timedOut = true; child.kill(); }, TIMEOUT_MS);
    child.stdout.on("data", (d) => (stdout += d));
    child.stderr.on("data", (d) => (stderr += d));
    child.on("error", (e) => { clearTimeout(timer); resolve({ stdout, stderr, exitCode: null, spawnError: e.message }); });
    child.on("close", (code) => { clearTimeout(timer); resolve({ stdout, stderr, exitCode: code, timedOut }); });
  });

export interface CheckOptions {
  /** the uv executable: a full path or `uv` */
  uv: string;
  /** the Obsidian vault folder (absolute); it is the uv project and the working folder */
  vaultRoot: string;
  /** absolute path of scat_json.py, next to main.js */
  shim: string;
  /** absolute path of the note */
  page: string;
  neighborhood?: boolean;
}

/** `uv run --project <vault> python <shim> <note> [--neighborhood]`: the vault pins scat_kg, so uv supplies it. */
export function buildArgs(o: CheckOptions): string[] {
  const args = ["run", "--quiet", "--project", o.vaultRoot, "python", o.shim, o.page];
  if (o.neighborhood) args.push("--neighborhood");
  return args;
}

/** A readable form of the command, for logs and for the troubleshooting section. */
export function commandLine(o: CheckOptions): string {
  return [o.uv, ...buildArgs(o)].map((a) => (/\s/.test(a) ? JSON.stringify(a) : a)).join(" ");
}

/** The shim exits 0 whenever it printed JSON; a note with errors is a normal result, not a failure. */
export async function runCheck(run: Runner, o: CheckOptions): Promise<ParseResult> {
  const r = await run(o.uv, buildArgs(o), o.vaultRoot);
  if (r.spawnError) {
    return {
      ok: false,
      error: `Could not start uv (\`${o.uv}\`): ${r.spawnError}. Install uv, or set "Path to uv" in the SCAT settings to the output of \`which uv\`.`,
    };
  }
  if (r.timedOut) return { ok: false, error: "The check took too long and was stopped. Run `uv run python` once in the vault folder in a terminal, then try again." };
  const parsed = parseReport(r.stdout);
  if (parsed.ok) return parsed;
  const detail = r.stderr.trim().split("\n").slice(-3).join(" | ");
  return { ok: false, error: `uv did not return a result (exit ${r.exitCode})${detail ? `: ${detail}` : ""}` };
}
