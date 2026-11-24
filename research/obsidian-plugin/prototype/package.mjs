// Deterministic copy of the four files an install needs into dist/scat (or the folder given as the argument).
// Run `npm run build` first; `npm run package` does both.
import { copyFileSync, existsSync, mkdirSync, rmSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const out = resolve(process.argv[2] ?? join(here, "..", "dist", "scat"));
const files = ["main.js", "manifest.json", "styles.css", "scat_json.py"];

for (const f of files) {
  if (!existsSync(join(here, f))) {
    console.error(`missing ${f}; run \`npm run build\` first`);
    process.exit(1);
  }
}
rmSync(out, { recursive: true, force: true });
mkdirSync(out, { recursive: true });
for (const f of files) copyFileSync(join(here, f), join(out, f));
console.log(`packaged ${files.join(", ")} -> ${out}`);
