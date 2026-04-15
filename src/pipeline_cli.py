"""
CLI parsing for the pipeline: pure argparse → skip kwargs (testable without mocks).
"""

from __future__ import annotations

import argparse
from typing import Any


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the links analysis pipeline")
    parser.add_argument("--skip-organize", action="store_true", help="Skip the organize links stage")
    parser.add_argument("--skip-scrape", action="store_true", help="Skip the scrape websites stage")
    parser.add_argument("--skip-extract", action="store_true", help="Skip the extract categories stage")
    parser.add_argument("--skip-organize-extractions", action="store_true", help="Skip the organize extractions stage")
    parser.add_argument("--skip-essays", action="store_true", help="Skip the essay generation stage")
    parser.add_argument("--skip-essay-images", action="store_true", help="Skip the essay image generation stage")
    parser.add_argument("--skip-analyze", action="store_true", help="Skip the generate platform stage")
    parser.add_argument("--skip-render", action="store_true", help="Skip the Markdown rendering stage")
    parser.add_argument("--skip-images", action="store_true", help="Skip the image generation stage")
    parser.add_argument("--only-organize", action="store_true", help="Run only the organize links stage")
    parser.add_argument("--only-scrape", action="store_true", help="Run only the scrape websites stage")
    parser.add_argument("--only-extract", action="store_true", help="Run only the extract categories stage")
    parser.add_argument("--only-organize-extractions", action="store_true", help="Run only the organize extractions stage")
    parser.add_argument("--only-essays", action="store_true", help="Run only the essay generation stage")
    parser.add_argument("--only-essay-images", action="store_true", help="Run only the essay image generation stage")
    parser.add_argument("--only-analyze", action="store_true", help="Run only the generate platform stage")
    parser.add_argument("--only-render", action="store_true", help="Run only the Markdown rendering stage")
    parser.add_argument("--only-images", action="store_true", help="Run only the image generation stage")
    return parser


def apply_only_flags(args: argparse.Namespace) -> None:
    """Mutate skip flags so exactly one stage runs when an --only-* flag is set (fixed script order)."""
    if args.only_organize:
        args.skip_scrape = True
        args.skip_extract = True
        args.skip_organize_extractions = True
        args.skip_essays = True
        args.skip_essay_images = True
        args.skip_analyze = True
        args.skip_render = True
        args.skip_images = True
        args.skip_organize = False
    if args.only_scrape:
        args.skip_organize = True
        args.skip_extract = True
        args.skip_organize_extractions = True
        args.skip_essays = True
        args.skip_essay_images = True
        args.skip_analyze = True
        args.skip_render = True
        args.skip_images = True
        args.skip_scrape = False
    if args.only_extract:
        args.skip_organize = True
        args.skip_scrape = True
        args.skip_organize_extractions = True
        args.skip_essays = True
        args.skip_essay_images = True
        args.skip_analyze = True
        args.skip_render = True
        args.skip_images = True
        args.skip_extract = False
    if args.only_organize_extractions:
        args.skip_organize = True
        args.skip_scrape = True
        args.skip_extract = True
        args.skip_essays = True
        args.skip_essay_images = True
        args.skip_analyze = True
        args.skip_render = True
        args.skip_images = True
        args.skip_organize_extractions = False
    if args.only_essays:
        args.skip_organize = True
        args.skip_scrape = True
        args.skip_extract = True
        args.skip_organize_extractions = True
        args.skip_essay_images = True
        args.skip_analyze = True
        args.skip_render = True
        args.skip_images = True
        args.skip_essays = False
    if args.only_essay_images:
        args.skip_organize = True
        args.skip_scrape = True
        args.skip_extract = True
        args.skip_organize_extractions = True
        args.skip_essays = True
        args.skip_analyze = True
        args.skip_render = True
        args.skip_images = True
        args.skip_essay_images = False
    if args.only_analyze:
        args.skip_organize = True
        args.skip_scrape = True
        args.skip_extract = True
        args.skip_organize_extractions = True
        args.skip_essays = True
        args.skip_essay_images = True
        args.skip_render = True
        args.skip_images = True
        args.skip_analyze = False
    if args.only_render:
        args.skip_organize = True
        args.skip_scrape = True
        args.skip_extract = True
        args.skip_organize_extractions = True
        args.skip_essays = True
        args.skip_essay_images = True
        args.skip_analyze = True
        args.skip_images = True
        args.skip_render = False
    if args.only_images:
        args.skip_organize = True
        args.skip_scrape = True
        args.skip_extract = True
        args.skip_organize_extractions = True
        args.skip_essays = True
        args.skip_essay_images = True
        args.skip_analyze = True
        args.skip_render = True
        args.skip_images = False


def parse_pipeline_argv(argv: list[str]) -> dict[str, Any]:
    """Parse argv (no program name) and return kwargs for run_pipeline()."""
    parser = build_parser()
    args = parser.parse_args(argv)
    apply_only_flags(args)
    return {
        "skip_organize": args.skip_organize,
        "skip_scrape": args.skip_scrape,
        "skip_extract": args.skip_extract,
        "skip_organize_extractions": args.skip_organize_extractions,
        "skip_essays": args.skip_essays,
        "skip_essay_images": args.skip_essay_images,
        "skip_analyze": args.skip_analyze,
        "skip_render": args.skip_render,
        "skip_images": args.skip_images,
    }
