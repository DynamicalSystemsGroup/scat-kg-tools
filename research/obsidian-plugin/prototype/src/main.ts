// Lifecycle only: wires Obsidian to the modules. Logic lives in contract, runner, group, format.
import { FileSystemAdapter, Notice, Plugin, TFile, debounce } from "obsidian";
import type { Problem } from "./contract";
import { noticeText, statusText } from "./format";
import { runCheck, spawnRunner } from "./runner";
import { DEFAULT_SETTINGS, ScatSettingTab, type ScatSettings } from "./settings";
import { ScatView, VIEW_TYPE } from "./view";

export default class ScatPlugin extends Plugin {
  settings: ScatSettings = DEFAULT_SETTINGS;
  private statusEl!: HTMLElement;
  private problems: Problem[] | null = null;
  private error: string | null = null;
  private note: string | null = null;

  async onload() {
    this.settings = { ...DEFAULT_SETTINGS, ...(await this.loadData()) };
    this.statusEl = this.addStatusBarItem();
    this.statusEl.setText(statusText(null));
    this.registerView(VIEW_TYPE, (leaf) => new ScatView(leaf, (p) => this.reveal(p)));
    this.addSettingTab(new ScatSettingTab(this.app, this));

    this.addCommand({ id: "check-active-note", name: "Check active note", callback: () => this.check(true) });
    this.addCommand({ id: "open-panel", name: "Open panel", callback: () => this.openPanel() });

    const later = debounce(() => this.check(false), 500, true);
    this.registerEvent(this.app.workspace.on("file-open", () => later()));
    this.registerEvent(this.app.vault.on("modify", (f) => {
      if (f === this.app.workspace.getActiveFile()) later();
    }));
  }

  async check(announce: boolean) {
    const file = this.app.workspace.getActiveFile();
    const adapter = this.app.vault.adapter;
    if (!file || file.extension !== "md" || !(adapter instanceof FileSystemAdapter)) return;
    const r = await runCheck(spawnRunner, {
      exe: this.settings.scatPath,
      vaultRoot: adapter.getBasePath(),
      page: file.path,
      neighborhood: this.settings.neighborhood,
    });
    this.note = file.path;
    if (r.ok) { this.problems = r.report.problems; this.error = null; }
    else { this.problems = null; this.error = r.error; }
    this.statusEl.setText(statusText(this.problems, !r.ok));
    if (announce) new Notice(r.ok ? noticeText(r.report.problems) : `SCAT: ${r.error}`, 8000);
    this.panel()?.render(this.note, this.problems, this.error);
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
    this.panel()?.render(this.note, this.problems, this.error);
  }

  private async reveal(p: Problem) {
    const f = this.app.vault.getAbstractFileByPath(p.file);
    if (!(f instanceof TFile)) return;
    const line = p.line === null ? 0 : p.line - 1;
    await this.app.workspace.getLeaf(false).openFile(f, { eState: { line } });
  }
}
