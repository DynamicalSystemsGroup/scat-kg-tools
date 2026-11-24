import { describe, expect, it } from "vitest";
import { parseReport } from "../src/contract";
import { counts, groupBySeverity } from "../src/group";
import { formatHead, noticeText, statusText } from "../src/format";
import { buildArgs, runCheck, type Runner } from "../src/runner";

const good = JSON.stringify({
  schema_version: 1,
  ok: false,
  problems: [
    { rule: "SCAT-NAME", severity: "error", file: "a.md", where: "field `name`", what: "bad", fix: "Fix: rename", line: 3, column: 1, repeat: 2 },
    { rule: "SCAT-MENTION", severity: "warning", file: "a.md", where: "text `x`", what: "plain", fix: "Fix: link it", line: 9, column: null },
  ],
});

function parsed(raw: string) {
  const r = parseReport(raw);
  if (!r.ok) throw new Error(r.error);
  return r.report;
}

describe("parseReport", () => {
  it("parses a good payload", () => {
    const r = parsed(good);
    expect(r.ok).toBe(false);
    expect(r.problems).toHaveLength(2);
    expect(r.problems[0]).toMatchObject({ rule: "SCAT-NAME", line: 3, column: 1, repeat: 2 });
  });
  it("fills missing optional fields", () => {
    const r = parsed(JSON.stringify({ problems: [{ rule: "SCAT-FM-PARSE", file: "b.md" }] }));
    expect(r.problems[0]).toMatchObject({ severity: "error", line: null, column: null, repeat: 1, fix: "", where: "" });
    expect(r.ok).toBe(false); // derived from the problems
  });
  it("rejects malformed JSON with a message", () => {
    const r = parseReport("scat: command not found");
    expect(r.ok).toBe(false);
  });
  it("rejects JSON without a problems list and a newer schema", () => {
    expect(parseReport("{}").ok).toBe(false);
    expect(parseReport('{"schema_version": 9, "problems": []}').ok).toBe(false);
  });
  it("accepts an empty problem list", () => {
    const r = parsed('{"schema_version":1,"ok":true,"problems":[]}');
    expect(r.problems).toEqual([]);
    expect(r.ok).toBe(true);
  });
  it("drops entries without a rule or file", () => {
    expect(parsed('{"problems":[{"rule":"X"},42,null]}').problems).toEqual([]);
  });
});

describe("grouping and formatting", () => {
  const ps = parsed(good).problems;
  it("groups errors before warnings and omits empty groups", () => {
    expect(groupBySeverity(ps).map((g) => g.severity)).toEqual(["error", "warning"]);
    expect(groupBySeverity([ps[1]]).map((g) => g.severity)).toEqual(["warning"]);
    expect(groupBySeverity([])).toEqual([]);
    expect(counts(ps)).toEqual({ errors: 1, warnings: 1 });
  });
  it("makes status-bar text", () => {
    expect(statusText(parsed(good))).toBe("SCAT: 1 error, 1 warning");
    expect(statusText(parsed('{"problems":[]}'))).toBe("SCAT: clean");
    expect(statusText(null)).toBe("SCAT: -");
    expect(statusText(null, true)).toBe("SCAT: check failed");
  });
  it("formats a message head like the CLI", () => {
    expect(formatHead(ps[0])).toBe("error [SCAT-NAME] a.md:3:1 field `name`: bad (x2)");
    expect(formatHead(ps[1])).toBe("warning [SCAT-MENTION] a.md:9 text `x`: plain");
  });
  it("truncates notice text", () => {
    expect(noticeText(parsed(good), 1).split("\n")).toHaveLength(3);
  });
});

describe("runCheck with an injected runner", () => {
  const opts = { uv: "uv", vaultRoot: "/v", shim: "/v/.obsidian/plugins/scat/scat_json.py", page: "/v/a.md" };
  it("builds args without a shell", () => {
    expect(buildArgs({ ...opts, neighborhood: true })).toEqual([
      "run", "--quiet", "--project", "/v", "python", "/v/.obsidian/plugins/scat/scat_json.py", "/v/a.md", "--neighborhood",
    ]);
    expect(buildArgs(opts)).not.toContain("--neighborhood");
  });
  it("treats exit 1 with JSON as a normal result", async () => {
    const run: Runner = async () => ({ stdout: good, stderr: "", exitCode: 1 });
    const r = await runCheck(run, opts);
    expect(r.ok && r.report.problems.length).toBe(2);
  });
  it("reports a missing executable with the fix", async () => {
    const run: Runner = async () => ({ stdout: "", stderr: "", exitCode: null, spawnError: "spawn scat ENOENT" });
    const r = await runCheck(run, opts);
    expect(!r.ok && r.error).toContain("Path to uv");
  });
  it("reports a timeout", async () => {
    const run: Runner = async () => ({ stdout: "", stderr: "", exitCode: null, timedOut: true });
    const r = await runCheck(run, opts);
    expect(!r.ok && r.error).toContain("too long");
  });
  it("reports non-JSON output with stderr", async () => {
    const run: Runner = async () => ({ stdout: "usage: scat", stderr: "error: Failed to resolve scat-kg", exitCode: 2 });
    const r = await runCheck(run, opts);
    expect(!r.ok && r.error).toContain("Failed to resolve");
  });
});
