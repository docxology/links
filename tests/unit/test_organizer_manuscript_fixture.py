"""Replay the canonical manuscript's local metadata observations."""

import json
from pathlib import Path

from src.data import organize_links as organizer

FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "organizer_neutral.json"


def test_neutral_fixture_round_trip(tmp_path, monkeypatch):
    monkeypatch.setattr(organizer, "MAX_LINKS", 0)
    records = organizer.load_raw_links(FIXTURE)
    assert len(records) == 5
    expected = {
        "political": [],
        "economic": [],
        "social": [records[2]],
        "technological": [records[1], records[4]],
        "other": [records[0], records[3]],
    }
    organized = organizer.categorize_links(records)
    assert organized == expected

    first_output = tmp_path / "first.json"
    second_output = tmp_path / "second.json"
    organizer.save_organized_links(organized, first_output)
    organizer.save_organized_links(organizer.categorize_links(records), second_output)
    assert json.loads(first_output.read_text(encoding="utf-8")) == expected
    assert first_output.read_bytes() == second_output.read_bytes()
    assert expected["other"][0]["url"] == expected["other"][1]["url"]


def test_neutral_fixture_limit(monkeypatch):
    monkeypatch.setattr(organizer, "MAX_LINKS", 2)
    records = organizer.load_raw_links(FIXTURE)
    assert [record["title"] for record in records] == ["Stone", "Exhibit"]
    organized = organizer.categorize_links(records)
    assert {name: len(bucket) for name, bucket in organized.items()} == {
        "political": 0,
        "economic": 0,
        "social": 0,
        "technological": 1,
        "other": 1,
    }
