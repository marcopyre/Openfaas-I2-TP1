from handler import handle
import json
import re

def test_handle_returns_valid_json():
    response_raw = handle(None)
    response = json.loads(response_raw)

    assert "quote" in response
    assert "status" in response
    assert response["status"] == "success"
    assert isinstance(response["quote"], str)
    assert len(response["quote"]) > 0

def test_handle_returns_different_quotes():
    quotes = set()
    for _ in range(10):
        response = json.loads(handle(None))
        quotes.add(response["quote"])

    # Il devrait y avoir plus d'une citation différente (car choix aléatoire parmi 5)
    assert len(quotes) > 1
