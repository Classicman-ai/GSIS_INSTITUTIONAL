import datetime


class EconomicCalendarEngine:

    def __init__(self):

        print("==============================")
        print("GSIS ECONOMIC CALENDAR ENGINE v1.0 ONLINE")
        print("MACRO ECONOMIC INTELLIGENCE ACTIVE")
        print("==============================")

        self.events = []

    def add_event(
        self,
        date,
        currency,
        event,
        impact,
        forecast=None,
        previous=None,
        actual=None
    ):

        self.events.append({

            "date": date,
            "currency": currency,
            "event": event,
            "impact": impact.upper(),
            "forecast": forecast,
            "previous": previous,
            "actual": actual

        })

    def upcoming_events(self):

        return sorted(
            self.events,
            key=lambda x: x["date"]
        )

    def high_impact_events(self):

        return [

            e for e in self.events

            if e["impact"] == "HIGH"

        ]

    def summary(self):

        result = {

            "status": "ECONOMIC CALENDAR READY",

            "total_events": len(self.events),

            "high_impact":

                len(self.high_impact_events()),

            "medium_impact":

                len([
                    e for e in self.events
                    if e["impact"] == "MEDIUM"
                ]),

            "low_impact":

                len([
                    e for e in self.events
                    if e["impact"] == "LOW"
                ]),

            "timestamp":

                datetime.datetime.now(
                    datetime.timezone.utc
                ).isoformat()

        }

        print("==============================")
        print("GSIS ECONOMIC CALENDAR SUMMARY")
        print("==============================")
        print(result)

        return result


if __name__ == "__main__":

    engine = EconomicCalendarEngine()

    engine.add_event(
        "2026-08-05 18:00 UTC",
        "USD",
        "FOMC Interest Rate Decision",
        "HIGH",
        "4.25%",
        "4.25%"
    )

    engine.add_event(
        "2026-08-07 12:30 UTC",
        "USD",
        "Non-Farm Payrolls",
        "HIGH",
        "185K",
        "172K"
    )

    engine.add_event(
        "2026-08-12 12:30 UTC",
        "USD",
        "Consumer Price Index",
        "HIGH",
        "2.6%",
        "2.5%"
    )

    engine.summary()

    print()

    for event in engine.upcoming_events():

        print(event)
