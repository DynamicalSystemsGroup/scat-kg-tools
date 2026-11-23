"""Stack C schema: one pydantic model per page type. This is the ONLY place the rules' shape lives
in stack C; r13/ holds it equal to placeholder-tbox.ttl by a test.

Per model: CLASS (TBox class local name), LINKS (link field -> TBox class its targets must be),
REQUIRED_LINKS (link fields that must be present and non-empty once status is `done`).
"""

import re
from typing import ClassVar, Literal

from pydantic import BaseModel, ConfigDict

WIKILINK = re.compile(r"\[\[([^\]|#]+)(?:[|#][^\]]*)?\]\]")
STATUSES = ("stub", "draft", "done")


class Page(BaseModel):
    """Always required, every status: type, status, title (README contract). `description` is
    required only at `done` (checked in checks.py, R-3)."""

    model_config = ConfigDict(extra="ignore", frozen=True)
    CLASS: ClassVar[str]
    LINKS: ClassVar[dict[str, str]] = {}
    REQUIRED_LINKS: ClassVar[tuple[str, ...]] = ()

    type: str
    status: Literal["stub", "draft", "done"]
    title: str
    description: str | None = None


class _Linked(Page):
    """Link fields are lists of quoted wikilinks; a bare string is rejected by pydantic."""

    heldby: list[str] | None = None
    addresses: list[str] | None = None
    attributes: list[str] | None = None
    groups: list[str] | None = None
    concerns: list[str] | None = None
    affordances: list[str] | None = None
    technologies: list[str] | None = None
    raw: list[str] | None = None
    coded: list[str] | None = None


class StakeholderGroup(_Linked):
    type: Literal["stakeholder-group"]
    CLASS: ClassVar[str] = "StakeholderGroup"
    LINKS: ClassVar[dict[str, str]] = {"heldby": "Concern"}


class Concern(_Linked):
    type: Literal["concern"]
    CLASS: ClassVar[str] = "Concern"
    LINKS: ClassVar[dict[str, str]] = {"addresses": "Affordance"}


class Affordance(_Linked):
    type: Literal["affordance"]
    CLASS: ClassVar[str] = "Affordance"
    LINKS: ClassVar[dict[str, str]] = {"attributes": "Technology"}


class Technology(_Linked):
    type: Literal["technology"]
    CLASS: ClassVar[str] = "Technology"


class RawScenario(_Linked):
    type: Literal["scenario-raw"]
    CLASS: ClassVar[str] = "RawScenario"
    LINKS: ClassVar[dict[str, str]] = {"coded": "CodedScenario"}


class CodedScenario(_Linked):
    type: Literal["scenario-coded"]
    CLASS: ClassVar[str] = "CodedScenario"
    LINKS: ClassVar[dict[str, str]] = {
        "groups": "StakeholderGroup",
        "concerns": "Concern",
        "affordances": "Affordance",
        "raw": "RawScenario",
    }
    REQUIRED_LINKS: ClassVar[tuple[str, ...]] = ("groups", "concerns", "affordances")


class RawArchitecture(_Linked):
    type: Literal["architecture-raw"]
    CLASS: ClassVar[str] = "RawArchitecture"
    LINKS: ClassVar[dict[str, str]] = {"coded": "CodedArchitecture"}


class CodedArchitecture(_Linked):
    type: Literal["architecture-coded"]
    CLASS: ClassVar[str] = "CodedArchitecture"
    LINKS: ClassVar[dict[str, str]] = {
        "concerns": "Concern",
        "affordances": "Affordance",
        "technologies": "Technology",
        "raw": "RawArchitecture",
    }
    REQUIRED_LINKS: ClassVar[tuple[str, ...]] = ("concerns", "affordances", "technologies")


MODELS: dict[str, type[Page]] = {
    m.model_fields["type"].annotation.__args__[0]: m
    for m in (
        StakeholderGroup,
        Concern,
        Affordance,
        Technology,
        RawScenario,
        CodedScenario,
        RawArchitecture,
        CodedArchitecture,
    )
}
