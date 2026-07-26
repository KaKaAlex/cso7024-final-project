"""Integration tests for the Northwind HTTP API."""

import json
import threading
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer

import pytest

from app.service import DeliveryHandler


@pytest.fixture
def service_url():
    server = ThreadingHTTPServer(("127.0.0.1", 0), DeliveryHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    host, port = server.server_address
    yield f"http://{host}:{port}"

    server.shutdown()
    server.server_close()
    thread.join()


def get_json(url):
    with urllib.request.urlopen(url) as response:
        return response.status, json.loads(response.read())


def test_health_endpoint(service_url):
    status, body = get_json(f"{service_url}/health")

    assert status == 200
    assert body == {"status": "ok"}


def test_deliveries_endpoint_returns_all_records(service_url):
    status, body = get_json(f"{service_url}/deliveries")

    assert status == 200
    assert len(body) == 5


def test_known_delivery_endpoint(service_url):
    status, body = get_json(f"{service_url}/deliveries/NL-1002")

    assert status == 200
    assert body["destination"] == "Bristol"
    assert body["status"] == "delivered"


def test_unknown_delivery_returns_404(service_url):
    with pytest.raises(urllib.error.HTTPError) as error:
        urllib.request.urlopen(f"{service_url}/deliveries/NL-9999")

    assert error.value.code == 404
    body = json.loads(error.value.read())
    assert body == {"error": "No delivery with id NL-9999"}


def test_unknown_route_returns_404(service_url):
    with pytest.raises(urllib.error.HTTPError) as error:
        urllib.request.urlopen(f"{service_url}/unknown")

    assert error.value.code == 404