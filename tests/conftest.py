"""
Pytest configuration file for the Links Analysis project.

This file contains fixtures that can be used across all tests.
"""

import os
import json
import pytest
from pathlib import Path


@pytest.fixture
def test_data_dir():
    """Return the path to the test fixtures directory."""
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def sample_urls():
    """Return a sample of URLs for testing."""
    return {
        "tech": [
            {"url": "https://example.com/tech1", "title": "Tech Article 1"},
            {"url": "https://example.com/tech2", "title": "Tech Article 2"}
        ],
        "politics": [
            {"url": "https://example.com/politics1", "title": "Politics Article 1"},
            {"url": "https://example.com/politics2", "title": "Politics Article 2"}
        ]
    }


@pytest.fixture
def sample_tags():
    """Return a sample of tags for testing."""
    return {
        "https://example.com/tech1": ["technology", "ai", "future"],
        "https://example.com/tech2": ["technology", "programming"],
        "https://example.com/politics1": ["politics", "governance"],
        "https://example.com/politics2": ["politics", "election"]
    }


@pytest.fixture
def sample_scraped_data():
    """Return sample scraped data for testing."""
    return {
        "tech": [
            {
                "url": "https://example.com/tech1",
                "title": "Tech Article 1",
                "status": "success",
                "content": {
                    "title": "Tech Article 1",
                    "headings": [
                        {"level": 1, "text": "Main Heading"},
                        {"level": 2, "text": "Subheading 1"}
                    ],
                    "paragraphs": [
                        "This is the first paragraph about technology.",
                        "This is the second paragraph about AI."
                    ],
                    "lists": [
                        {
                            "items": ["List item 1", "List item 2"]
                        }
                    ]
                }
            }
        ],
        "politics": [
            {
                "url": "https://example.com/politics1",
                "title": "Politics Article 1",
                "status": "success",
                "content": {
                    "title": "Politics Article 1",
                    "headings": [
                        {"level": 1, "text": "Main Political Heading"},
                        {"level": 2, "text": "Policy Subheading"}
                    ],
                    "paragraphs": [
                        "This is a paragraph about politics.",
                        "This is a paragraph about governance."
                    ],
                    "lists": [
                        {
                            "items": ["Policy 1", "Policy 2"]
                        }
                    ]
                }
            }
        ]
    }


@pytest.fixture
def sample_extracted_concepts():
    """Return sample extracted concepts for testing."""
    return {
        "tech": [
            {
                "url": "https://example.com/tech1",
                "title": "Tech Article 1",
                "status": "success",
                "concepts": "1. AI Ethics\n- Concept: Establishing ethical guidelines for AI development\n- Implementation: Creating regulatory frameworks\n- Significance: Ensures AI benefits humanity without causing harm"
            }
        ],
        "politics": [
            {
                "url": "https://example.com/politics1",
                "title": "Politics Article 1",
                "status": "success",
                "concepts": "1. Democratic Reform\n- Concept: Improving democratic processes\n- Implementation: Electoral system changes\n- Significance: Increases representation and participation"
            }
        ]
    }


@pytest.fixture
def sample_platform():
    """Return a sample political platform for testing."""
    return {
        "title": "Sample Political Platform",
        "executive_summary": "This is a sample political platform for testing.",
        "categories": {
            "political": {
                "title": "Political Reforms",
                "items": [
                    {
                        "title": "Democratic Reform",
                        "description": "Improving democratic processes",
                        "details": "Electoral system changes to increase representation",
                        "sources": ["https://example.com/politics1"]
                    }
                ]
            },
            "technological": {
                "title": "Technology Policy",
                "items": [
                    {
                        "title": "AI Ethics",
                        "description": "Establishing ethical guidelines for AI",
                        "details": "Creating regulatory frameworks for AI development",
                        "sources": ["https://example.com/tech1"]
                    }
                ]
            }
        }
    } 