import requests


def fetch_reactor_events():

    opportunities = []

    try:

        for page in range(1, 4):

            response = requests.get(
                f"https://developer.microsoft.com/reactor/api/events?page={page}",
                timeout=20
            )

            data = response.json()

            events = data.get(
                "items",
                []
            )

            for event in events:

                registration_url = event.get(
                    "primaryRegistrationUrl"
                )

                if not registration_url:
                    continue

                # English only
                languages = event.get(
                    "languages",
                    []
                )

                if languages:

                    english_found = False

                    for lang in languages:

                        lang_text = str(lang).lower()

                        if "english" in lang_text:
                            english_found = True
                            break

                    if not english_found:
                        continue

                has_livestream = event.get(
                    "hasLivestreamSession",
                    False
                )

                is_hybrid = event.get(
                    "isHybrid",
                    False
                )

                location_city = (
                    event.get(
                        "locationDisplayCity"
                    )
                    or ""
                )

                # Indian cities
                indian_cities = [
                    "mumbai",
                    "pune",
                    "bangalore",
                    "bengaluru",
                    "hyderabad",
                    "chennai",
                    "delhi",
                    "kolkata",
                    "ahmedabad",
                    "kochi",
                    "goa",
                    "nagpur",
                    "bhubaneswar"
                ]

                is_indian_event = any(
                    city in location_city.lower()
                    for city in indian_cities
                )

                # Keep:
                # 1. Indian events
                # 2. Livestream events
                # 3. Hybrid events

                if not (
                    is_indian_event
                    or has_livestream
                    or is_hybrid
                ):
                    continue

                # Display location

                if is_indian_event:

                    display_location = location_city

                elif has_livestream or is_hybrid:

                    display_location = "Online"

                else:

                    display_location = "Online"

                print("\n========== EVENT ==========")
                print(event.get("title"))
                print("===========================\n")
                
                opportunities.append({

                    "id":
                        f"reactor-{event.get('id')}",

                    "title":
                        event.get(
                            "title",
                            "Microsoft Reactor Event"
                        ),

                    "company":
                        "Microsoft Reactor",

                    "desc":
                        (
                            event.get(
                                "description",
                                ""
                            )[:140]
                            + "..."
                        ),

                    "image":
                        event.get(
                            "imageUrl",
                            "/images/opportunitiescard6.png"
                        ),

                    "link":
                        registration_url,

                    "deadline":
                        event.get(
                            "startDateTimeUser"
                        ),

                    "location":
                        display_location,

                    "stipend":
                        "",

                    "tags":
                        [
                            "microsoft",
                            "reactor",
                            "workshop"
                        ],

                    "type":
                        "Workshops",

                    "source":
                        "live"
                })

                if len(opportunities) >= 10:

                    print(
                        f"Reactor Events Found: {len(opportunities)}"
                    )

                    return opportunities

        print(
            f"Reactor Events Found: {len(opportunities)}"
        )

    except Exception as e:

        print(
            "Reactor API Error:",
            e
        )

    return opportunities