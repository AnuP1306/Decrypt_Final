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

COURSES_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "static",
    "data",
    "verified_courses.json"
)

# Cache
OPPORTUNITY_CACHE = {
    "data": None,
    "timestamp": 0,
}

CACHE_TTL_SECONDS = 60 * 60  # 1 hour

def shorten_description(text):

    if not text:
        return ""

    text = text.strip()

    if len(text) <= 120:
        return text

    return text[:120] + "..."

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
    
    
def _load_verified_courses():
    try:

        with open(
            COURSES_PATH,
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)

        courses = data.get(
            "courses",
            []
        )

        for course in courses:
            course["source"] = "verified"

        return courses

    except Exception as e:

        print(
            "Error loading verified_courses.json:",
            e
        )

        return []
    
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
    verified_opportunities = (
    _load_verified_opportunities()
    )

    verified_courses = (
        _load_verified_courses()
    )

    verified = (
        verified_opportunities
        +
        verified_courses
    )

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

    # Remove duplicates
    seen = set()
    unique_opportunities = []

    for opp in opportunities:

        title = (
            opp.get(
                "title",
                ""
            )
            .strip()
            .lower()
        )

        if title in seen:
            continue

        seen.add(title)

        unique_opportunities.append(
            opp
        )

    opportunities = unique_opportunities
    live_opps = [
        o for o in opportunities
        if o.get("source") == "live"
    ]

    verified_opps = [
        o for o in opportunities
        if o.get("source") == "verified"
    ]

    opportunities = (
        live_opps +
        verified_opps
    )

    # Cache
    OPPORTUNITY_CACHE["data"] = opportunities
    OPPORTUNITY_CACHE["timestamp"] = now

    for opp in opportunities:

        opp["desc"] = shorten_description(
            opp.get("desc", "")
        )

        opp["tags"] = opp.get(
            "tags",
            []
        )[:4]
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