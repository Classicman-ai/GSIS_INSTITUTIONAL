"""
=========================================================

GSIS INSTITUTIONAL

EVENT BUS ENGINE

Version 1.0

Internal Communication Layer

=========================================================
"""

from collections import defaultdict
from datetime import datetime, UTC


class EventBus:

    def __init__(self):

        self.name = "GSIS Event Bus"

        self.status = "ONLINE"

        self.subscribers = defaultdict(list)

    def subscribe(self, event_name, callback):

        self.subscribers[event_name].append(callback)

        print(f"[SUBSCRIBED] {callback.__name__} -> {event_name}")

    def publish(self, event_name, data):

        print(f"[EVENT] {event_name}")

        for callback in self.subscribers[event_name]:

            callback(data)

    def report(self):

        return {

            "status": self.status,

            "events": len(self.subscribers),

            "time": datetime.now(UTC).isoformat()

        }


event_bus = EventBus()
