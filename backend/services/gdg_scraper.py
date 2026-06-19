import requests


def fetch_gdg_events():

    opportunities = []

    url = (
        "https://gdg.community.dev/api/search/"
        "?result_types=upcoming_event"
        "&order_by_proximity=true"
        "&proximity=3300"
    )

    try:

        response = requests.get(
            url,
            headers={
                "Accept": "application/json; version=bevy.1.0"
            },
            timeout=20
        )

        data = response.json()

        print("GDG API Response Keys:")
        print(data.keys())

        results = data.get("results", [])

        for event in results[:10]:

            print("\n========== EVENT ==========")
            print(event.get("title"))
            print("===========================\n")

            opportunities.append({

                "id":
                    f"gdg-{event.get('id')}",

                "title":
                    event.get(
                        "title",
                        "GDG Event"
                    ),

                "company":
                    event.get(
                        "chapter",
                        {}
                    ).get(
                        "title",
                        "Google Developer Groups"
                    ),

                "desc":
                    event.get(
                        "description_short",
                        "GDG Community Event"
                    ),

                "image":
                    (
                        event.get(
                            "picture",
                            {}
                        ).get(
                            "url"
                        )
                        or
                        event.get(
                            "event_type_logo",
                            {}
                        ).get(
                            "url"
                        )
                        or
                        "/images/opportunitiescard6.png"
                    ),

                "link":
                    event.get(
                        "url",
                        ""
                    ),

                "deadline":
                    event.get(
                        "start_date",
                        "Check Website"
                    ),

                "location":
                    event.get(
                        "city",
                        "Online"
                    ),

                "stipend":
                    "",

                "tags":
                    event.get(
                        "tags",
                        []
                    ),

                "type":
                    "Workshops",

                "source":
                    "live"
            })

        print(
            f"GDG Events Found: {len(opportunities)}"
        )

    except Exception as e:

        print(
            "GDG API Error:",
            e
        )

    return opportunities
