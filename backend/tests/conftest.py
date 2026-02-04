from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List

import pytest
from fastapi.testclient import TestClient

from app.db import mongo
from app.main import app


class FakeCursor:
    def __init__(self, items: List[Dict[str, Any]]):
        self._items = items

    async def to_list(self, length: int = 100) -> List[Dict[str, Any]]:
        return list(self._items)[:length]


@dataclass
class FakeCollection:
    items: List[Dict[str, Any]] = field(default_factory=list)

    async def create_index(self, *_args: Any, **_kwargs: Any) -> None:
        return None

    async def find_one(self, query: Dict[str, Any]) -> Dict[str, Any] | None:
        for item in self.items:
            if all(item.get(key) == value for key, value in query.items()):
                return item
        return None

    async def insert_one(self, document: Dict[str, Any]) -> None:
        self.items.append(document)

    def find(self, query: Dict[str, Any]) -> FakeCursor:
        results = [item for item in self.items if all(item.get(key) == value for key, value in query.items())]
        return FakeCursor(results)

    async def update_one(self, query: Dict[str, Any], update: Dict[str, Any]) -> None:
        for item in self.items:
            if all(item.get(key) == value for key, value in query.items()):
                if "$set" in update:
                    item.update(update["$set"])
                return None
        return None

    async def delete_one(self, query: Dict[str, Any]):
        for index, item in enumerate(self.items):
            if all(item.get(key) == value for key, value in query.items()):
                self.items.pop(index)
                return type("DeleteResult", (), {"deleted_count": 1})()
        return type("DeleteResult", (), {"deleted_count": 0})()


@dataclass
class FakeDatabase:
    users: FakeCollection = field(default_factory=FakeCollection)
    tasks: FakeCollection = field(default_factory=FakeCollection)


@pytest.fixture()
def client(monkeypatch: pytest.MonkeyPatch) -> Iterable[TestClient]:
    fake_db = FakeDatabase()
    monkeypatch.setattr(mongo, "connect_to_mongo", lambda: None)
    monkeypatch.setattr(mongo, "close_mongo_connection", lambda: None)
    monkeypatch.setattr(mongo, "get_database", lambda: fake_db)

    with TestClient(app) as test_client:
        yield test_client
