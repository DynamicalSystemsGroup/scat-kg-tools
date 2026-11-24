// "Works when copied": package the plugin, install it into a scratch vault the way a user does,
// and run the plugin's own runCheck (real uv, real shim, real scat_kg). Skipped without uv or the template.
import { execFileSync, spawnSync } from "node:child_process";
import { cpSync, existsSync, mkdirSync, readdirSync, rmSync, writeFileSync } from "node:fs";
import { homedir } from "node:os";
import { join } from "node:path";
import { describe, expect, it } from "vitest";
import { commandLine, runCheck, spawnRunner } from "../src/runner";

const template = process.env.SCAT_TEMPLATE ?? join(homedir(), "Documents/GitHub/scat-kg-template");
const scratch = process.env.SCAT_SCRATCH ?? "/private/tmp/claude-501/scat-rs1";
const haveUv = spawnSync("uv", ["--version"]).status === 0;
const can = haveUv && existsSync(join(template, "scat.toml")) && existsSync(join(__dirname, "..", "main.js"));

describe.skipIf(!can)("plugin folder copied into a vault", () => {
  const vault = join(scratch, "vitest-vault");
  const plugin = join(vault, ".obsidian", "plugins", "scat");
  const seeded = `---\ntype: concern\nstatus: done\ntitle: "Seeded"\ndescription: "x"\nconflicts:\n  - "[[no-such-page]]"\n---\n\nSee [[also-missing]].\n`;

  const check = async (note: string, neighborhood = false) => {
    const o = { uv: "uv", vaultRoot: vault, shim: join(plugin, "scat_json.py"), page: join(vault, note), neighborhood };
    console.log("COMMAND:", commandLine(o)); // the exact line the plugin runs
    const r = await runCheck(spawnRunner, o);
    if (!r.ok) throw new Error(r.error);
    return r.report;
  };

  it("sets up the vault and installs the packaged folder", () => {
    rmSync(vault, { recursive: true, force: true });
    mkdirSync(scratch, { recursive: true });
    cpSync(template, vault, { recursive: true, filter: (s) => !/[\\/](\.git|\.venv)$/.test(s) });
    execFileSync(process.execPath, [join(__dirname, "..", "package.mjs"), plugin]);
    expect(readdirSync(plugin).sort()).toEqual(["main.js", "manifest.json", "scat_json.py", "styles.css"]);
    writeFileSync(join(vault, "concern", "seeded.md"), seeded);
  });

  it("reports the case study's warning with line and exact fix", async () => {
    const r = await check("scenario-coded/notes-at-a-chatham-house-session-coded.md");
    expect(r.status).toBe("ok");
    expect(r.ok).toBe(true);
    expect(r.problems).toHaveLength(1);
    expect(r.problems[0]).toMatchObject({ rule: "SCAT-CONFLICT-BOTH", severity: "warning", line: 11 });
    expect(r.problems[0].fix.startsWith("Fix: none needed")).toBe(true);
  });

  it("reports the seeded defects as errors", async () => {
    const r = await check("concern/seeded.md");
    expect(r.ok).toBe(false);
    expect(r.problems.map((p) => [p.rule, p.line])).toEqual([["SCAT-LINK-DANGLING", 7], ["SCAT-LINK-DANGLING-BODY", 10]]);
  });

  it("says nothing is checked for a note without type", async () => {
    const r = await check("README.md");
    expect(r.status).toBe("not-a-page");
  });

  it("reports a missing uv with the fix", async () => {
    const r = await runCheck(spawnRunner, { uv: "/nonexistent/uv", vaultRoot: vault, shim: "x", page: "y" });
    expect(!r.ok && r.error).toContain("Path to uv");
  });
});
