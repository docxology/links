#!/usr/bin/env python3
"""
Validation script to ensure the extraction pipeline is working correctly with the new definitions and requirements.

This script validates:
1. Proper extraction of Principles, Policies, Values, Goals with correct definitions
2. Source attribution in compiled data
3. Essay quality (source citations and quotes)
4. Image generation functionality
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, Any

def validate_extraction_definitions():
    """Validate that extraction is using correct category definitions."""
    print("🔍 Validating extraction definitions...")

    extract_file = Path("src/analysis/extract_concepts.py")
    if not extract_file.exists():
        print("❌ extract_concepts.py not found")
        return False

    with open(extract_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check for correct category definitions
    required_definitions = [
        "PRINCIPLES** (deep first values)",
        "POLICIES** (actions of individuals and collectives)",
        "VALUES** (what matters)",
        "GOALS** (desired endpoints)"
    ]

    for definition in required_definitions:
        if definition in content:
            print(f"✅ Found: {definition}")
        else:
            print(f"❌ Missing: {definition}")
            return False

    print("✅ All extraction definitions are correct")
    return True

def validate_compiled_data():
    """Validate that compiled data maintains proper source attribution."""
    print("\n🔍 Validating compiled data structure...")

    compiled_dir = Path("output/compiled")
    if not compiled_dir.exists():
        print("❌ Compiled directory not found - run extraction first")
        return False

    categories = ["principles", "policies", "values", "goals"]
    all_valid = True

    for category in categories:
        json_file = compiled_dir / f"{category}.json"
        if not json_file.exists():
            print(f"❌ {category}.json not found")
            all_valid = False
            continue

        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if "items" not in data:
            print(f"❌ {category}.json missing 'items' field")
            all_valid = False
            continue

        items = data["items"]
        print(f"📊 {category}: {len(items)} items")

        # Check that each item has source attribution
        for i, item in enumerate(items[:3]):  # Check first 3 items
            if "source_url" not in item or "source_title" not in item:
                print(f"❌ Item {i+1} in {category} missing source attribution")
                all_valid = False
            else:
                print(f"✅ Item {i+1} in {category} has source: {item['source_title'][:50]}...")

        # Check that each item has required fields
        required_fields = ["title", "content", "explanation"]
        for item in items[:3]:
            for field in required_fields:
                if field not in item:
                    print(f"❌ Item in {category} missing '{field}' field")
                    all_valid = False

    return all_valid

def validate_essays():
    """Validate that essays properly cite sources and include quotes."""
    print("\n🔍 Validating essay quality...")

    essays_dir = Path("output/essays")
    if not essays_dir.exists():
        print("❌ Essays directory not found - run essay generation first")
        return False

    # Import the validation function
    sys.path.append(str(Path(__file__).parent / "src" / "analysis"))
    try:
        from generate_essays import validate_essay_quality
    except ImportError:
        print("❌ Could not import validation function")
        return False

    categories = ["principles", "policies", "values", "goals"]
    all_valid = True

    for category in categories:
        essay_file = essays_dir / f"{category}_essay.md"
        if not essay_file.exists():
            print(f"❌ {category}_essay.md not found")
            all_valid = False
            continue

        with open(essay_file, 'r', encoding='utf-8') as f:
            essay_content = f.read()

        validation = validate_essay_quality(essay_content, category)

        if not validation["has_source_citations"]:
            print(f"❌ {category} essay missing source citations")
            all_valid = False
        else:
            print(f"✅ {category} essay has source citations ({validation['citation_count']})")

        if not validation["has_quotes"]:
            print(f"❌ {category} essay missing quotes")
            all_valid = False
        else:
            print(f"✅ {category} essay has quotes ({validation['quote_count']})")

        if not validation["has_structure"]:
            print(f"❌ {category} essay missing proper structure")
            all_valid = False
        else:
            print(f"✅ {category} essay has proper structure")

        print(f"📊 {category} essay: {validation['word_count']} words")

    return all_valid

def validate_images():
    """Validate that images were generated successfully."""
    print("\n🔍 Validating image generation...")

    images_dir = Path("output/essay_images")
    if not images_dir.exists():
        print("❌ Essay images directory not found - run image generation first")
        return False

    # Check for image files
    image_files = list(images_dir.glob("*.png"))
    expected_count = 8  # 4 categories × 2 images each

    print(f"📊 Found {len(image_files)} image files (expected: {expected_count})")

    categories = ["principles", "policies", "values", "goals"]
    all_valid = True

    for category in categories:
        category_images = [f for f in image_files if f.name.startswith(category)]
        if len(category_images) != 2:
            print(f"❌ {category}: Expected 2 images, found {len(category_images)}")
            all_valid = False
        else:
            print(f"✅ {category}: Found 2 images")
            for img in category_images:
                size = img.stat().st_size
                print(f"   - {img.name}: {size} bytes")

    # Check for summary file
    summary_file = images_dir / "generation_summary.json"
    if summary_file.exists():
        print("✅ Image generation summary found")
        with open(summary_file, 'r', encoding='utf-8') as f:
            summary = json.load(f)
        print(f"📊 Summary: {summary.get('total_categories', 0)} categories processed")
    else:
        print("❌ Image generation summary not found")
        all_valid = False

    return all_valid

def main():
    """Run all validations."""
    print("🚀 Starting pipeline validation...\n")

    results = {
        "extraction_definitions": validate_extraction_definitions(),
        "compiled_data": validate_compiled_data(),
        "essays": validate_essays(),
        "images": validate_images()
    }

    print("\n" + "="*50)
    print("📋 VALIDATION SUMMARY")
    print("="*50)

    all_passed = True
    for test, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test.replace('_', ' ').title()}: {status}")
        if not passed:
            all_passed = False

    print("\n" + "="*50)
    if all_passed:
        print("🎉 ALL VALIDATIONS PASSED!")
        print("Your extraction pipeline is working correctly with:")
        print("✅ Proper category definitions (Principles, Policies, Values, Goals)")
        print("✅ Source attribution in compiled data")
        print("✅ Source citations and quotes in essays")
        print("✅ Successful image generation")
    else:
        print("⚠️  SOME VALIDATIONS FAILED!")
        print("Please check the errors above and fix them.")

    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
