import { App, PluginSettingTab, Setting } from "obsidian";
import type ScatPlugin from "./main";

export interface ScatSettings {
  /** empty = look in the usual places, then PATH */
  uvPath: string;
  neighborhood: boolean;
}
export const DEFAULT_SETTINGS: ScatSettings = { uvPath: "", neighborhood: false };

export class ScatSettingTab extends PluginSettingTab {
  constructor(app: App, private plugin: ScatPlugin) {
    super(app, plugin);
  }
  display(): void {
    this.containerEl.empty();
    new Setting(this.containerEl)
      .setName("Path to uv")
      .setDesc("Leave empty to look in ~/.local/bin, /opt/homebrew/bin and /usr/local/bin, then PATH. If Obsidian cannot find uv, paste the output of `which uv` here.")
      .addText((t) =>
        t.setPlaceholder("/opt/homebrew/bin/uv").setValue(this.plugin.settings.uvPath).onChange(async (v) => {
          this.plugin.settings.uvPath = v.trim();
          await this.plugin.saveData(this.plugin.settings);
        }),
      );
    new Setting(this.containerEl)
      .setName("Include neighbors")
      .setDesc("Also check pages one link away from the active note.")
      .addToggle((t) =>
        t.setValue(this.plugin.settings.neighborhood).onChange(async (v) => {
          this.plugin.settings.neighborhood = v;
          await this.plugin.saveData(this.plugin.settings);
        }),
      );
  }
}
