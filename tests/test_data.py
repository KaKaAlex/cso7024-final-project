"""Tests for the in-memory delivery data functions."""

from app import data


def test_all_deliveries_returns_all_records():
    deliveries = data.all_deliveries()

    assert len(deliveries) == 5
    assert deliveries[0]["id"] == "NL-1001"


def test_all_deliveries_returns_a_copy():
    deliveries = data.all_deliveries()
    deliveries[0]["status"] = "changed"

    fresh_deliveries = data.all_deliveries()

    assert fresh_deliveries[0]["status"] == "in_transit"


def test_find_delivery_returns_known_delivery():
    delivery = data.find_delivery("NL-1002")

    assert delivery is not None
    assert delivery["destination"] == "Bristol"
    assert delivery["status"] == "delivered"


def test_find_delivery_returns_none_for_unknown_id():
    assert data.find_delivery("NL-9999") is None