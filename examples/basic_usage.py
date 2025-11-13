"""
Basic usage example for slide-renderer.

This script demonstrates the core functionality of rendering
JSON slide data to Marp markdown.
"""

import json
from pathlib import Path

from slide_renderer import SlideRenderer


def main():
    """Demonstrate basic slide rendering."""
    print("=" * 70)
    print("SLIDE RENDERER - BASIC USAGE EXAMPLE")
    print("=" * 70)

    # Create renderer
    renderer = SlideRenderer()

    # Example 1: Render a single title slide
    print("\n1. Rendering a single title slide:")
    print("-" * 70)

    title_content = {
        "title": "My Awesome Presentation",
        "subtitle": "Powered by slide-renderer"
    }

    markdown = renderer.render("title_slide", title_content)
    print(markdown)

    # Example 2: Render multiple slides
    print("\n\n2. Rendering a complete presentation:")
    print("-" * 70)

    slides = [
        {
            "type": "title_slide",
            "content": {
                "title": "Welcome",
                "subtitle": "Introduction to slide-renderer"
            }
        },
        {
            "type": "section_title",
            "content": {
                "title": "Features"
            }
        },
        {
            "type": "vertical_list",
            "content": {
                "title": "Key Features",
                "items": [
                    {
                        "title": "JSON to Markdown",
                        "description": "Convert structured JSON to Marp markdown"
                    },
                    {
                        "title": "14 Slide Types",
                        "description": "Support for various presentation layouts"
                    },
                    {
                        "title": "LLM Integration",
                        "description": "Built-in schemas for LLM-driven generation"
                    },
                    {
                        "title": "Template-Based",
                        "description": "Jinja2 templates for easy customization"
                    }
                ]
            }
        },
        {
            "type": "quote",
            "content": {
                "quote": "Simplicity is the ultimate sophistication.",
                "author": "Leonardo da Vinci"
            }
        }
    ]

    presentation = renderer.render_presentation(slides, validate=True)
    print(presentation[:500])
    print("...")
    print(f"\nTotal length: {len(presentation)} characters")
    print(f"Number of slides: {len(slides)}")

    # Example 3: Save to file
    print("\n\n3. Saving to file:")
    print("-" * 70)

    output_file = Path("output_presentation.md")
    renderer.save_presentation(slides, output_file)
    print(f"Saved to: {output_file}")

    # Example 4: Load from sample data
    print("\n\n4. Loading from sample data:")
    print("-" * 70)

    sample_file = Path(__file__).parent.parent / "sample_data" / "sample_slides.json"

    if sample_file.exists():
        with open(sample_file) as f:
            sample_data = json.load(f)

        # Convert to slides format
        sample_slides = [
            {"type": slide_type, "content": content}
            for slide_type, content in list(sample_data.items())[:3]
        ]

        sample_presentation = renderer.render_presentation(sample_slides)
        print(f"Rendered {len(sample_slides)} slides from sample data")
        print(f"Length: {len(sample_presentation)} characters")
    else:
        print("Sample data not found (expected during development)")

    print("\n" + "=" * 70)
    print("✅ EXAMPLES COMPLETE")
    print("=" * 70)
    print("\nNext steps:")
    print("  - Explore more slide types in sample_data/")
    print("  - Check reference_slides/ for expected output")
    print("  - Try llm_integration.py for AI-powered generation")


if __name__ == "__main__":
    main()
