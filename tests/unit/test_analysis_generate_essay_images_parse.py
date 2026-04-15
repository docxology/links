"""Unit tests for essay image prompt JSON parsing (no API calls)."""

import pytest

from src.analysis.generate_essay_images import _parse_two_prompt_strings


def test_parse_strict_json_array():
    assert _parse_two_prompt_strings('["a", "b"]') == ["a", "b"]


def test_parse_strips_whitespace():
    assert _parse_two_prompt_strings('  ["  x  ", "y"]  ') == ["x", "y"]


def test_parse_json_in_markdown_fence():
    raw = 'Here:\n```json\n["one", "two"]\n```'
    assert _parse_two_prompt_strings(raw) == ["one", "two"]


def test_parse_rejects_wrong_length():
    with pytest.raises(ValueError):
        _parse_two_prompt_strings('["only"]')


def test_parse_rejects_non_strings():
    with pytest.raises(ValueError):
        _parse_two_prompt_strings("[1, 2]")


def test_parse_rejects_empty_strings():
    with pytest.raises(ValueError):
        _parse_two_prompt_strings('["a", ""]')
