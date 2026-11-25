"""WP17-U8: check_metrics refuses a ts ahead of the clock, unless a later record corrects it."""

import importlib.util
import json
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "work-packages" / "check_metrics.py"
_spec = importlib.util.spec_from_file_location("check_metrics", SCRIPT)
script = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(script)

NOW = datetime.now().astimezone()


def at(minutes):
    return (NOW + timedelta(minutes=minutes)).isoformat(timespec="seconds")


def unit(ts, state="queued", unit_name="WP99-U1", **extra):
    done = state == "done"
    rec = {
        "ts": ts,
        "kind": "unit",
        "wp": "WP99",
        "unit": unit_name,
        "actor": "Python developer",
        "model": "sonnet",
        "state": state,
        "est_pts": 2,
        "realized_pts": 2 if done else None,
        "basis": "on estimate" if done else None,
        "waiting_on": None,
        "iteration": 1 if done else None,
    }
    rec.update(extra)
    return rec


def iteration(ts, **extra):
    rec = {
        "ts": ts,
        "kind": "iteration",
        "iteration": 1,
        "units": ["WP99-U1"],
        "est_pts": 2,
        "realized_pts": 2,
        "elapsed_h": 1.0,
        "velocity": 2.0,
    }
    rec.update(extra)
    return rec


def run(monkeypatch, tmp_path, capsys, records):
    log = tmp_path / "metrics.jsonl"
    log.write_text("".join(json.dumps(r) + "\n" for r in records))
    monkeypatch.setattr(script, "LOG", log)
    monkeypatch.setattr(script, "HISTORY_LINES", 0)
    code = script.main([])
    return code, capsys.readouterr().out


def test__u8__a_record_ten_minutes_ahead_with_no_correction_fails(monkeypatch, tmp_path, capsys):
    records = [unit(at(-180)), unit(at(10), "done"), iteration(at(10))]
    code, out = run(monkeypatch, tmp_path, capsys, records)
    assert code == 1
    assert "line 2: ts is in the future" in out
    assert "line 3: ts is in the future" in out
    assert at(10) in out


def test__u8__a_record_four_minutes_ahead_passes_the_future_rule(monkeypatch, tmp_path, capsys):
    records = [unit(at(-180)), unit(at(4), "done"), iteration(at(4))]
    code, out = run(monkeypatch, tmp_path, capsys, records)
    assert "in the future" not in out
    assert code == 0, out


def test__u8__a_correction_supersedes_a_future_record_and_an_iteration_is_not_counted_twice(
    monkeypatch, tmp_path, capsys
):
    wrong = at(10)
    records = [
        unit(at(-180)),
        unit(wrong, "done"),
        iteration(wrong),
        unit(at(-60), "done", corrects=wrong),
        iteration(at(-60), corrects=wrong),
    ]
    code, out = run(monkeypatch, tmp_path, capsys, records)
    assert code == 0, out
    assert "more than one iteration record" not in out


def test__u8__a_corrects_that_matches_nothing_does_not_exempt_a_future_record(
    monkeypatch, tmp_path, capsys
):
    records = [
        unit(at(-180)),
        unit(at(10), "done"),
        unit(at(-60), "done", corrects=at(30)),  # wrong ts: matches no earlier record
        iteration(at(-60)),
    ]
    code, out = run(monkeypatch, tmp_path, capsys, records)
    assert code == 1
    assert "line 2: ts is in the future" in out


def test__u8__a_correction_of_another_unit_does_not_exempt_a_future_record(
    monkeypatch, tmp_path, capsys
):
    wrong = at(10)
    records = [
        unit(at(-180)),
        unit(wrong, "done"),
        unit(at(-60), "done", unit_name="WP99-U2", corrects=wrong),
    ]
    code, out = run(monkeypatch, tmp_path, capsys, records)
    assert code == 1
    assert "line 2: ts is in the future" in out


def test__u8__two_records_of_one_unit_with_one_wrong_ts_need_two_corrections(
    monkeypatch, tmp_path, capsys
):
    wrong = at(10)
    planned = [unit(wrong), unit(wrong, "done"), iteration(at(-60))]
    both = [
        *planned,
        unit(at(-120), corrects=wrong),
        unit(at(-90), "done", corrects=wrong),
    ]
    code, out = run(monkeypatch, tmp_path, capsys, both)
    assert code == 0, out

    one = both[:-1]  # only one correction: the later of the two wrong records stays wrong
    code, out = run(monkeypatch, tmp_path, capsys, one)
    assert code == 1
    assert "line 2: ts is in the future" in out
    assert "line 1: ts is in the future" not in out


def test__u8__the_real_log_passes_the_check():
    done = subprocess.run(
        [sys.executable, str(SCRIPT)], check=False, capture_output=True, text=True, cwd=ROOT
    )
    assert (done.returncode, done.stderr) == (0, ""), done.stdout
    assert done.stdout.startswith("metrics ok")
