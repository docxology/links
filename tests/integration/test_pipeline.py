"""
Integration tests for the links analysis pipeline.

Stage mains are exercised with mocks; optional tests skip when repo artifacts are absent.
"""

import json
from pathlib import Path
from unittest.mock import patch

import pytest


@pytest.fixture
def setup_test_data(tmp_path, sample_urls, sample_tags):
    """Set up test data files for the pipeline."""
    urls_path = tmp_path / "bestofnow_urls.json"
    tags_path = tmp_path / "bestofnow_tags.json"

    with open(urls_path, "w", encoding="utf-8") as f:
        json.dump(sample_urls, f)

    with open(tags_path, "w", encoding="utf-8") as f:
        json.dump(sample_tags, f)

    data_dir = tmp_path / "data"
    data_dir.mkdir(exist_ok=True)

    output_dir = tmp_path / "output"
    output_dir.mkdir(exist_ok=True)

    logs_dir = tmp_path / "logs"
    logs_dir.mkdir(exist_ok=True)

    return {
        "tmp_path": tmp_path,
        "urls_path": urls_path,
        "tags_path": tags_path,
        "data_dir": data_dir,
        "output_dir": output_dir,
        "logs_dir": logs_dir,
    }


@patch("src.data.organize_links.save_organized_links")
def test_organize_links_integration(mock_save, setup_test_data):
    """organize_links.main reads RAW_LINKS_PATH and writes categorized links."""
    organized_path = setup_test_data["data_dir"] / "organized_links.json"
    with patch("src.data.organize_links.RAW_LINKS_PATH", setup_test_data["urls_path"]), patch(
        "src.data.organize_links.ORGANIZED_LINKS_PATH", organized_path
    ):
        from src.data.organize_links import main

        main()

    mock_save.assert_called_once()
    organized_links = mock_save.call_args[0][0]
    assert set(organized_links.keys()) == {
        "political",
        "economic",
        "social",
        "technological",
        "other",
    }
    for _cat, links in organized_links.items():
        for link in links:
            assert "url" in link
            assert "title" in link


@patch("src.scrapers.scrape_sites.scrape_links")
@patch("src.scrapers.scrape_sites.save_scraped_data")
def test_scrape_sites_integration(mock_save, mock_scrape, setup_test_data):
    """scrape_sites.main loads organized JSON and saves scraped data."""
    organized_links = {
        "political": [
            {"url": "https://example.com/politics1", "title": "Democratic Reform", "tags": ["politics"]}
        ],
        "economic": [],
        "social": [],
        "technological": [],
        "other": [],
    }
    organized_links_path = setup_test_data["data_dir"] / "organized_links.json"
    with open(organized_links_path, "w", encoding="utf-8") as f:
        json.dump(organized_links, f)

    fake_scraped = {
        "political": [
            {"url": "https://example.com/politics1", "status": "success", "content": {"title": "P"}}
        ]
    }
    mock_scrape.return_value = fake_scraped
    scraped_path = setup_test_data["data_dir"] / "scraped_data.json"

    with patch("src.scrapers.scrape_sites.ORGANIZED_LINKS_PATH", organized_links_path), patch(
        "src.scrapers.scrape_sites.SCRAPED_DATA_PATH", scraped_path
    ):
        from src.scrapers.scrape_sites import main

        main()

    mock_scrape.assert_called_once()
    mock_save.assert_called_once_with(fake_scraped, scraped_path)


@patch("src.analysis.extract_concepts.extract_concepts")
@patch("src.analysis.extract_concepts.save_extracted_concepts")
def test_extract_concepts_integration(mock_save, mock_extract, setup_test_data, sample_scraped_data):
    """extract_concepts.main loads scraped JSON and persists extractions."""
    scraped_data_path = setup_test_data["data_dir"] / "scraped_data.json"
    with open(scraped_data_path, "w", encoding="utf-8") as f:
        json.dump(sample_scraped_data, f)

    mock_extract.return_value = {
        "tech": [
            {
                "url": "https://example.com/tech1",
                "title": "Tech Article 1",
                "status": "success",
                "categories": {"principles": [], "policies": [], "values": [], "goals": []},
            }
        ]
    }
    out_path = setup_test_data["output_dir"] / "extracted_concepts.json"

    with patch("src.analysis.extract_concepts.SCRAPED_DATA_PATH", scraped_data_path), patch(
        "src.analysis.extract_concepts.EXTRACTED_CONCEPTS_PATH", out_path
    ):
        from src.analysis.extract_concepts import main

        main()

    mock_extract.assert_called_once_with(sample_scraped_data)
    mock_save.assert_called_once_with(mock_extract.return_value, out_path)


@patch("src.analysis.generate_platform.generate_platform")
@patch("src.analysis.generate_platform.save_platform")
def test_generate_platform_integration(mock_save, mock_generate, setup_test_data, sample_extracted_concepts):
    """generate_platform.main loads extractions and saves platform JSON."""
    concepts_path = setup_test_data["output_dir"] / "extracted_concepts.json"
    with open(concepts_path, "w", encoding="utf-8") as f:
        json.dump(sample_extracted_concepts, f)

    mock_platform = {
        "executive_summary": "Summary.",
        "political": "Section",
        "economic": "Economic",
        "social": "Social",
        "technological": "Tech",
        "other": "Other",
    }
    mock_generate.return_value = mock_platform
    platform_path = setup_test_data["output_dir"] / "political_platform.json"

    with patch("src.analysis.generate_platform.EXTRACTED_CONCEPTS_PATH", concepts_path), patch(
        "src.analysis.generate_platform.PLATFORM_OUTPUT_PATH", platform_path
    ):
        from src.analysis.generate_platform import main

        main()

    mock_generate.assert_called_once_with(sample_extracted_concepts)
    mock_save.assert_called_once_with(mock_platform, platform_path)


@patch("src.analysis.render_markdown.load_platform_data")
@patch("src.analysis.render_markdown.save_html")
@patch("src.analysis.render_markdown.save_markdown")
@patch("src.analysis.render_markdown.render_html")
@patch("src.analysis.render_markdown.render_markdown")
def test_render_markdown_integration(
    mock_rm, mock_rh, mock_sm, mock_sh, mock_load, setup_test_data, sample_platform
):
    """render_markdown.main writes MD and HTML; returns path tuple."""
    mock_load.return_value = sample_platform
    mock_rm.return_value = "# Sample\n"
    mock_rh.return_value = "<html></html>"
    out = setup_test_data["output_dir"]
    md_path = out / "political_platform.md"
    html_path = out / "political_platform.html"
    platform_json = out / "political_platform.json"

    with patch("src.analysis.render_markdown.PLATFORM_OUTPUT_PATH", platform_json), patch(
        "src.analysis.render_markdown.MARKDOWN_OUTPUT_PATH", md_path
    ), patch("src.analysis.render_markdown.HTML_OUTPUT_PATH", html_path):
        from src.analysis.render_markdown import main

        result = main()

    mock_rm.assert_called_once_with(sample_platform)
    mock_rh.assert_called_once_with(sample_platform)
    mock_sm.assert_called_once_with(mock_rm.return_value, md_path)
    mock_sh.assert_called_once_with(mock_rh.return_value, html_path)
    assert result == (md_path, html_path)


def test_pipeline_flow(setup_test_data):
    """Full ``run_pipeline`` calls each injected stage in order."""
    from pathlib import Path

    from src.pipeline_orchestration import PipelineStages, run_pipeline

    calls = []

    def mk(name, ret=None):
        def inner():
            calls.append(name)
            return ret

        return inner

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
        render=mk("render", ("m.md", "h.html")),
        images=mk("images", Path("img")),
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


@pytest.mark.skipif(
    not Path(__file__).resolve().parents[2].joinpath("bestofnow_urls.json").exists(),
    reason="bestofnow_urls.json not in repo",
)
def test_real_data_loaders():
    """Smoke-test loaders against committed inputs when present."""
    from src.utils.config import (
        RAW_LINKS_PATH,
        ORGANIZED_LINKS_PATH,
        SCRAPED_DATA_PATH,
        EXTRACTED_CONCEPTS_PATH,
        PLATFORM_OUTPUT_PATH,
    )
    from src.data.organize_links import load_raw_links
    from src.scrapers.scrape_sites import load_organized_links
    from src.analysis.extract_concepts import load_scraped_data
    from src.analysis.generate_platform import load_extracted_concepts

    raw = load_raw_links(RAW_LINKS_PATH)
    assert isinstance(raw, list)
    assert len(raw) > 0

    if ORGANIZED_LINKS_PATH.exists():
        org = load_organized_links(ORGANIZED_LINKS_PATH)
        assert isinstance(org, dict)

    if SCRAPED_DATA_PATH.exists():
        scraped = load_scraped_data(SCRAPED_DATA_PATH)
        assert isinstance(scraped, dict)

    if EXTRACTED_CONCEPTS_PATH.exists():
        from src.analysis.generate_platform import load_extracted_concepts

        ext = load_extracted_concepts(EXTRACTED_CONCEPTS_PATH)
        assert isinstance(ext, dict)

    if PLATFORM_OUTPUT_PATH.exists():
        plat = load_extracted_concepts(PLATFORM_OUTPUT_PATH)
        assert isinstance(plat, dict)
        assert "executive_summary" in plat


@pytest.mark.skipif(
    not Path(__file__).resolve().parents[2].joinpath("output", "political_platform.json").exists(),
    reason="no output/political_platform.json",
)
def test_output_files_structure():
    """When platform output exists, JSON/MD/HTML have expected headings."""
    from src.utils.config import PLATFORM_OUTPUT_PATH
    from src.analysis.render_markdown import MARKDOWN_OUTPUT_PATH, HTML_OUTPUT_PATH

    with open(PLATFORM_OUTPUT_PATH, "r", encoding="utf-8") as f:
        platform_data = json.load(f)

    assert isinstance(platform_data, dict)
    assert "executive_summary" in platform_data

    exec_summary = platform_data["executive_summary"]
    assert exec_summary != "Error generating executive summary."
    assert len(str(exec_summary)) > 10

    categories = ["political", "economic", "social", "technological", "other"]
    has_content = any(
        category in platform_data
        and platform_data[category]
        and platform_data[category] != "No data available for this category."
        for category in categories
    )
    assert has_content, "No category has meaningful content"

    if MARKDOWN_OUTPUT_PATH.exists():
        with open(MARKDOWN_OUTPUT_PATH, "r", encoding="utf-8") as f:
            markdown_content = f.read()
        assert "# Political Platform" in markdown_content
        assert "## Executive Summary" in markdown_content

    if HTML_OUTPUT_PATH.exists():
        with open(HTML_OUTPUT_PATH, "r", encoding="utf-8") as f:
            html_content = f.read()
        assert "<!DOCTYPE html>" in html_content
        assert "<title>Political Platform</title>" in html_content


@pytest.mark.skipif(
    not Path(__file__).resolve().parents[2].joinpath("output", "political_platform.json").exists(),
    reason="no platform JSON for prompts",
)
def test_image_generation_prompts_with_repo_platform():
    """Prompt generation from committed platform JSON (no image API calls)."""
    from src.utils.config import PLATFORM_OUTPUT_PATH
    from src.analysis.generate_images import load_platform_data, generate_image_prompts

    platform_data = load_platform_data(PLATFORM_OUTPUT_PATH)
    prompts = generate_image_prompts(platform_data, num_prompts=5)
    assert len(prompts) == 5
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)
