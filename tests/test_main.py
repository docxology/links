"""
Tests for ``main`` wiring and ``run_pipeline`` with injected ``PipelineStages``.
"""

import sys
from pathlib import Path

import pytest

from src.pipeline_orchestration import PipelineStages, run_pipeline


def test_main_passes_argv_to_run_pipeline(monkeypatch):
    """``main()`` calls ``parse_pipeline_argv`` with ``sys.argv[1:]`` and ``run_pipeline`` with kwargs."""
    captured = {}

    def fake_parse(argv):
        captured["argv"] = argv
        return {"skip_organize": True, "skip_scrape": False}

    def fake_run(**kwargs):
        captured["kwargs"] = kwargs

    monkeypatch.setattr("src.main.parse_pipeline_argv", fake_parse)
    monkeypatch.setattr("src.main.run_pipeline", fake_run)
    monkeypatch.setattr(sys, "argv", ["prog", "--skip-organize"])

    import src.main as main_mod

    main_mod.main()

    assert captured["argv"] == ["--skip-organize"]
    assert captured["kwargs"] == {"skip_organize": True, "skip_scrape": False}


def test_main_propagates_errors(monkeypatch):
    def fake_parse(_argv):
        return {
            "skip_organize": False,
            "skip_scrape": False,
            "skip_extract": False,
            "skip_organize_extractions": False,
            "skip_essays": False,
            "skip_essay_images": False,
            "skip_analyze": False,
            "skip_render": False,
            "skip_images": False,
        }

    def boom(**_kwargs):
        raise RuntimeError("Test error")

    monkeypatch.setattr("src.main.parse_pipeline_argv", fake_parse)
    monkeypatch.setattr("src.main.run_pipeline", boom)
    monkeypatch.setattr(sys, "argv", ["prog"])

    import src.main as main_mod

    with pytest.raises(RuntimeError, match="Test error"):
        main_mod.main()


def _stage_tracker():
    calls = []

    def mk(name, ret=None):
        def inner():
            calls.append(name)
            return ret

        return inner

    return calls, mk


def test_run_pipeline_calls_all_stages_in_order():
    calls, mk = _stage_tracker()
    stages = PipelineStages(
        organize=mk("organize"),
        scrape=mk("scrape"),
        extract=mk("extract"),
        organize_extractions=mk(
            "organize_extractions",
            {"site_specific_dir": "s", "compiled_dir": "c"},
        ),
        essays=mk("essays", {"essays_dir": "e"}),
        essay_images=mk("essay_images", {"images_dir": "i"}),
        analyze=mk("analyze"),
        render=mk("render", (Path("out.md"), Path("out.html"))),
        images=mk("images", Path("imgdir")),
    )
    run_pipeline(stages=stages)
    assert calls == [
        "organize",
        "scrape",
        "extract",
        "organize_extractions",
        "essays",
        "essay_images",
        "analyze",
        "render",
        "images",
    ]


def test_run_pipeline_respects_skips():
    calls, mk = _stage_tracker()
    stages = PipelineStages(
        organize=mk("organize"),
        scrape=mk("scrape"),
        extract=mk("extract"),
        organize_extractions=mk("organize_extractions", {}),
        essays=mk("essays", {}),
        essay_images=mk("essay_images", {}),
        analyze=mk("analyze"),
        render=mk("render", ("m.md", "h.html")),
        images=mk("images", Path("x")),
    )
    run_pipeline(
        skip_scrape=True,
        skip_extract=True,
        skip_organize_extractions=True,
        skip_essays=True,
        skip_essay_images=True,
        skip_analyze=True,
        skip_render=True,
        skip_images=True,
        stages=stages,
    )
    assert calls == ["organize"]
