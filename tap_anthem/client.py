"""REST client handling, including anthemStream base class."""

import requests
from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable

from memoization import cached

from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.streams import RESTStream

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class AnthemStream(RESTStream):
    """Anthem (Plans and Providers) stream class."""

    # From https://www22.anthem.com/cms-data-index.json/index.html
    url_base = "https://www22.anthem.com/CMS"


class FormularyNavigatorStream(RESTStream):
    """FormularyNavigator (drugs) stream class."""

    # From https://www22.anthem.com/cms-data-index.json/index.html
    url_base = "https://fm.formularynavigator.com/jsonFiles/publish/143"
