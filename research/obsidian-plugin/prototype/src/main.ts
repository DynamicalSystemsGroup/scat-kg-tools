// Lifecycle only: wires Obsidian to the modules. Logic lives in contract, runner, paths, group, format.
import { FileSystemAdapter, Notice, Plugin, TFile, debounce } from "obsidian";
import { existsSync } from "node:fs";
import { homedir } from "node:os";
import * as path from "node:path";
import type { Problem, Report } from "./contract";
import { noticeText, statusText } from "./format";
import { resolveUv, vaultPath } from "./paths";
import { runCheck, spawnRunner } from "./runner";
import { DEFAULT_SETTINGS, ScatSettingTab, type ScatSettings } from "./settings";
import { ScatView, VIEW_TYPE } from "./view";

export default class ScatPlugin extends Plugin {
  settings: ScatSettings = DEFAULT_SETTINGS;
  private statusEl!: HTMLElement;
  private report: Report | null = null;
  private error: string | null = null;
  private note: string | null = null;
  private seq = 0;

  async onload() {
    this.settings = { ...DEFAULT_SETTINGS, ...(await this.loadData()) };
    this.statusEl = this.addStatusBarItem();
    this.statusEl.setText(statusText(null));
    this.registerView(VIEW_TYPE, (leaf) => new ScatView(leaf, (p) => this.jump(p)));
    this.addSettingTab(new ScatSettingTab(this.app, this));

    this.addCommand({ id: "check-active-note", name: "Check active note", callback: () => this.check(true) });
    this.addCommand({ id: "open-panel", name: "Open panel", callback: () => this.openPanel() });

    // rerun on file open and on save; the modify event fires on every auto-save, so debounce it
    const later = debounce(() => this.check(false), 500, true);
    this.registerEvent(this.app.workspace.on("file-open", () => later()));
    this.registerEvent(this.app.vault.on("modify", (f) => {
      if (f === this.app.workspace.getActiveFile()) later();
    }));
  }

  private vaultBase(): string | null {
    const adapter = this.app.vault.adapter;
    return adapter instanceof FileSystemAdapter ? adapter.getBasePath() : null;
  }

  async check(announce: boolean) {
    const file = this.app.workspace.getActiveFile();
    const base = this.vaultBase();
    if (!file || file.extension !== "md") return;
    const mine = ++this.seq;
    let report: Report | null = null;
    let error: string | null = null;
    if (!base) {
      error = "SCAT works on a desktop vault stored as folders on disk; this vault is not.";
    } else {
      const shim = path.join(base, this.app.vault.configDir, "plugins", this.manifest.id, "scat_json.py");
      const r = await runCheck(spawnRunner, {
        uv: resolveUv(this.settings.uvPath, homedir(), existsSync),
        vaultRoot: base,
        shim,
        page: path.join(base, file.path),
        neighborhood: this.settings.neighborhood,
      });
      if (r.ok) report = r.report; else error = r.error;
    }
    if (mine !== this.seq) return; // a newer check started; drop this one
    this.note = file.path;
    this.report = report;
    this.error = error;
    this.statusEl.setText(statusText(report, error !== null));
    if (announce) new Notice(report ? noticeText(report) : `SCAT: ${error}`, 8000);
    this.panel()?.render(this.note, this.report, this.error);
  }

  private panel(): ScatView | null {
    const leaf = this.app.workspace.getLeavesOfType(VIEW_TYPE)[0];
    return leaf ? (leaf.view as ScatView) : null;
  }

  async openPanel() {
    let leaf = this.app.workspace.getLeavesOfType(VIEW_TYPE)[0];
    if (!leaf) {
      leaf = this.app.workspace.getRightLeaf(false)!;
      await leaf.setViewState({ type: VIEW_TYPE, active: true });
    }
    this.app.workspace.revealLeaf(leaf);
    this.panel()?.render(this.note, this.report, this.error);
  }

  /** Open the problem's file at its line. `file` is relative to the SCAT root, which may sit above the vault. */
  private async jump(p: Problem) {
    const base = this.vaultBase();
    const rel = base ? vaultPath(base, this.report?.root ?? null, p.file) : null;
    const f = rel ? this.app.vault.getAbstractFileByPath(rel) : null;
    if (!(f instanceof TFile)) return;
    const line = p.line === null ? 0 : p.line - 1;
    await this.app.workspace.getLeaf(false).openFile(f, { eState: { line } });
  }
}
