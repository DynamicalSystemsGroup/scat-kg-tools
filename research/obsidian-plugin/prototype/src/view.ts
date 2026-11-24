import { ItemView, WorkspaceLeaf } from "obsidian";
import type { Problem } from "./contract";
import { formatHead } from "./format";
import { groupBySeverity, counts } from "./group";

export const VIEW_TYPE = "scat-check-panel";

export class ScatView extends ItemView {
  constructor(leaf: WorkspaceLeaf, private onOpen_: (p: Problem) => void) {
    super(leaf);
  }
  getViewType() { return VIEW_TYPE; }
  getDisplayText() { return "SCAT check"; }
  getIcon() { return "check-circle"; }

  /** problems null = nothing checked yet; error = the last run failed */
  render(note: string | null, problems: Problem[] | null, error: string | null) {
    const el = this.contentEl;
    el.empty();
    if (error) { el.createDiv({ text: error, cls: "scat-error" }); return; }
    if (problems === null) { el.createDiv({ text: "Run \"SCAT: check active note\"." }); return; }
    const c = counts(problems);
    el.createDiv({ cls: "scat-panel-summary", text: `${note ?? ""}: ${c.errors} errors, ${c.warnings} warnings` });
    for (const g of groupBySeverity(problems)) {
      el.createDiv({ cls: `scat-group-title scat-${g.severity}`, text: `${g.severity}s (${g.problems.length})` });
      for (const p of g.problems) {
        const row = el.createDiv({ cls: "scat-problem" });
        row.createDiv({ cls: "scat-problem-head", text: formatHead(p) });
        if (p.fix) row.createDiv({ cls: "scat-problem-fix", text: p.fix });
        row.addEventListener("click", () => this.onOpen_(p));
      }
    }
  }
}
