"""Seed data for the Northwind delivery-tracking service.

In a production system these records would come from a database. For this
starter they are held in memory so the service runs with no external
dependencies and the focus stays on the DevOps workflow around the code.

Wiring the service up to a real datastore is a reasonable extension, but it is
not required by the brief: keep changes to the application modest.
"""

DELIVERIES = [
    {"id": "NL-1001", "destination": "Manchester", "status": "in_transit", "driver": "A. Okafor"},
    {"id": "NL-1002", "destination": "Bristol", "status": "delivered", "driver": "R. Nowak"},
    {"id": "NL-1003", "destination": "Leeds", "status": "pending", "driver": None},
    {"id": "NL-1004", "destination": "Glasgow", "status": "in_transit", "driver": "S. Patel"},
    {"id": "NL-1005", "destination": "Cardiff", "status": "delivered", "driver": "M. Haddad"},
]


def all_deliveries() -> list[dict]:
    """Return a copy of all delivery records."""
    return [dict(delivery) for delivery in DELIVERIES]


def find_delivery(delivery_id: str) -> dict | None:
    """Return the delivery with the given id, or None if there is no match."""
    for delivery in DELIVERIES:
        if delivery["id"] == delivery_id:
            return dict(delivery)
    return None
