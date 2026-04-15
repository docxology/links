"""
Live OpenAI API checks (opt-in; excluded from default ``pytest`` run).

Run: ``uv run pytest tests/live -m live_openai``
"""

import os

import pytest

pytestmark = pytest.mark.live_openai


@pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="OPENAI_API_KEY not set")
def test_models_list_smoke():
    """Minimal authenticated call: list models (no completion charges)."""
    from openai import OpenAI

    client = OpenAI()
    models = client.models.list()
    assert models.data
    assert any(m.id for m in models.data)
