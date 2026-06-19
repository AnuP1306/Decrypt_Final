import json
import os
from datetime import datetime


CACHE_FILE = os.path.join(
    os.path.dirname(__file__),
    "..",
    "cache",
    "live_opportunities_cache.json"
)


def load_live_opportunities():
    """
    Load cached live opportunities.
    """

    try:

        with open(
            CACHE_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)

            return data.get(
                "opportunities",
                []
            )

    except Exception as e:

        print(
            "Live opportunity cache error:",
            e
        )

        return []


def save_live_opportunities(opportunities):

    payload = {
        "last_updated":
            datetime.utcnow().isoformat(),

        "opportunities":
            opportunities
    }

    with open(
        CACHE_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            payload,
            f,
            indent=2,
            ensure_ascii=False
        )