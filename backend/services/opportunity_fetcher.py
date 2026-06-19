import requests

from services.opportunity_scraper import (
    save_live_opportunities
)

from services.gdg_scraper import (
    fetch_gdg_events
)


def fetch_live_opportunities():

    opportunities = []

    gdg_events = fetch_gdg_events()

    opportunities.extend(
        gdg_events
    )

    save_live_opportunities(
        opportunities
    )

    print(
        f"Saved {len(opportunities)} live opportunities"
    )

    return opportunities