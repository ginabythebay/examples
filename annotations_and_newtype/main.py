"""Demonstrates a way to use NewType and Annotations to mark fields in a class.

In this example we have RoleId and ChannelId which are ints underneath, but we want to display them differently and
declare them using NewType.  We also want to add labels to the fields that we can show to a user, and we leverage
Annotated for that.
"""

import annotationlib
from dataclasses import dataclass
from typing import Annotated, Callable, NewType, get_args

# pretty much just ints, but we can introspect and format them differently at run time.
ChannelId = NewType("ChannelId", int)
RoleId = NewType("RoleId", int)

#
# We output something different depending on the kind of int a field is
#

type Formatter = Callable[[object], str]


def format_channel(channel_id: object) -> str:
    return f"<#{channel_id}>"


def format_role(role_id: object) -> str:
    return f"<@&{role_id}>"


def formatter_for(field_type: object) -> Formatter:
    if field_type is ChannelId:
        return format_channel
    if field_type is RoleId:
        return format_role
    return str


def render_field(cfg: object, field_name: str, field_info: object) -> str:
    args: tuple[object, ...] = get_args(field_info)
    base_type: object = args[0]
    formatter = formatter_for(base_type)
    field_text = formatter(getattr(cfg, field_name))  # pyright: ignore[reportAny]
    return f"{args[1]}: {field_text}"


def to_text(cfg: object) -> str:
    field_descriptors: dict[str, object] = annotationlib.get_annotations(type(cfg))
    lines = (
        render_field(cfg, field_name, field_type)
        for field_name, field_type in field_descriptors.items()
    )
    return "\n".join(lines)


#
# Demonstrate the annotations and formatting
#


@dataclass(frozen=True)
class ExampleConfig:
    """Demonstrates the use of ChannelId, RoleId, and Annotated."""

    channel: Annotated[ChannelId, "channel"]
    allowed_role: Annotated[RoleId, "allowed role"]
    max_count: Annotated[int, "maximum count"]


def main():
    cfg = ExampleConfig(
        channel=ChannelId(123),
        allowed_role=RoleId(456),
        max_count=10,
    )

    print(to_text(cfg))


if __name__ == "__main__":
    main()
