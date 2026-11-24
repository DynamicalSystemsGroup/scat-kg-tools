"use strict";
var __create = Object.create;
var __defProp = Object.defineProperty;
var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
var __getOwnPropNames = Object.getOwnPropertyNames;
var __getProtoOf = Object.getPrototypeOf;
var __hasOwnProp = Object.prototype.hasOwnProperty;
var __export = (target, all) => {
  for (var name in all)
    __defProp(target, name, { get: all[name], enumerable: true });
};
var __copyProps = (to, from, except, desc) => {
  if (from && typeof from === "object" || typeof from === "function") {
    for (let key of __getOwnPropNames(from))
      if (!__hasOwnProp.call(to, key) && key !== except)
        __defProp(to, key, { get: () => from[key], enumerable: !(desc = __getOwnPropDesc(from, key)) || desc.enumerable });
  }
  return to;
};
var __toESM = (mod, isNodeMode, target) => (target = mod != null ? __create(__getProtoOf(mod)) : {}, __copyProps(
  // If the importer is in node compatibility mode or this is not an ESM
  // file that has been converted to a CommonJS file using a Babel-
  // compatible transform (i.e. "__esModule" has not been set), then set
  // "default" to the CommonJS "module.exports" for node compatibility.
  isNodeMode || !mod || !mod.__esModule ? __defProp(target, "default", { value: mod, enumerable: true }) : target,
  mod
));
var __toCommonJS = (mod) => __copyProps(__defProp({}, "__esModule", { value: true }), mod);

// src/main.ts
var main_exports = {};
__export(main_exports, {
  default: () => ScatPlugin
});
module.exports = __toCommonJS(main_exports);
var import_obsidian3 = require("obsidian");
var import_node_fs = require("node:fs");
var import_node_os = require("node:os");
var path2 = __toESM(require("node:path"));

// src/group.ts
function groupBySeverity(problems) {
  const out = [];
  for (const severity of ["error", "warning"]) {
    const ps = problems.filter((p) => p.severity === severity);
    if (ps.length > 0) out.push({ severity, problems: ps });
  }
  return out;
}
function counts(problems) {
  return {
    errors: problems.filter((p) => p.severity === "error").length,
    warnings: problems.filter((p) => p.severity === "warning").length
  };
}

// src/format.ts
function location(p) {
  if (p.line === null) return p.file;
  return p.column === null ? `${p.file}:${p.line}` : `${p.file}:${p.line}:${p.column}`;
}
function formatHead(p) {
  const again = p.repeat > 1 ? ` (x${p.repeat})` : "";
  const where = p.where ? ` ${p.where}:` : "";
  return `${p.severity} [${p.rule}] ${location(p)}${where} ${p.what}${again}`.trim();
}
function stateMessage(r) {
  switch (r.status) {
    case "ok":
      return null;
    case "not-a-vault":
      return "This note is not in a SCAT vault: no scat.toml in its folder or above it. Nothing is checked.";
    case "not-a-page":
      return "This note has no `type:` in its frontmatter, so it is not a SCAT page. Nothing is checked.";
    default:
      return r.message || `SCAT reported: ${r.status}`;
  }
}
var SHORT = {
  "not-a-vault": "SCAT: not a SCAT vault",
  "not-a-page": "SCAT: not a page",
  refused: "SCAT: refused",
  "no-scat-kg": "SCAT: scat_kg missing",
  error: "SCAT: check failed"
};
function statusText(report, failed = false) {
  if (failed) return "SCAT: check failed";
  if (report === null) return "SCAT: -";
  if (report.status !== "ok") return SHORT[report.status] ?? "SCAT: check failed";
  const { errors, warnings } = counts(report.problems);
  if (errors === 0 && warnings === 0) return "SCAT: clean";
  return `SCAT: ${errors} error${errors === 1 ? "" : "s"}, ${warnings} warning${warnings === 1 ? "" : "s"}`;
}
function noticeText(report, max = 3) {
  const state = stateMessage(report);
  if (state) return `${statusText(report)}
${state}`;
  if (report.problems.length === 0) return "SCAT: clean";
  const shown = report.problems.slice(0, max).map(formatHead);
  const more = report.problems.length > max ? [`... and ${report.problems.length - max} more (see the SCAT panel)`] : [];
  return [statusText(report), ...shown, ...more].join("\n");
}

// src/paths.ts
var path = __toESM(require("node:path"));
function vaultPath(vaultBase, scatRoot, file) {
  const abs = path.resolve(scatRoot ?? vaultBase, file);
  const rel = path.relative(vaultBase, abs);
  if (rel === "" || rel.startsWith("..") || path.isAbsolute(rel)) return null;
  return rel.split(path.sep).join("/");
}
function uvCandidates(home) {
  return [
    path.join(home, ".local", "bin", "uv"),
    "/opt/homebrew/bin/uv",
    "/usr/local/bin/uv",
    path.join(home, ".cargo", "bin", "uv")
  ];
}
function resolveUv(setting, home, exists) {
  const set = setting.trim();
  if (set) return set;
  return uvCandidates(home).find(exists) ?? "uv";
}

// src/runner.ts
var import_node_child_process = require("node:child_process");

// src/contract.ts
var STATUSES = ["ok", "not-a-vault", "not-a-page", "refused", "no-scat-kg", "error"];
var SUPPORTED_SCHEMA = 1;
var isObj = (v) => typeof v === "object" && v !== null && !Array.isArray(v);
var str = (v, d = "") => typeof v === "string" ? v : d;
var posInt = (v) => typeof v === "number" && Number.isInteger(v) && v >= 1 ? v : null;
function parseProblem(v) {
  if (!isObj(v)) return null;
  const rule = str(v.rule);
  const file = str(v.file);
  if (!rule || !file) return null;
  return {
    rule,
    severity: v.severity === "warning" ? "warning" : "error",
    // unknown severity is treated as blocking
    file,
    where: str(v.where),
    what: str(v.what),
    fix: str(v.fix),
    line: posInt(v.line),
    column: posInt(v.column),
    repeat: posInt(v.repeat) ?? 1
  };
}
function parseReport(raw) {
  let data;
  try {
    data = JSON.parse(raw);
  } catch (e) {
    return { ok: false, error: `output is not JSON (${e.message})` };
  }
  if (!isObj(data)) return { ok: false, error: "output is not a JSON object" };
  if (!Array.isArray(data.problems)) return { ok: false, error: "output has no `problems` list" };
  const schemaVersion = typeof data.schema_version === "number" ? data.schema_version : SUPPORTED_SCHEMA;
  if (schemaVersion > SUPPORTED_SCHEMA) {
    return { ok: false, error: `scat reports schema ${schemaVersion}; this plugin reads ${SUPPORTED_SCHEMA}` };
  }
  const problems = data.problems.map(parseProblem).filter((p) => p !== null);
  const ok = typeof data.ok === "boolean" ? data.ok : !problems.some((p) => p.severity === "error");
  const status = STATUSES.includes(data.status) ? data.status : "ok";
  return {
    ok: true,
    report: { schemaVersion, ok, problems, status, message: str(data.message), root: str(data.root) || null }
  };
}

// src/runner.ts
var TIMEOUT_MS = 18e4;
var spawnRunner = (exe, args, cwd) => new Promise((resolve2) => {
  let stdout = "";
  let stderr = "";
  let timedOut = false;
  const child = (0, import_node_child_process.spawn)(exe, args, { cwd, shell: false });
  const timer = setTimeout(() => {
    timedOut = true;
    child.kill();
  }, TIMEOUT_MS);
  child.stdout.on("data", (d) => stdout += d);
  child.stderr.on("data", (d) => stderr += d);
  child.on("error", (e) => {
    clearTimeout(timer);
    resolve2({ stdout, stderr, exitCode: null, spawnError: e.message });
  });
  child.on("close", (code) => {
    clearTimeout(timer);
    resolve2({ stdout, stderr, exitCode: code, timedOut });
  });
});
function buildArgs(o) {
  const args = ["run", "--quiet", "--project", o.vaultRoot, "python", o.shim, o.page];
  if (o.neighborhood) args.push("--neighborhood");
  return args;
}
async function runCheck(run, o) {
  const r = await run(o.uv, buildArgs(o), o.vaultRoot);
  if (r.spawnError) {
    return {
      ok: false,
      error: `Could not start uv (\`${o.uv}\`): ${r.spawnError}. Install uv, or set "Path to uv" in the SCAT settings to the output of \`which uv\`.`
    };
  }
  if (r.timedOut) return { ok: false, error: "The check took too long and was stopped. Run `uv run python` once in the vault folder in a terminal, then try again." };
  const parsed = parseReport(r.stdout);
  if (parsed.ok) return parsed;
  const detail = r.stderr.trim().split("\n").slice(-3).join(" | ");
  return { ok: false, error: `uv did not return a result (exit ${r.exitCode})${detail ? `: ${detail}` : ""}` };
}

// src/settings.ts
var import_obsidian = require("obsidian");
var DEFAULT_SETTINGS = { uvPath: "", neighborhood: false };
var ScatSettingTab = class extends import_obsidian.PluginSettingTab {
  constructor(app, plugin) {
    super(app, plugin);
    this.plugin = plugin;
  }
  display() {
    this.containerEl.empty();
    new import_obsidian.Setting(this.containerEl).setName("Path to uv").setDesc("Leave empty to look in ~/.local/bin, /opt/homebrew/bin and /usr/local/bin, then PATH. If Obsidian cannot find uv, paste the output of `which uv` here.").addText(
      (t) => t.setPlaceholder("/opt/homebrew/bin/uv").setValue(this.plugin.settings.uvPath).onChange(async (v) => {
        this.plugin.settings.uvPath = v.trim();
        await this.plugin.saveData(this.plugin.settings);
      })
    );
    new import_obsidian.Setting(this.containerEl).setName("Include neighbors").setDesc("Also check pages one link away from the active note.").addToggle(
      (t) => t.setValue(this.plugin.settings.neighborhood).onChange(async (v) => {
        this.plugin.settings.neighborhood = v;
        await this.plugin.saveData(this.plugin.settings);
      })
    );
  }
};

// src/view.ts
var import_obsidian2 = require("obsidian");
var VIEW_TYPE = "scat-panel";
var ScatView = class extends import_obsidian2.ItemView {
  constructor(leaf, onJump) {
    super(leaf);
    this.onJump = onJump;
  }
  getViewType() {
    return VIEW_TYPE;
  }
  getDisplayText() {
    return "SCAT";
  }
  getIcon() {
    return "check-circle";
  }
  /** report null and error null = nothing checked yet; error = the last run failed */
  render(note, report, error) {
    const el = this.contentEl;
    el.empty();
    if (error) {
      el.createDiv({ text: error, cls: "scat-error" });
      return;
    }
    if (report === null) {
      el.createDiv({ text: 'Open a note, or run the command "SCAT: Check active note".' });
      return;
    }
    el.createDiv({ cls: "scat-panel-summary", text: `${note ?? ""}: ${statusText(report)}` });
    const state = stateMessage(report);
    if (state) {
      el.createDiv({ text: state, cls: "scat-state" });
      return;
    }
    if (report.problems.length === 0) {
      el.createDiv({ text: "No problems." });
      return;
    }
    for (const g of groupBySeverity(report.problems)) {
      el.createDiv({ cls: `scat-group-title scat-${g.severity}`, text: `${g.severity}s (${g.problems.length})` });
      for (const p of g.problems) {
        const row = el.createDiv({ cls: "scat-problem" });
        row.createDiv({ cls: "scat-problem-head", text: formatHead(p) });
        if (p.fix) row.createDiv({ cls: "scat-problem-fix", text: p.fix });
        row.addEventListener("click", () => this.onJump(p));
      }
    }
  }
};

// src/main.ts
var ScatPlugin = class extends import_obsidian3.Plugin {
  constructor() {
    super(...arguments);
    this.settings = DEFAULT_SETTINGS;
    this.report = null;
    this.error = null;
    this.note = null;
    this.seq = 0;
  }
  async onload() {
    this.settings = { ...DEFAULT_SETTINGS, ...await this.loadData() };
    this.statusEl = this.addStatusBarItem();
    this.statusEl.setText(statusText(null));
    this.registerView(VIEW_TYPE, (leaf) => new ScatView(leaf, (p) => this.jump(p)));
    this.addSettingTab(new ScatSettingTab(this.app, this));
    this.addCommand({ id: "check-active-note", name: "Check active note", callback: () => this.check(true) });
    this.addCommand({ id: "open-panel", name: "Open panel", callback: () => this.openPanel() });
    const later = (0, import_obsidian3.debounce)(() => this.check(false), 500, true);
    this.registerEvent(this.app.workspace.on("file-open", () => later()));
    this.registerEvent(this.app.vault.on("modify", (f) => {
      if (f === this.app.workspace.getActiveFile()) later();
    }));
  }
  vaultBase() {
    const adapter = this.app.vault.adapter;
    return adapter instanceof import_obsidian3.FileSystemAdapter ? adapter.getBasePath() : null;
  }
  async check(announce) {
    const file = this.app.workspace.getActiveFile();
    const base = this.vaultBase();
    if (!file || file.extension !== "md") return;
    const mine = ++this.seq;
    let report = null;
    let error = null;
    if (!base) {
      error = "SCAT works on a desktop vault stored as folders on disk; this vault is not.";
    } else {
      const shim = path2.join(base, this.app.vault.configDir, "plugins", this.manifest.id, "scat_json.py");
      const r = await runCheck(spawnRunner, {
        uv: resolveUv(this.settings.uvPath, (0, import_node_os.homedir)(), import_node_fs.existsSync),
        vaultRoot: base,
        shim,
        page: path2.join(base, file.path),
        neighborhood: this.settings.neighborhood
      });
      if (r.ok) report = r.report;
      else error = r.error;
    }
    if (mine !== this.seq) return;
    this.note = file.path;
    this.report = report;
    this.error = error;
    this.statusEl.setText(statusText(report, error !== null));
    if (announce) new import_obsidian3.Notice(report ? noticeText(report) : `SCAT: ${error}`, 8e3);
    this.panel()?.render(this.note, this.report, this.error);
  }
  panel() {
    const leaf = this.app.workspace.getLeavesOfType(VIEW_TYPE)[0];
    return leaf ? leaf.view : null;
  }
  async openPanel() {
    let leaf = this.app.workspace.getLeavesOfType(VIEW_TYPE)[0];
    if (!leaf) {
      leaf = this.app.workspace.getRightLeaf(false);
      await leaf.setViewState({ type: VIEW_TYPE, active: true });
    }
    this.app.workspace.revealLeaf(leaf);
    this.panel()?.render(this.note, this.report, this.error);
  }
  /** Open the problem's file at its line. `file` is relative to the SCAT root, which may sit above the vault. */
  async jump(p) {
    const base = this.vaultBase();
    const rel = base ? vaultPath(base, this.report?.root ?? null, p.file) : null;
    const f = rel ? this.app.vault.getAbstractFileByPath(rel) : null;
    if (!(f instanceof import_obsidian3.TFile)) return;
    const line = p.line === null ? 0 : p.line - 1;
    await this.app.workspace.getLeaf(false).openFile(f, { eState: { line } });
  }
};
