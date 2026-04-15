"""
Tests for ``parse_pipeline_argv`` (pure argparse → ``run_pipeline`` kwargs).
"""

import pytest

from src.pipeline_cli import parse_pipeline_argv


def _all_skip_false():
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


def test_no_args():
    assert parse_pipeline_argv([]) == _all_skip_false()


def test_skip_flags():
    assert parse_pipeline_argv(["--skip-organize", "--skip-scrape"]) == {
        **_all_skip_false(),
        "skip_organize": True,
        "skip_scrape": True,
    }


def test_only_extract():
    assert parse_pipeline_argv(["--only-extract"]) == {
        "skip_organize": True,
        "skip_scrape": True,
        "skip_extract": False,
        "skip_organize_extractions": True,
        "skip_essays": True,
        "skip_essay_images": True,
        "skip_analyze": True,
        "skip_render": True,
        "skip_images": True,
    }


def test_later_only_wins():
    """Later ``--only-*`` wins: extract then analyze leaves only analyze running."""
    assert parse_pipeline_argv(["--only-extract", "--only-analyze"]) == {
        "skip_organize": True,
        "skip_scrape": True,
        "skip_extract": True,
        "skip_organize_extractions": True,
        "skip_essays": True,
        "skip_essay_images": True,
        "skip_analyze": False,
        "skip_render": True,
        "skip_images": True,
    }


def test_only_extract_overrides_extra_skip():
    """``--only-extract`` wins over extra ``--skip-images``."""
    assert parse_pipeline_argv(["--only-extract", "--skip-images"]) == {
        "skip_organize": True,
        "skip_scrape": True,
        "skip_extract": False,
        "skip_organize_extractions": True,
        "skip_essays": True,
        "skip_essay_images": True,
        "skip_analyze": True,
        "skip_render": True,
        "skip_images": True,
    }


def test_parse_rejects_unknown():
    with pytest.raises(SystemExit):
        parse_pipeline_argv(["--not-a-real-flag"])
