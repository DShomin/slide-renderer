#!/usr/bin/env python3
"""
Render sample_slides.json to markdown.

This script converts the sample JSON data to a Marp presentation.
"""

import json
from pathlib import Path

from slide_renderer import SlideRenderer


def main():
    """Render sample slides to markdown."""
    # Load sample data
    sample_file = Path("sample_data/sample_slides.json")

    if not sample_file.exists():
        print(f"❌ Error: {sample_file} not found")
        return 1

    with open(sample_file) as f:
        data = json.load(f)

    # Convert to slides format
    slides = [{"type": k, "content": v} for k, v in data.items()]

    # Render presentation
    renderer = SlideRenderer()
    markdown = renderer.render_presentation(slides, validate=True)

    # Save to file
    output_file = Path("sample_presentation.md")
    with open(output_file, "w") as f:
        f.write(markdown)

    print(f"✅ Generated {output_file}")
    print(f"   Total slides: {len(slides)}")
    print(f"   File size: {len(markdown)} characters")

    return 0


if __name__ == "__main__":
    exit(main())
