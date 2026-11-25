"""Check work-packages/metrics.jsonl against the estimation practice (ORG.md, "Estimation data"; log D-061).

Usage:
    python3 work-packages/check_metrics.py               # the whole log (CI runs this)
    python3 work-packages/check_metrics.py --accept WP10  # also: WP10 is ready for acceptance

Standard library only. Records on lines up to HISTORY_LINES (everything before WP10's first record) are history and
only need to parse; the practice is enforced from WP10 on.
The latest record per unit, in file order, is authoritative (metrics.md).
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

LOG = Path(__file__).with_name("metrics.jsonl")
HISTORY_LINES = (
    251  # the log's length when WP10 was approved (log D-058); D-061 applies to every later line
)
FUTURE_SLACK = timedelta(minutes=5)  # a record may be stamped this far ahead of the clock
SCALE = {1, 2, 3, 5, 8}
STATES = {"queued", "in flight", "in review", "done", "blocked"}
MODELS = {"sonnet", "haiku", "opus"}


def identity(r):
    return (r["kind"], r.get("unit") if r["kind"] == "unit" else r.get("iteration"))


def superseded_lines(records):
    """Lines whose record a later record corrects: same identity, `corrects` equal to its ts, one to one."""
    gone = set()
    for i, (n, _, r) in enumerate(records):
        if "corrects" not in r:
            continue
        for m, _, old in records[:i]:
            if m not in gone and identity(old) == identity(r) and old["ts"] == r["corrects"]:
                gone.add(m)
                break
    return gone


def main(argv):
    now = datetime.now().astimezone()
    accept = argv[argv.index("--accept") + 1] if "--accept" in argv else None
    problems = []
    records = []
    for n, line in enumerate(LOG.read_text().splitlines(), 1):
        if not line.strip():
            continue
        try:
            r = json.loads(line)
            ts = datetime.fromisoformat(r["ts"])
            if ts.tzinfo is None:
                raise ValueError("ts has no timezone")
            if r.get("kind") not in ("unit", "iteration"):
                raise ValueError(f"kind {r.get('kind')!r}")
        except (ValueError, KeyError, TypeError) as e:
            problems.append(f"line {n}: not a valid record ({e})")
            continue
        records.append((n, ts, r))

    gone = superseded_lines(records)
    for n, ts, r in records:
        if n not in gone and ts > now + FUTURE_SLACK:
            ahead = ts - now
            problems.append(
                f"line {n}: ts is in the future ({r['ts']} is {ahead} ahead of the clock, "
                f"more than {FUTURE_SLACK}); stamp the real time, or correct it with a later record"
            )

    current = [(n, ts, r) for n, ts, r in records if n > HISTORY_LINES]
    units = {}  # unit -> list of (line, record), file order
    prev_ts = None
    for n, ts, r in current:
        if n not in gone:  # a superseded record is not the baseline
            if prev_ts and ts < prev_ts and "corrects" not in r:
                problems.append(f"line {n}: ts goes back in time without a `corrects` field")
            prev_ts = max(prev_ts, ts) if prev_ts else ts
        if r["kind"] == "unit":
            units.setdefault(r.get("unit"), []).append((n, r))

    for unit, recs in units.items():
        first_n, first = recs[0]
        where = f"{unit} (line {first_n})"
        for key in ("wp", "unit", "actor"):
            if not first.get(key):
                problems.append(f"{where}: `{key}` is missing")
        if first.get("state") not in ("queued", "in flight"):
            problems.append(
                f"{where}: first record is `{first.get('state')}`; a unit is planned before it lands"
            )
        if first.get("est_pts") not in SCALE:
            problems.append(
                f"{where}: `est_pts` {first.get('est_pts')!r} is not on the scale 1, 2, 3, 5, 8"
            )
        for n, r in recs:
            if r.get("est_pts") != first.get("est_pts"):
                problems.append(f"{unit} (line {n}): `est_pts` changed; use `replanned_est_pts`")
            if r.get("state") not in STATES:
                problems.append(f"{unit} (line {n}): state {r.get('state')!r}")
            if r.get("model") not in MODELS:
                problems.append(f"{unit} (line {n}): model {r.get('model')!r}")
        n, last = recs[-1]
        if last.get("state") == "done":
            if not isinstance(last.get("realized_pts"), int) or last["realized_pts"] < 1:
                problems.append(f"{unit} (line {n}): done without integer `realized_pts`")
            if not (last.get("basis") or "").strip():
                problems.append(f"{unit} (line {n}): done without a `basis` line")
            if not isinstance(last.get("iteration"), int):
                problems.append(f"{unit} (line {n}): done without the `iteration` it landed in")

    iterations = [(n, r) for n, ts, r in current if r["kind"] == "iteration" and n not in gone]
    in_iteration = {}
    for n, it in iterations:
        names = it.get("units") or []
        if not names:
            problems.append(f"iteration record line {n}: no `units`")
        est = real = 0
        for u in names:
            in_iteration.setdefault(u, []).append(n)
            last = units.get(u, [(None, {})])[-1][1]
            if last.get("state") != "done":
                problems.append(f"iteration record line {n}: {u} is not done")
            est += last.get("est_pts") or 0
            real += last.get("realized_pts") or 0
        if names and (it.get("est_pts") != est or it.get("realized_pts") != real):
            problems.append(
                f"iteration record line {n}: points {it.get('est_pts')}/{it.get('realized_pts')} "
                f"differ from its units' {est}/{real}"
            )
        h = it.get("elapsed_h")
        if not isinstance(h, (int, float)) or h <= 0:
            problems.append(f"iteration record line {n}: `elapsed_h` must be positive")
        elif abs((it.get("velocity") or 0) - real / h) > 0.01 * max(1, real / h):
            problems.append(
                f"iteration record line {n}: `velocity` is not realized_pts / elapsed_h"
            )
    for u, lines in in_iteration.items():
        if len(lines) > 1:
            problems.append(f"{u}: in more than one iteration record (lines {lines})")

    if accept:
        mine = {u: recs for u, recs in units.items() if recs[0][1].get("wp") == accept}
        if not mine:
            problems.append(f"--accept {accept}: no units planned for it")
        for u, recs in mine.items():
            if recs[-1][1].get("state") != "done":
                problems.append(f"--accept {accept}: {u} is `{recs[-1][1].get('state')}`, not done")
            elif u not in in_iteration:
                problems.append(f"--accept {accept}: {u} is in no iteration record")

    for p in problems:
        print(p)
    if problems:
        verdict = f"; {accept} is not ready for acceptance" if accept else ""
        print(
            f"{len(problems)} problems in {len(records)} records ({len(current)} under the practice){verdict}"
        )
    else:
        verdict = f"; {accept} is ready for acceptance" if accept else ""
        print(f"metrics ok: {len(records)} records ({len(current)} under the practice){verdict}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
