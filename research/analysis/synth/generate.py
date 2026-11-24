"""Deterministic generator of a synthetic SCAT vault (fictional water cooperative).

Run from research/analysis:  uv run python synth/generate.py
Writes synth/vault/ afresh. Uses only the public scat_kg API (stub, stub_pair, index,
set_status, check) plus plain file writes for page content. All content is invented.
"""

import random
import shutil
import sys
from pathlib import Path

import scat_kg

HERE = Path(__file__).resolve().parent
ROOT = HERE / "vault"
SEED = 20260

# --- content -----------------------------------------------------------------------------
# (name, title, description)
GROUPS = [
    ("household-members", "Household members", "Residents who receive water at home and pay the monthly bill."),
    ("farm-irrigators", "Farm irrigators", "Growers who draw large seasonal volumes for crops and orchards."),
    ("treatment-operators", "Treatment operators", "Staff who run the treatment works and sample the water."),
    ("board-volunteers", "Board volunteers", "Elected volunteers who set tariffs, budgets and policy."),
    ("watershed-stewards", "Watershed stewards", "A local group that speaks for the river and its wildlife."),
    ("maintenance-crew", "Maintenance crew", "The team that repairs mains, valves and pumps."),
    ("school-liaisons", "School liaisons", "Teachers and youth leaders who bring pupils to learn about water."),
]

CONCERNS = [
    ("affordable-bills", "Affordable bills", "Households want a bill they can plan around."),
    ("guaranteed-irrigation-allocation", "Guaranteed irrigation allocation", "Growers want a fixed volume each season."),
    ("drought-supply-security", "Drought supply security", "Everyone wants water to keep flowing in a dry summer."),
    ("fair-usage-limits", "Fair usage limits", "Use should be capped in a way people see as even-handed."),
    ("water-quality-transparency", "Water quality transparency", "People want to see test results, not be told they are fine."),
    ("low-operating-cost", "Low operating cost", "Running costs should stay as small as they can."),
    ("safe-treatment-margins", "Safe treatment margins", "Treatment should keep a wide margin below every safety limit."),
    ("quick-leak-response", "Quick leak response", "A leak should be found and fixed within hours."),
    ("privacy-of-usage-data", "Privacy of usage data", "What a household uses is nobody else's business."),
    ("detailed-usage-visibility", "Detailed usage visibility", "Managers want to see use at fine detail to plan and spot waste."),
    ("predictable-maintenance-schedule", "Predictable maintenance schedule", "Work should be planned and announced well ahead."),
    ("minimal-service-interruptions", "Minimal service interruptions", "Taps should rarely run dry, planned work included."),
    ("environmental-flow-protection", "Environmental flow protection", "The river must keep enough flow for its wildlife."),
    ("regulatory-reporting-ease", "Regulatory reporting ease", "Annual reports to the inspectorate should not take weeks."),
    ("community-voice-in-decisions", "Community voice in decisions", "Members want a real say in rates and projects."),
    ("long-term-asset-renewal", "Long-term asset renewal", "Pipes and pumps should be replaced before they fail."),
    ("pupil-learning-access", "Pupil learning access", "Pupils should learn how water reaches the tap."),
    ("hands-on-site-visits", "Hands-on site visits", "Visits to the works should let pupils touch and try."),
]

AFFORDANCES = [
    ("tiered-tariff-schedule", "Tiered tariff schedule", "Price per unit rises in steps with use."),
    ("seasonal-allocation-calendar", "Seasonal allocation calendar", "A published calendar of volumes per user class and season."),
    ("usage-dashboard", "Usage dashboard", "Charts of consumption by area, user class and hour."),
    ("leak-alert-notifications", "Leak alert notifications", "An alert when flow looks like a leak."),
    ("public-quality-reports", "Public quality reports", "Monthly published water test results."),
    ("reserve-storage-policy", "Reserve storage policy", "A rule for how much water stays in the reservoir."),
    ("anonymised-usage-sharing", "Anonymised usage sharing", "Usage data shared with identities removed."),
    ("emergency-repair-roster", "Emergency repair roster", "An on-call rota for urgent repairs."),
    ("town-meeting-voting", "Town meeting voting", "Members vote on rates and projects."),
    ("regulator-report-export", "Regulator report export", "A ready-made annual report for the inspectorate."),
    ("river-flow-display", "River flow display", "A public display of current river flow."),
    ("community-asset-fund", "Community asset fund", "A ring-fenced fund for renewing pipes and pumps."),
    ("operator-training-course", "Operator training course", "A course that certifies new treatment operators."),
]

TECHNOLOGIES = [
    ("smart-meter-network", "Smart meter network", "Meters at each connection that report use by the hour."),
    ("member-portal", "Member portal", "A website where members see accounts and notices."),
    ("sensor-telemetry-platform", "Sensor telemetry platform", "Collects readings from pumps, mains and gauges."),
    ("billing-system", "Billing system", "Produces and records member bills."),
    ("sms-gateway", "SMS gateway", "Sends text messages to members and crews."),
    ("water-quality-lab-kit", "Water quality lab kit", "Field kit for sampling and testing water."),
    ("reservoir-level-gauges", "Reservoir level gauges", "Gauges that report reservoir and river levels."),
    ("voting-platform", "Voting platform", "Runs secure member ballots."),
    ("usage-data-warehouse", "Usage data warehouse", "Stores history of readings for analysis."),
    ("report-generator", "Report generator", "Builds formatted reports from stored data."),
]

# group -> concerns held
HELDBY = {
    "household-members": ["affordable-bills", "drought-supply-security", "fair-usage-limits",
                          "water-quality-transparency", "privacy-of-usage-data",
                          "minimal-service-interruptions", "quick-leak-response",
                          "community-voice-in-decisions"],
    "farm-irrigators": ["guaranteed-irrigation-allocation", "drought-supply-security",
                        "detailed-usage-visibility", "minimal-service-interruptions",
                        "community-voice-in-decisions"],
    "treatment-operators": ["safe-treatment-margins", "low-operating-cost",
                            "water-quality-transparency", "predictable-maintenance-schedule",
                            "regulatory-reporting-ease", "quick-leak-response"],
    "board-volunteers": ["affordable-bills", "low-operating-cost", "long-term-asset-renewal",
                         "fair-usage-limits", "community-voice-in-decisions",
                         "regulatory-reporting-ease", "safe-treatment-margins",
                         "privacy-of-usage-data", "detailed-usage-visibility"],
    "watershed-stewards": ["environmental-flow-protection", "water-quality-transparency",
                           "drought-supply-security", "fair-usage-limits",
                           "community-voice-in-decisions"],
    "maintenance-crew": ["quick-leak-response", "predictable-maintenance-schedule",
                         "minimal-service-interruptions", "long-term-asset-renewal",
                         "low-operating-cost"],
    "school-liaisons": ["pupil-learning-access", "hands-on-site-visits"],
}

# concern -> affordances addressing it (gaps: predictable-maintenance-schedule,
# pupil-learning-access, hands-on-site-visits have none)
ADDRESSES = {
    "affordable-bills": ["tiered-tariff-schedule", "usage-dashboard"],
    "guaranteed-irrigation-allocation": ["seasonal-allocation-calendar", "reserve-storage-policy"],
    "drought-supply-security": ["reserve-storage-policy", "seasonal-allocation-calendar", "usage-dashboard"],
    "fair-usage-limits": ["tiered-tariff-schedule", "seasonal-allocation-calendar", "usage-dashboard"],
    "water-quality-transparency": ["public-quality-reports", "usage-dashboard"],
    "low-operating-cost": ["leak-alert-notifications", "usage-dashboard"],
    "safe-treatment-margins": ["public-quality-reports", "operator-training-course"],
    "quick-leak-response": ["leak-alert-notifications", "emergency-repair-roster", "usage-dashboard"],
    "privacy-of-usage-data": ["anonymised-usage-sharing"],
    "detailed-usage-visibility": ["usage-dashboard"],
    "minimal-service-interruptions": ["emergency-repair-roster", "leak-alert-notifications", "usage-dashboard"],
    "environmental-flow-protection": ["river-flow-display", "reserve-storage-policy"],
    "regulatory-reporting-ease": ["regulator-report-export", "public-quality-reports"],
    "community-voice-in-decisions": ["town-meeting-voting"],
    "long-term-asset-renewal": ["community-asset-fund", "tiered-tariff-schedule"],
}

# affordance -> technologies (gaps: reserve-storage-policy, community-asset-fund,
# operator-training-course have none)
ATTRIBUTES = {
    "tiered-tariff-schedule": ["billing-system", "smart-meter-network"],
    "seasonal-allocation-calendar": ["member-portal"],
    "usage-dashboard": ["smart-meter-network", "member-portal", "sensor-telemetry-platform",
                        "usage-data-warehouse"],
    "leak-alert-notifications": ["smart-meter-network", "sensor-telemetry-platform", "sms-gateway"],
    "public-quality-reports": ["water-quality-lab-kit", "member-portal", "report-generator"],
    "anonymised-usage-sharing": ["usage-data-warehouse", "member-portal"],
    "emergency-repair-roster": ["sms-gateway", "sensor-telemetry-platform"],
    "town-meeting-voting": ["voting-platform", "member-portal"],
    "regulator-report-export": ["report-generator", "usage-data-warehouse"],
    "river-flow-display": ["reservoir-level-gauges", "sensor-telemetry-platform"],
}

# Conflicts: declared once, on the first concern (the relation is symmetric)
CONFLICTS = {
    "affordable-bills": ["long-term-asset-renewal"],
    "guaranteed-irrigation-allocation": ["environmental-flow-protection", "fair-usage-limits"],
    "privacy-of-usage-data": ["detailed-usage-visibility"],
    "low-operating-cost": ["safe-treatment-margins"],
}

# (raw name, raw title, raw description, raw body, coded name, groups, concerns, affordances)
SCENARIOS = [
    ("dry-july-allocation-talk", "Dry July allocation talk",
     "Notes from a meeting held during a dry July.",
     "A grower, a resident and a river steward sat down in the dry month. The grower asked how the "
     "season's volumes would be shared. The resident worried about low pressure in the evening. The "
     "steward asked that the river keep a visible flow.",
     "dry-july-allocation-talk-coded",
     ["household-members", "farm-irrigators", "watershed-stewards"],
     ["drought-supply-security", "fair-usage-limits", "environmental-flow-protection",
      "minimal-service-interruptions"],
     ["seasonal-allocation-calendar", "reserve-storage-policy", "river-flow-display"]),
    ("night-main-break", "Night main break",
     "An account of a burst main at two in the morning.",
     "A pipe burst in the night. A resident phoned it in, and the on-call repairer was woken. The "
     "operator saw pressure drop on the screens and agreed to isolate the section.",
     "night-main-break-coded",
     ["household-members", "maintenance-crew", "treatment-operators"],
     ["quick-leak-response", "minimal-service-interruptions", "low-operating-cost"],
     ["leak-alert-notifications", "emergency-repair-roster"]),
    ("budget-evening", "Budget evening",
     "Minutes of the yearly budget meeting.",
     "Volunteers presented next year's budget. A resident asked why the bill would rise. A grower "
     "asked whether the volume tiers would change. A crew member asked about pipe replacement.",
     "budget-evening-coded",
     ["board-volunteers", "household-members", "farm-irrigators", "maintenance-crew"],
     ["affordable-bills", "community-voice-in-decisions", "fair-usage-limits"],
     ["tiered-tariff-schedule", "town-meeting-voting"]),
    ("school-visit-day", "School visit day",
     "Notes from a class visit to the treatment works.",
     "A class of pupils toured the works. The teacher asked whether pupils could handle sample "
     "bottles. The operator showed the posted test results and answered questions.",
     "school-visit-day-coded",
     ["school-liaisons", "treatment-operators"],
     ["pupil-learning-access", "hands-on-site-visits", "water-quality-transparency"],
     ["public-quality-reports"]),
]

# (raw name, raw title, raw description, raw body, coded name, concerns, affordances, technologies)
ARCHITECTURES = [
    ("portal-first-pitch", "Portal first pitch",
     "A pitch to put members at the centre through a web portal.",
     "Every member gets an account in a portal with bills, tiers and a usage view. Reports to the "
     "inspectorate come from the same stored data.",
     "portal-first-pitch-coded",
     ["affordable-bills", "fair-usage-limits", "detailed-usage-visibility",
      "regulatory-reporting-ease"],
     ["tiered-tariff-schedule", "usage-dashboard", "regulator-report-export"],
     ["member-portal", "billing-system", "usage-data-warehouse", "report-generator"]),
    ("sensor-first-pitch", "Sensor first pitch",
     "A pitch to instrument the network and react fast.",
     "Sensors on the mains and at the river feed one platform. Alerts go out by text. Crews work "
     "from an on-call list.",
     "sensor-first-pitch-coded",
     ["quick-leak-response", "minimal-service-interruptions", "drought-supply-security",
      "environmental-flow-protection"],
     ["leak-alert-notifications", "emergency-repair-roster", "river-flow-display"],
     ["smart-meter-network", "sensor-telemetry-platform", "sms-gateway", "reservoir-level-gauges"]),
    ("lean-volunteer-pitch", "Lean volunteer pitch",
     "A pitch to run on volunteers and a small fund.",
     "Decisions go to a member vote. A small fund pays for renewals. Billing stays simple and "
     "cheap to run.",
     "lean-volunteer-pitch-coded",
     ["low-operating-cost", "community-voice-in-decisions", "long-term-asset-renewal"],
     ["town-meeting-voting", "community-asset-fund", "tiered-tariff-schedule"],
     ["voting-platform", "billing-system", "member-portal"]),
]

# --- writing -----------------------------------------------------------------------------


def q(text: str) -> str:
    return '"' + text.replace("\\", "\\\\").replace('"', '\\"') + '"'


def link(name: str) -> str:
    return f'"[[{name}]]"'


def write_page(path: Path, fm: list[tuple[str, object]], body: str = "") -> None:
    """Write frontmatter in the contract's field order. A list value is a YAML list of links;
    a `("key", ("link", name))` value is a single link; strings are quoted when text."""
    lines = ["---"]
    for key, val in fm:
        if key in ("type", "status"):
            lines.append(f"{key}: {val}")
        elif isinstance(val, list):
            lines.append(f"{key}:")
            lines.extend(f"  - {link(v)}" for v in val)
        elif isinstance(val, tuple):
            lines.append(f"{key}: {link(val[1])}")
        else:
            lines.append(f"{key}: {q(val)}")
    lines.append("---")
    text = "\n".join(lines) + "\n"
    if body:
        text += "\n" + body.strip() + "\n"
    path.write_text(text, encoding="utf-8")


def must(result):
    if not result.ok:
        sys.exit(f"generator failed:\n{result}")
    return result


def make(name: str, type_: str, title: str, description: str, extra=(), body=""):
    """Create a stub with the tools, then fill it in (status done)."""
    res = must(scat_kg.stub(name, type=type_, root=ROOT))
    assert res.created and res.created[0].endswith(f"{type_}/{name}.md"), res
    fm = [("type", type_), ("status", "done"), ("title", title), ("description", description)]
    write_page(ROOT / type_ / f"{name}.md", fm + list(extra), body)


def main() -> None:
    rng = random.Random(SEED)
    if ROOT.exists():
        shutil.rmtree(ROOT)
    ROOT.mkdir(parents=True)
    (ROOT / "scat.toml").write_text("stakeholder_group_cap = 8\n", encoding="utf-8")

    title = {}
    for name, t, d in GROUPS:
        title[name] = t
        make(name, "stakeholder-group", t, d)
    for name, t, d in CONCERNS:
        title[name] = t
        make(name, "concern", t, d, [("conflicts", CONFLICTS[name])] if name in CONFLICTS else [])
    for name, t, d in AFFORDANCES:
        title[name] = t
        make(name, "affordance", t, d)
    for name, t, d in TECHNOLOGIES:
        title[name] = t
        make(name, "technology", t, d)

    # Relation pages: the tools create and name them from the endpoint titles; we add the prose.
    held_notes = ["Raised often at their meetings.", "A steady worry through the year.",
                  "Comes up whenever the topic does.", "Felt most in the busy season."]
    addr_notes = ["Helps in most cases.", "Covers part of the concern.", "Works when used as intended.",
                  "A partial answer so far."]
    attr_notes = ["Provided by this part today.", "Relies on it for the core function.",
                  "One of the parts that deliver it."]

    def relation(kind, a, b, desc, notes, extra_keys):
        res = must(scat_kg.stub_pair(kind, a, b, root=ROOT))
        path = ROOT / res.created[0]
        write_page(path, [("type", kind), ("status", "done"), ("title", f"{title[a]} {desc} {title[b]}"),
                          ("description", f"{title[a]} {desc} {title[b]}."),
                          (extra_keys[0], ("link", a)), (extra_keys[1], ("link", b)),
                          ("notes", rng.choice(notes))])

    for g, cs in HELDBY.items():
        for c in cs:
            relation("heldby", g, c, "holds", held_notes, ("group", "concern"))
    for c, afs in ADDRESSES.items():
        for a in afs:
            relation("addresses", c, a, "is addressed by", addr_notes, ("concern", "affordance"))
    for a, ts in ATTRIBUTES.items():
        for t in ts:
            relation("attributes", a, t, "is attributed to", attr_notes, ("affordance", "technology"))

    for rname, rt, rd, body, cname, gs, cs, afs in SCENARIOS:
        make(rname, "scenario-raw", rt, rd, [("coded", [cname])], body)
        make(cname, "scenario-coded", rt + ", coded", f"A reading of the {rt.lower()} account.",
             [("raw", [rname]), ("groups", gs), ("concerns", cs), ("affordances", afs)])
    for rname, rt, rd, body, cname, cs, afs, ts in ARCHITECTURES:
        make(rname, "architecture-raw", rt, rd, [("coded", [cname])], body)
        make(cname, "architecture-coded", rt + ", coded", f"A reading of the {rt.lower()}.",
             [("raw", [rname]), ("concerns", cs), ("affordances", afs), ("technologies", ts)])

    must(scat_kg.index(root=ROOT))
    res = scat_kg.check(root=ROOT)
    print(res)
    if not res.ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
