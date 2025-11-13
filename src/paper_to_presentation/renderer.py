"""
Markdown rendering with figure ID to URL conversion.
"""

import json
from pathlib import Path
from typing import List

from slide_renderer import SlideRenderer
from .utils import convert_figure_ids_to_urls


def render_slides_to_markdown(slides: List[dict], output_file: str, figure_map: dict = None) -> str:
    """
    Render slides to Marp markdown.

    Args:
        slides: List of slide content dicts
        output_file: Output markdown file path
        figure_map: Optional dict mapping figure_id to absolute_url

    Returns:
        Generated markdown content
    """
    print("\n" + "=" * 70)
    print("RENDERING TO MARKDOWN")
    print("=" * 70)

    # Convert Figure IDs to URLs if figure_map provided
    if figure_map:
        print(f"   Converting Figure IDs to URLs ({len(figure_map)} figures available)...")
        slides = convert_figure_ids_to_urls(slides, figure_map)

    # Convert slides to slide-renderer format
    # Format: [{"type": slide_type_string, "content": {...}}]
    slides_data = []
    for slide in slides:
        slide_type = slide.pop("type")  # Extract type (Enum)
        # Convert Enum to string value if needed
        if hasattr(slide_type, 'value'):
            slide_type = slide_type.value
        slides_data.append({
            "type": slide_type,
            "content": slide  # Rest is content
        })

    print(f"   Rendering {len(slides_data)} slides...")

    renderer = SlideRenderer()

    try:
        markdown = renderer.render_presentation(slides_data, validate=True)

        # Save to file
        output_path = Path(output_file)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(markdown)

        print(f"\n✅ Markdown generated: {output_file}")
        print(f"   File size: {len(markdown)} characters")

        return markdown

    except ValueError as e:
        print(f"\n❌ Validation error: {e}")
        print("\nGenerated slides data:")
        print(json.dumps(slides_data, indent=2, ensure_ascii=False))
        raise
