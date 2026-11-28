"""Build the three copies of the WP24 test vault from one source of truth.

The range vault (research/range/koi/vault) plus synthetic narratives about the same fictional lab case, written to
research/node-pages/vault/{disallowed,optional,required}. The copies differ only as the attribution mode requires:
the scat.toml, the contributor pages and the narratives' `attributed_to`. Run: uv run python research/node-pages/build_vault.py
"""

from __future__ import annotations

import shutil
from pathlib import Path

import scat_tools

HERE = Path(__file__).resolve().parent
RANGE = HERE.parent / "range" / "koi" / "vault"
OUT = HERE / "vault"
MODES = ("disallowed", "optional", "required")
CONTRIBUTORS = {
    "lab-member-a": "Lab member A",
    "lab-member-b": "Lab member B",
    "lab-member-c": "Lab member C",
}

# ---- node pages: (type, name, status, title, description, body) ------------------------------------------------

NODES = [
    # concerns
    (
        "concern",
        "members-not-replying",
        "draft",
        "Members not replying",
        "Many members do not reply to the direct message that starts a feedback round, so the round stalls.",
        "Many [[members-not-replying|members were not replying]] to the direct message that starts a feedback round, "
        "so the round stalled. The ethnographers added a reminder message sent by the [[forum-bot|forum bot]] three days after the first one.",
    ),
    (
        "concern",
        "unanswered-direct-messages",
        "draft",
        "Unanswered direct messages",
        "Messages sent to members at the start of a round go without an answer, and nothing moves until someone replies.",
        "",
    ),
    (
        "concern",
        "members-lose-the-thread",
        "draft",
        "Members lose the thread",
        "Members drop out of a long-running thread because nothing brings them back to where it stands.",
        "Across the trial narratives this is told two ways. In the ethnographers' telling the thread is the study, and "
        "members fall away from it between feedback rounds. In the moderators' telling the thread is the forum's own "
        "discussion, and the loss is felt as repeated questions. Both agree a short periodic summary helps; they differ "
        "on whether it should come as a post or in the inbox. Thin: no member is recorded as saying what they wanted.",
    ),
    (
        "concern",
        "data-retention",
        "done",
        "Data retention",
        "How long consented data may be kept before the committee expects it to be reviewed.",
        "",
    ),
    (
        "concern",
        "data-retention-schedule",
        "done",
        "Data retention schedule",
        "The timetable on which the platform removes expired records.",
        "",
    ),
    (
        "concern",
        "interpretive-work-needs-time",
        "draft",
        "Interpretive work needs time",
        "Writing up what a round showed takes hours the ethnographers do not always have.",
        "",
    ),
    ("concern", "renewal-cost-visibility", "stub", "Renewal cost visibility", None, ""),
    # affordances
    (
        "affordance",
        "direct-message-reminder",
        "draft",
        "Direct message reminder",
        "A reminder sent three days after the first message to members who have not replied.",
        "The ethnographers added a [[direct-message-reminder|reminder message]] sent by the [[forum-bot|forum bot]] three "
        "days after the first one. Replies rose, though nobody counted how much.",
    ),
    (
        "affordance",
        "weekly-digest",
        "draft",
        "Weekly digest",
        "A summary of the week's activity posted to the forum on Sundays.",
        "",
    ),
    (
        "affordance",
        "digest-email",
        "draft",
        "Digest email",
        "A summary of the week's activity sent to members by email on Sundays.",
        "",
    ),
    (
        "affordance",
        "retention-review-calendar",
        "draft",
        "Retention review calendar",
        "A calendar of dates on which the committee reviews how long data is kept.",
        "",
    ),
    (
        "affordance",
        "auto-expiry-job",
        "draft",
        "Auto-expiry job",
        "A scheduled job that removes records once they pass their age limit.",
        "",
    ),
    ("affordance", "field-notes-template", "stub", "Field notes template", None, ""),
    (
        "affordance",
        "shared-cost-report",
        "draft",
        "Shared cost report",
        "A yearly report that shows each member organisation what its share of the platform costs.",
        "",
    ),
    # technologies
    (
        "technology",
        "forum-bot",
        "draft",
        "Forum bot",
        "A bot on the forum that sends messages and posts on a timetable.",
        "In the narratives the bot is the thing that does the sending: reminders in one, a posted digest in another. "
        "It is never described as deciding what to send; the ethnographers or moderators set the wording and the "
        "timing. Where accounts differ is upkeep: one narrative says it needed no attention, another says a moderator "
        "restarted it twice. What is thin is who owns it.",
    ),
    ("technology", "mail-relay", "stub", "Mail relay", None, ""),
    ("technology", "scheduler", "stub", "Scheduler", None, ""),
]

# ---- narratives ------------------------------------------------------------------------------------------------
# (name, title, kind, status, description, timeframe, account, rows); a row is (from, type, to, note)

H, A, P = "holds", "is addressed by", "is provided by"

NARRATIVES = [
    (
        "reminders-and-the-quiet-inbox",
        "Reminders and the quiet inbox",
        "scenario",
        "draft",
        "The second season began with a stalled feedback round and a reminder message to get it moving.",
        "past",
        """The [[ethnographers]] opened the second season with a long list of what had not worked in the first. The study had to be fed back, and the work of [[closing-the-loop|closing the loop]] had slipped for six weeks. Nothing was written up in March because nobody had the time to do the interpretive work, and that is what held the loop open.

The second trouble was the quiet inbox. Many [[members-not-replying|members were not replying]] to the direct message that starts a feedback round, so the round stalled. The ethnographers added a [[direct-message-reminder|reminder message]] sent by the [[forum-bot|forum bot]] three days after the first one. Replies rose, though nobody counted how much.

Notes from every round were kept in [[telescope|Telescope]], as [[durable-shared-records|lasting, shared records]].""",
        [
            ("ethnographers", H, "closing-the-loop", "Slipped for six weeks in March."),
            ("closing-the-loop", A, "durable-shared-records", "Notes from every round kept."),
            ("durable-shared-records", P, "telescope", ""),
            ("ethnographers", H, "members-not-replying", "The stalled round."),
            ("members-not-replying", A, "direct-message-reminder", "Replies rose, uncounted."),
            ("direct-message-reminder", P, "forum-bot", "Sent three days after the first message."),
        ],
    ),
    (
        "the-unanswered-messages-week",
        "The unanswered messages week",
        "scenario",
        "draft",
        "One week in which the opening messages of a round went unanswered and the reminder was tried for the first time.",
        "past",
        """In the week the round opened, the [[ethnographers]] counted the [[unanswered-direct-messages|messages that went unanswered]] and stopped counting at thirty. They had expected a few. Because the [[closing-the-loop|loop]] depends on members answering first, a silent inbox meant the whole round could not begin.

On the Thursday they switched on the [[direct-message-reminder|reminder]], which the [[forum-bot|forum bot]] sent to everyone who had not replied. By Sunday about half of the thirty had answered. The ethnographers read this as the reminder working, and wrote it into [[telescope|Telescope]] so that the next round would start from it.""",
        [
            (
                "ethnographers",
                H,
                "closing-the-loop",
                "The loop depends on members answering first.",
            ),
            ("closing-the-loop", A, "durable-shared-records", "Written up for the next round."),
            ("durable-shared-records", P, "telescope", ""),
            ("ethnographers", H, "unanswered-direct-messages", "Counted to thirty and stopped."),
            (
                "unanswered-direct-messages",
                A,
                "direct-message-reminder",
                "About half answered by Sunday.",
            ),
            ("direct-message-reminder", P, "forum-bot", ""),
        ],
    ),
    (
        "two-names-for-the-same-silence",
        "Two names for the same silence",
        "scenario",
        "done",
        "The ethnographers kept two phrases for one problem, members who do not answer, and the same reminder served both.",
        "past",
        """The [[ethnographers]] had two phrases in their notes for what looked like one problem. Some entries spoke of [[members-not-replying|members not replying]], and others of [[unanswered-direct-messages|unanswered direct messages]]. Reading the entries side by side, the working group found the same people, the same rounds and the same remedy under both phrases.

Both were met with the [[direct-message-reminder|reminder message]] that the [[forum-bot|forum bot]] sends. Both sit inside the larger worry of [[closing-the-loop|closing the loop]], which the [[telescope|Telescope]] notes tracked round by round.

The notes do not say whether the group meant to keep the two phrases apart. They record only that the same reminder was applied to both.""",
        [
            ("ethnographers", H, "members-not-replying", "One phrase in the notes."),
            (
                "ethnographers",
                H,
                "unanswered-direct-messages",
                "The other phrase, for the same rounds.",
            ),
            ("members-not-replying", A, "direct-message-reminder", "The same reminder."),
            ("unanswered-direct-messages", A, "direct-message-reminder", "The same reminder."),
            ("direct-message-reminder", P, "forum-bot", ""),
            ("ethnographers", H, "closing-the-loop", "The larger worry both sit inside."),
            ("closing-the-loop", A, "durable-shared-records", "Tracked round by round."),
            ("durable-shared-records", P, "telescope", ""),
        ],
    ),
    (
        "notes-that-survived-the-move",
        "Notes that survived the move",
        "architecture",
        "draft",
        "How the lab's notes moved between tools and what let them last.",
        "past",
        """When the lab changed its working space, the notes moved with it. The [[durable-shared-records|shared records]] were the one thing everyone insisted on, since [[closing-the-loop|closing the loop]] needs last season's notes in front of the people writing this season's analysis. They lived in [[telescope|Telescope]] and in [[obsidian|Obsidian]] side by side for a term, and neither lost an entry.

Telescope's participatory mode also carried over. The [[participatory-consent-feature|consent feature]] kept working, which mattered because [[legitimate-consent-at-forum-scale|consent at forum scale]] had to be shown again to the committee at the end of the term.""",
        [
            (
                "closing-the-loop",
                A,
                "durable-shared-records",
                "Last season's notes in front of this season's analysts.",
            ),
            ("durable-shared-records", P, "telescope", ""),
            ("durable-shared-records", P, "obsidian", "Side by side for a term."),
            (
                "legitimate-consent-at-forum-scale",
                A,
                "participatory-consent-feature",
                "Kept working through the move.",
            ),
            ("participatory-consent-feature", P, "telescope", ""),
        ],
    ),
    (
        "weekly-digest-trial",
        "The weekly digest trial",
        "scenario",
        "done",
        "Two ways of summarising the week were tried for members who lose the thread, one posted and one emailed.",
        "past",
        """The [[ethnographers]] noticed that [[members-lose-the-thread|members lost the thread]] between feedback rounds. For one term they tried two summaries. The [[weekly-digest|weekly digest]] was posted to the forum by the [[forum-bot|forum bot]] on Sundays. The [[digest-email|digest email]] went to members' inboxes through the [[mail-relay|mail relay]] at the same hour.

Both were meant to keep the study in view, part of [[closing-the-loop|closing the loop]]. The notes treat them as two forms of one remedy: either way, the same members were reached with the same summary.""",
        [
            ("ethnographers", H, "members-lose-the-thread", "Between feedback rounds."),
            ("members-lose-the-thread", A, "weekly-digest", "Posted to the forum."),
            ("members-lose-the-thread", A, "digest-email", "Sent to the inbox."),
            ("weekly-digest", P, "forum-bot", ""),
            ("digest-email", P, "mail-relay", ""),
            ("ethnographers", H, "closing-the-loop", "The summaries keep the study in view."),
        ],
    ),
    (
        "consent-emoji-at-the-spring-forum",
        "Consent emoji at the spring forum",
        "scenario",
        "draft",
        "At the spring forum members gave consent with emoji and the working group learned how far that carried.",
        "past",
        """At the spring forum the [[ethnographers]] asked members to give [[legitimate-consent-at-forum-scale|consent]] with an emoji on each post they were happy to have collected. The [[participatory-consent-feature|participatory consent feature]] in [[telescope|Telescope]] recorded the reactions, and several members, not only the ethnographers, could see and collect them.

That spread the work. It also eased the [[attention-limit-on-participation|attention limit]], since one person no longer had to watch every thread. The ethnographers still checked a sample by hand, and the sample was small.""",
        [
            ("ethnographers", H, "legitimate-consent-at-forum-scale", ""),
            (
                "legitimate-consent-at-forum-scale",
                A,
                "participatory-consent-feature",
                "Emoji on each post.",
            ),
            ("participatory-consent-feature", P, "telescope", ""),
            (
                "ethnographers",
                H,
                "attention-limit-on-participation",
                "One person could not watch every thread.",
            ),
            (
                "attention-limit-on-participation",
                A,
                "participatory-consent-feature",
                "Several people could collect.",
            ),
        ],
    ),
    (
        "the-committee-asks-again",
        "The committee asks again",
        "scenario",
        "draft",
        "At renewal the committee asked how long the lab kept consented data and how it would show consent was still good.",
        "past",
        """At renewal the [[ethics-committees|committee]] asked two things. The first was how long consented data would be kept: its worry was [[data-retention|data retention]], and it wanted dates. The lab answered with a [[retention-review-calendar|retention review calendar]] kept in [[obsidian|Obsidian]].

The second question was whether [[legitimate-consent-at-forum-scale|consent]] still held at the forum's present size. The lab pointed to the [[participatory-consent-feature|participatory consent feature]] in [[telescope|Telescope]]. The committee accepted both answers, with a note to look again next year.""",
        [
            ("ethics-committees", H, "data-retention", "It wanted dates."),
            ("data-retention", A, "retention-review-calendar", ""),
            ("retention-review-calendar", P, "obsidian", ""),
            ("ethics-committees", H, "legitimate-consent-at-forum-scale", ""),
            (
                "legitimate-consent-at-forum-scale",
                A,
                "participatory-consent-feature",
                "Pointed to at renewal.",
            ),
            ("participatory-consent-feature", P, "telescope", ""),
        ],
    ),
    (
        "expiry-job-design-notes",
        "Expiry job design notes",
        "architecture",
        "draft",
        "Notes on how the platform removes records that pass their age limit.",
        "future",
        """The [[technical-team|technical team]] needs a [[data-retention-schedule|schedule]] for removing records that pass their age limit. The plan is an [[auto-expiry-job|auto-expiry job]] that runs nightly and removes what is due. It would run on the [[scheduler|scheduler]], which the team already uses for backups.

Open question: whether the job keeps a log of what it removed. The team has not settled this.""",
        [
            ("technical-team", H, "data-retention-schedule", ""),
            ("data-retention-schedule", A, "auto-expiry-job", "Nightly run."),
            ("auto-expiry-job", P, "scheduler", "Already used for backups."),
        ],
    ),
    (
        "members-as-the-site-sees-them",
        "Members as the site sees them",
        "scenario",
        "draft",
        "At the field site the community members are the people who post, resist and reshape the thread.",
        "past",
        """At the field site, the [[community-members|community members]] are the people who post in the forum every day. They answer questions, argue with the moderators and decide, by their replies, whether a feedback round gets anywhere. When [[members-lose-the-thread|members lose the thread]] it is they who say so first, usually by asking the same question again.

They are also who the ethnographers' [[shared-data-set-integrity|shared data set]] is about, and whose use of it counts.""",
        [
            (
                "community-members",
                H,
                "members-lose-the-thread",
                "They say so first, by repeating a question.",
            ),
            (
                "community-members",
                H,
                "shared-data-set-integrity",
                "The data set is about them and used by them.",
            ),
        ],
    ),
    (
        "member-organisations-and-the-renewal",
        "Member organisations and the renewal",
        "scenario",
        "draft",
        "The community members who sign off the yearly renewal are staff of the member organisations, not the site's posters.",
        "past",
        """Each year the [[community-members|community members]] who matter for the renewal are the staff of the beneficiary organisations. They do not post at the site. They hold the budget, and they read the yearly report to decide whether the platform is worth its share.

Their worry is [[vendor-lock-in|vendor lock-in]]: they want a reason to stay that is not only that leaving is hard. The other is [[renewal-cost-visibility|seeing what their share pays for]], which the [[shared-cost-report|shared cost report]] is meant to answer, built on the [[scheduler|scheduler]] that runs it each January.""",
        [
            (
                "community-members",
                H,
                "vendor-lock-in",
                "A reason to stay that is not only that leaving is hard.",
            ),
            ("community-members", H, "renewal-cost-visibility", "What their share pays for."),
            ("renewal-cost-visibility", A, "shared-cost-report", ""),
            ("shared-cost-report", P, "scheduler", "Runs each January."),
        ],
    ),
    (
        "a-second-look-at-consent-wording",
        "A second look at the consent wording",
        "scenario",
        "done",
        "After the spring forum the working group rewrote the consent wording and the feature carried it.",
        "past",
        """After the spring forum the [[ethnographers]] rewrote the wording that asked for [[legitimate-consent-at-forum-scale|consent]]. The first wording had been read as a request to join a study; the second said plainly what would be collected. The [[participatory-consent-feature|participatory consent feature]] in [[telescope|Telescope]] carried the new wording without further change.

The group also found the [[attention-limit-on-participation|attention limit]] less pressing once several people were collecting.""",
        [
            ("ethnographers", H, "legitimate-consent-at-forum-scale", ""),
            (
                "legitimate-consent-at-forum-scale",
                A,
                "participatory-consent-feature",
                "Carried the new wording.",
            ),
            ("participatory-consent-feature", P, "telescope", ""),
            (
                "ethnographers",
                H,
                "attention-limit-on-participation",
                "Less pressing with several collectors.",
            ),
            ("attention-limit-on-participation", A, "participatory-consent-feature", ""),
        ],
    ),
    (
        "forum-moderators-and-digests",
        "Forum moderators and digests",
        "scenario",
        "draft",
        "The moderators liked the posted digest, because it cut down on repeated questions.",
        "past",
        """The moderators, who are [[community-members|community members]] at the site, spoke well of the [[weekly-digest|weekly digest]]. Posted by the [[forum-bot|forum bot]] each Sunday, it answered the questions they were tired of answering. It helped with [[members-lose-the-thread|members losing the thread]], they said, though they could not say whether it brought anyone back.""",
        [
            ("community-members", H, "members-lose-the-thread", "Felt as repeated questions."),
            ("members-lose-the-thread", A, "weekly-digest", ""),
            ("weekly-digest", P, "forum-bot", "Posted each Sunday."),
        ],
    ),
    (
        "what-the-sunday-email-did",
        "What the Sunday email did",
        "scenario",
        "draft",
        "The emailed digest reached members who never opened the forum, with mixed results.",
        "past",
        """The [[digest-email|digest email]] reached some members who never opened the forum. It went out through the [[mail-relay|mail relay]], and a few weeks in the relay marked a batch as junk. The working group did not find out until a member mentioned it. For [[members-lose-the-thread|members who lose the thread]], the email was the only summary they saw, since the posted weekly digest never reached their inbox.""",
        [
            ("members-lose-the-thread", A, "digest-email", "Only summary some members saw."),
            ("digest-email", P, "mail-relay", "A batch was marked as junk."),
        ],
    ),
    (
        "field-notes-template-pilot",
        "Field notes template pilot",
        "scenario",
        "draft",
        "A shared template for field notes was tried to save the ethnographers time when they write up a round.",
        "past",
        """Write-up took the time the [[ethnographers]] did not have. Their worry was that [[interpretive-work-needs-time|interpretive work needs time]], and a round that is not written up cannot be fed back. They piloted a [[field-notes-template|field notes template]] in [[obsidian|Obsidian]], with headings for what was said, what was seen and what to follow up. Only two ethnographers used it.""",
        [
            ("ethnographers", H, "interpretive-work-needs-time", ""),
            ("interpretive-work-needs-time", A, "field-notes-template", "Only two used it."),
            ("field-notes-template", P, "obsidian", ""),
        ],
    ),
    (
        "reminder-wording-workshop",
        "Reminder wording workshop",
        "scenario",
        "draft",
        "The working group spent an afternoon on the wording of the reminder for members who had not answered.",
        "past",
        """The [[ethnographers]] spent an afternoon on the wording of the [[direct-message-reminder|reminder]]. They had two names for the trouble it addressed, [[members-not-replying|members not replying]] and [[unanswered-direct-messages|unanswered direct messages]], and agreed the reminder should not scold either way. The [[forum-bot|forum bot]] would send whatever text they settled on.""",
        [
            ("ethnographers", H, "members-not-replying", ""),
            ("ethnographers", H, "unanswered-direct-messages", ""),
            ("members-not-replying", A, "direct-message-reminder", ""),
            ("unanswered-direct-messages", A, "direct-message-reminder", ""),
            ("direct-message-reminder", P, "forum-bot", "Sends whatever text they settle on."),
        ],
    ),
]

# narratives that name contributors: required names one for each; optional names a few
RANGE_NARRATIVES = sorted(p.stem for p in (RANGE / "narrative").glob("*.md"))
ALL_NARRATIVES = RANGE_NARRATIVES + [n[0] for n in NARRATIVES]
CYCLE = [["lab-member-a"], ["lab-member-b"], ["lab-member-c"], ["lab-member-a", "lab-member-b"]]
OPTIONAL_NAMED = {
    "consent-and-ethics-gate": ["lab-member-a"],
    "two-names-for-the-same-silence": ["lab-member-b", "lab-member-c"],
    "weekly-digest-trial": ["lab-member-a"],
    "members-as-the-site-sees-them": ["lab-member-c"],
}


def attributed(mode: str, name: str) -> list[str]:
    if mode == "required":
        return CYCLE[ALL_NARRATIVES.index(name) % len(CYCLE)]
    if mode == "optional":
        return OPTIONAL_NAMED.get(name, [])
    return []


def q(text: str) -> str:
    return '"' + text.replace("\\", "\\\\").replace('"', '\\"') + '"'


def node_text(type_, name, status, title, description, body) -> str:
    lines = ["---", f"type: {type_}", f"status: {status}", f"title: {q(title)}"]
    if description:
        lines.append(f"description: {q(description)}")
    lines.append("---")
    text = "\n".join(lines) + "\n"
    return text + (f"\n{body}\n" if body else "")


def narrative_text(n, names: list[str]) -> str:
    name, title, kind, status, description, timeframe, account, rows = n
    head = ["---", "type: narrative", f"kind: {kind}", f"status: {status}", f"title: {q(title)}"]
    head += [f"description: {q(description)}", f"timeframe: {timeframe}"]
    if names:
        head.append("attributed_to: [" + ", ".join(q(f"[[{c}]]") for c in names) + "]")
    head.append("---")
    table = ["## Edges told", "", "| from | type | to | note |", "|---|---|---|---|"]
    table += [f"| [[{a}]] | {t} | [[{b}]] | {note} |" for a, t, b, note in rows]
    return "\n".join(head) + "\n\n" + account.strip() + "\n\n" + "\n".join(table) + "\n"


def with_attribution(text: str, names: list[str]) -> str:
    """A range narrative's text with `attributed_to` added to its frontmatter."""
    if not names:
        return text
    line = "attributed_to: [" + ", ".join(q(f"[[{c}]]") for c in names) + "]\n"
    head, sep, rest = text[4:].partition("\n---\n")
    return "---\n" + head + "\n" + line + "---\n" + rest


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def build(mode: str) -> None:
    root = OUT / mode
    if root.exists():
        shutil.rmtree(root)
    for src in sorted(RANGE.rglob("*.md")):
        rel = src.relative_to(RANGE)
        text = src.read_text(encoding="utf-8")
        if rel.parts[0] == "narrative":
            text = with_attribution(text, attributed(mode, src.stem))
        write(root / rel, text)
    for node in NODES:
        write(root / node[0] / f"{node[1]}.md", node_text(*node))
    for n in NARRATIVES:
        write(root / "narrative" / f"{n[0]}.md", narrative_text(n, attributed(mode, n[0])))
    if mode != "disallowed":
        for name, title in CONTRIBUTORS.items():
            write(
                root / "contributor" / f"{name}.md",
                f"---\ntype: contributor\nstatus: done\ntitle: {q(title)}\n---\n",
            )
    write(root / "scat.toml", f'attribution = "{mode}"\nstakeholder_group_cap = 4\n')
    scat_tools.index(root=root)


def main() -> None:
    for mode in MODES:
        build(mode)


if __name__ == "__main__":
    main()
