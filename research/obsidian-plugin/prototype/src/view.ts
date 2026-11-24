import { ItemView, WorkspaceLeaf } from "obsidian";
import type { Problem, Report } from "./contract";
import { formatHead, stateMessage, statusText } from "./format";
import { groupBySeverity } from "./group";

export const VIEW_TYPE = "scat-panel";

export class ScatView extends ItemView {
  constructor(leaf: WorkspaceLeaf, private onJump: (p: Problem) => void) {
    super(leaf);
  }
  getViewType() { return VIEW_TYPE; }
  getDisplayText() { return "SCAT"; }
  getIcon() { return "check-circle"; }

  /** report null and error null = nothing checked yet; error = the last run failed */
  render(note: string | null, report: Report | null, error: string | null) {
    const el = this.contentEl;
    el.empty();
    if (error) { el.createDiv({ text: error, cls: "scat-error" }); return; }
    if (report === null) { el.createDiv({ text: "Open a note, or run the command \"SCAT: Check active note\"." }); return; }
    el.createDiv({ cls: "scat-panel-summary", text: `${note ?? ""}: ${statusText(report)}` });
    const state = stateMessage(report);
    if (state) { el.createDiv({ text: state, cls: "scat-state" }); return; }
    if (report.problems.length === 0) { el.createDiv({ text: "No problems." }); return; }
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
}
