// Path helpers. No `obsidian` import.
import * as path from "node:path";

/**
 * The vault-relative path (with `/`) of a problem's file, or null when it is outside the Obsidian vault.
 * `root` is the SCAT root the shim reports; it can be the vault itself or a folder above it.
 */
export function vaultPath(vaultBase: string, scatRoot: string | null, file: string): string | null {
  const abs = path.resolve(scatRoot ?? vaultBase, file);
  const rel = path.relative(vaultBase, abs);
  if (rel === "" || rel.startsWith("..") || path.isAbsolute(rel)) return null;
  return rel.split(path.sep).join("/");
}

/** Where `uv` lives when Obsidian was started from the Dock and has no shell PATH. */
export function uvCandidates(home: string): string[] {
  return [
    path.join(home, ".local", "bin", "uv"),
    "/opt/homebrew/bin/uv",
    "/usr/local/bin/uv",
    path.join(home, ".cargo", "bin", "uv"),
  ];
}

/** The setting wins; then the first candidate that exists; then plain `uv` (found through PATH, or not at all). */
export function resolveUv(setting: string, home: string, exists: (p: string) => boolean): string {
  const set = setting.trim();
  if (set) return set;
  return uvCandidates(home).find(exists) ?? "uv";
}
