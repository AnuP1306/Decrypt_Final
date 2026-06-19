# import json
# import os
# import time

# Path to the verified opportunities JSON file
# DATA_PATH = os.path.join(
#     os.path.dirname(__file__), "..", "data", "verified_opportunities.json"
# )
# DATA_PATH = os.path.join(
#     os.path.dirname(__file__),
#     "..",
#     "static",
#     "data",
#     "verified_opportunities.json"
# )

# Simple in-memory cache (Phase 4 pattern, same as Daily Brief)
# OPPORTUNITY_CACHE = {
#     "data": None,
#     "timestamp": 0,
# }

# CACHE_TTL_SECONDS = 60 * 60  # 1 hour


# def _load_verified_opportunities():
#     """Load the static verified opportunities from JSON file."""
#     try:
#         with open(DATA_PATH, "r", encoding="utf-8") as f:
#             data = json.load(f)
#             return data.get("opportunities", [])
#     except Exception as e:
#         print("Error loading verified_opportunities.json:", e)
#         return []


# def get_opportunities(force_refresh: bool = False):
#     """
#     Returns the unified list of opportunities.

#     Phase 1/2: Returns static verified opportunities (Student Perks,
#     Courses, Workshops) from the JSON data source, with caching.

#     Phase 3+ (future): This is where live event feeds (Source 2) and
#     the Gemini AI Curator Layer (Source 3) will be merged in before
#     caching the combined result.
#     """
#     now = time.time()

#     if (
#         not force_refresh
#         and OPPORTUNITY_CACHE["data"] is not None
#         and (now - OPPORTUNITY_CACHE["timestamp"]) < CACHE_TTL_SECONDS
#     ):
#         return OPPORTUNITY_CACHE["data"]

#     # Source 1: static verified opportunities
#     opportunities = _load_verified_opportunities()

#     # TODO (Phase 3): fetch + merge live feeds here (Source 2)
#     # TODO (Phase 3): pass merged list through Gemini categorizer (Source 3)

#     OPPORTUNITY_CACHE["data"] = opportunities
#     OPPORTUNITY_CACHE["timestamp"] = now

#     return opportunities


# def get_opportunities_by_type(opp_type: str):
#     """Filter opportunities by type: 'Student Perks', 'Courses', 'Workshops'."""
#     all_opps = get_opportunities()
#     if opp_type == "All" or not opp_type:
#         return all_opps
#     return [o for o in all_opps if o.get("type") == opp_type]
import json
import os
import time

from dotenv import load_dotenv

from services.opportunity_scraper import (
    load_live_opportunities
)

from services.opportunity_fetcher import (
    fetch_live_opportunities
)

load_dotenv()

# Correct path
DATA_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "static",
    "data",
    "verified_opportunities.json"
)

# Cache
OPPORTUNITY_CACHE = {
    "data": None,
    "timestamp": 0,
}

CACHE_TTL_SECONDS = 60 * 60  # 1 hour


def _load_verified_opportunities():
    """Load opportunities from verified_opportunities.json"""

    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)

        opportunities = data.get("opportunities", [])

        # Add source tracking
        for opp in opportunities:
            opp["source"] = "verified"

        return opportunities

    except Exception as e:
        print("Error loading verified_opportunities.json:", e)
        return []


# def fetch_live_opportunities():
#     """
#     Future live opportunities.

#     Phase 2:
#     - GNews
#     - MLH
#     - GDG
#     - Microsoft Reactor

#     For now returns empty list.
#     """

#     return []



def get_opportunities(force_refresh=False):
    """
    Returns all opportunities.
    """

    now = time.time()

    if (
        not force_refresh
        and OPPORTUNITY_CACHE["data"] is not None
        and (now - OPPORTUNITY_CACHE["timestamp"]) < CACHE_TTL_SECONDS
    ):
        return OPPORTUNITY_CACHE["data"]

    # Source 1
    verified = _load_verified_opportunities()

    # Source 2
    live = load_live_opportunities()

    if len(live) == 0:

        print(
        "Live cache empty. Fetching..."
        )

        live = fetch_live_opportunities()

    print(f"Verified: {len(verified)}")
    print(f"Live: {len(live)}")

    # Merge
    opportunities = verified + live

    # Cache
    OPPORTUNITY_CACHE["data"] = opportunities
    OPPORTUNITY_CACHE["timestamp"] = now

    return opportunities

def get_opportunities_by_type(opp_type):
    """
    Filter by category.
    """

    opportunities = get_opportunities()

    if not opp_type or opp_type == "All":
        return opportunities

    return [
        opp
        for opp in opportunities
        if opp.get("type") == opp_type
    ]