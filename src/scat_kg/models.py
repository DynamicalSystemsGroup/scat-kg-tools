"""One pydantic model per page type, built from the TBox when this module loads (R-13).

No field list is written here: a model's fields are the TBox's fields for that page type, required
and optional alike. Each model checks the *shape* of what is written and nothing else:
every field is optional (whether a field is required depends on the page's status, which is a rule's
business, not the model's), a field with a value set (`status`, `timeframe`, `kind`) takes only its
values, any other field is text, and `type` takes only the page type's slug. Keys the TBox does not list
for the type are ignored, as the contract says.
"""

from typing import Literal

from pydantic import BaseModel, ConfigDict, create_model

from scat_kg.tbox import TBOX, Field, PageType, TBox


def _annotation(field: Field):
    if field.value_set is not None:
        return Literal[field.value_set]
    return str


def build_model(page_type: PageType) -> type[BaseModel]:
    fields = {f.key: (_annotation(f) | None, None) for f in page_type.fields if f.key != "type"}
    fields["type"] = (Literal[page_type.slug], ...)  # the one thing a model insists on
    return create_model(
        f"Page_{page_type.slug.replace('-', '_')}",
        __config__=ConfigDict(extra="ignore", strict=True),
        **fields,
    )


def build_models(tbox: TBox) -> dict[str, type[BaseModel]]:
    return {slug: build_model(t) for slug, t in tbox.page_types.items()}


MODELS = build_models(TBOX)
