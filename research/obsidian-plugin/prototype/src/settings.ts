import { App, PluginSettingTab, Setting } from "obsidian";
import type ScatPlugin from "./main";

export interface ScatSettings {
  scatPath: string;
  neighborhood: boolean;
}
export const DEFAULT_SETTINGS: ScatSettings = { scatPath: "scat", neighborhood: false };

export class ScatSettingTab extends PluginSettingTab {
  constructor(app: App, private plugin: ScatPlugin) {
    super(app, plugin);
  }
  display(): void {
    this.containerEl.empty();
    new Setting(this.containerEl)
      .setName("Path to scat")
      .setDesc("Full path if Obsidian does not see your shell PATH, for example the output of `which scat`.")
      .addText((t) =>
        t.setValue(this.plugin.settings.scatPath).onChange(async (v) => {
          this.plugin.settings.scatPath = v.trim() || "scat";
          await this.plugin.saveData(this.plugin.settings);
        }),
      );
    new Setting(this.containerEl)
      .setName("Include neighbors")
      .setDesc("Also check pages one link away.")
      .addToggle((t) =>
        t.setValue(this.plugin.settings.neighborhood).onChange(async (v) => {
          this.plugin.settings.neighborhood = v;
          await this.plugin.saveData(this.plugin.settings);
        }),
      );
  }
}
