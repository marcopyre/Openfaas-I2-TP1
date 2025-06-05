from handler import handle
import json
import redis
import os
import re

def test_handle_valid_json(monkeypatch):
    class MockRedis:
        def __init__(self, *args, **kwargs):
            self.store = {}

        def set(self, key, value):
            self.store[key] = value

    monkeypatch.setattr(redis, "Redis", lambda *args, **kwargs: MockRedis())

    payload = json.dumps({"message": "Super retour utilisateur"})
    response = json.loads(handle(payload))

    assert response["status"] == "success"
    assert response["message"] == "Feedback saved successfully"
    assert response["key"].startswith("feedback:")


def test_handle_raw_text(monkeypatch):
    class MockRedis:
        def __init__(self, *args, **kwargs):
            self.store = {}

        def set(self, key, value):
            self.store[key] = value

    monkeypatch.setattr(redis, "Redis", lambda *args, **kwargs: MockRedis())

    response = json.loads(handle("Juste un texte brut"))

    assert response["status"] == "success"
    assert "key" in response


def test_handle_empty():
    response = json.loads(handle(""))

    assert response["status"] == "error"
    assert response["error"] == "No message provided"

