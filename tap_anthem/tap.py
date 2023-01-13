"""anthem tap class."""

from typing import List

from singer_sdk import Tap, Stream
from singer_sdk import typing as th  # JSON schema typing helpers
from tap_anthem.streams import (
    NhPlansStream,
    NhProvidersStream,
    NhDrugsStream
)

STREAM_TYPES = [
    NhPlansStream,
    NhProvidersStream,
    NhDrugsStream
]


class Tapanthem(Tap):
    """anthem tap class."""
    name = "tap-anthem"

    config_jsonschema = th.PropertiesList().to_dict()

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        return [stream_class(tap=self) for stream_class in STREAM_TYPES]


if __name__ == "__main__":
    Tapanthem.cli()
