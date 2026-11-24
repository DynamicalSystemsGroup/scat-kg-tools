import { describe, expect, it } from "vitest";
import { parseReport } from "../src/contract";
import { NO_NOTE_PANEL, NO_NOTE_STATUS, isCheckable, noticeText, stateMessage, statusText } from "../src/format";
import { resolveUv, uvCandidates, vaultPath } from "../src/paths";
import { commandLine } from "../src/runner";

function report(o: object) {
  const r = parseReport(JSON.stringify({ problems: [], ...o }));
  if (!r.ok) throw new Error(r.error);
  return r.report;
}

describe("states from the shim", () => {
  it("reads status, message and root; a payload without status is ok", () => {
    expect(report({}).status).toBe("ok");
    const r = report({ status: "not-a-vault", message: "m", root: "/v" });
    expect(r).toMatchObject({ status: "not-a-vault", message: "m", root: "/v" });
    expect(report({ status: "weird" }).status).toBe("ok");
  });
  it("says so when the note is outside a SCAT vault", () => {
    const r = report({ status: "not-a-vault" });
    expect(stateMessage(r)).toContain("not in a SCAT vault");
    expect(statusText(r)).toBe("SCAT: not a SCAT vault");
    expect(noticeText(r)).toContain("Nothing is checked");
  });
  it("says nothing is checked for a note with no type", () => {
    const r = report({ status: "not-a-page" });
    expect(stateMessage(r)).toContain("no `type:`");
    expect(stateMessage(r)).toContain("Nothing is checked");
    expect(statusText(r)).toBe("SCAT: not a page");
  });
  it("shows the shim's own words for a refusal or a missing scat_kg", () => {
    expect(stateMessage(report({ status: "refused", message: "refused x: no page" }))).toBe("refused x: no page");
    expect(statusText(report({ status: "no-scat-kg" }))).toBe("SCAT: scat_kg missing");
    expect(stateMessage(report({ status: "ok" }))).toBeNull();
  });
});

describe("no note to check", () => {
  it("accepts only a Markdown file", () => {
    expect(isCheckable({ extension: "md" })).toBe(true);
    expect(isCheckable({ extension: "png" })).toBe(false);
    expect(isCheckable(null)).toBe(false);
    expect(isCheckable(undefined)).toBe(false);
  });
  it("has its own neutral wording, not a previous result", () => {
    expect(NO_NOTE_STATUS).toBe("SCAT: no note");
    expect(NO_NOTE_PANEL).toBe("Open a Markdown note.");
  });
});

describe("finding uv", () => {
  const home = "/Users/me";
  it("lists the three usual places in order", () => {
    expect(uvCandidates(home).slice(0, 3)).toEqual(["/Users/me/.local/bin/uv", "/opt/homebrew/bin/uv", "/usr/local/bin/uv"]);
  });
  it("prefers the setting, then the first existing candidate, then plain uv", () => {
    expect(resolveUv(" /x/uv ", home, () => true)).toBe("/x/uv");
    expect(resolveUv("", home, (p) => p === "/opt/homebrew/bin/uv" || p === "/usr/local/bin/uv")).toBe("/opt/homebrew/bin/uv");
    expect(resolveUv("", home, () => false)).toBe("uv");
  });
});

describe("jump target", () => {
  it("maps a root-relative file to a vault-relative path", () => {
    expect(vaultPath("/v", "/v", "concern/a.md")).toBe("concern/a.md");
    expect(vaultPath("/v", null, "a.md")).toBe("a.md");
  });
  it("handles a SCAT root above the vault, and a file outside the vault", () => {
    expect(vaultPath("/r/sub", "/r", "sub/a.md")).toBe("a.md");
    expect(vaultPath("/r/sub", "/r", "other/a.md")).toBeNull();
  });
});

describe("command line", () => {
  it("quotes only what has spaces", () => {
    const line = commandLine({ uv: "uv", vaultRoot: "/My Vault", shim: "/My Vault/s.py", page: "/My Vault/a.md" });
    expect(line).toBe('uv run --quiet --project "/My Vault" python "/My Vault/s.py" "/My Vault/a.md"');
  });
});
