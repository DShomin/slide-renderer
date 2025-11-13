"""
Pytest-based tests for template rendering and restoration.

Tests that Jinja2 templates + sample JSON can perfectly restore original markdowns.
"""

import json
from pathlib import Path

import pytest

from slide_renderer import SlideRenderer


# Pytest fixtures
@pytest.fixture
def renderer():
    """Create SlideRenderer instance."""
    return SlideRenderer()


@pytest.fixture
def sample_data():
    """Load sample data from JSON file."""
    # Go up from tests/ to package root
    package_root = Path(__file__).parent.parent
    sample_file = package_root / "sample_data" / "sample_slides.json"
    with open(sample_file) as f:
        return json.load(f)


@pytest.fixture
def reference_slides_dir():
    """Get reference_slides directory path."""
    # Go up from tests/ to package root
    package_root = Path(__file__).parent.parent
    return package_root / "reference_slides"


# Test data - mapping slide types to their markdown files
SLIDE_TYPE_FILES = {
    "title_slide": "a-title-slide.md",
    "section_title": "b-section-title.md",
    "single_content_with_image": "c-single-content-with-image.md",
    "highlight": "d-highlight.md",
    "two_column_list": "e-two-column-list.md",
    "vertical_list": "f-vertical-list.md",
    "horizontal_3_column_list": "g-horizontal-3-column-list.md",
    "two_columns_with_grid": "h-two-columns-with-2x2-grid.md",
    "horizontal_4_column_list": "i-horizontal-4-column-list.md",
    "image_with_description_2": "j-image-with-description---2-images-text.md",
    "image_with_description_3": "k-image-with-description---3-images-text.md",
    "three_column_metrics": "l-3-column-metrics.md",
    "metrics_grid": "m-metrics-grid.md",
    "quote": "n-quote.md",
}


def load_original_markdown(reference_slides_dir: Path, slide_type: str) -> str:
    """Load original markdown file for a slide type."""
    filename = SLIDE_TYPE_FILES[slide_type]
    filepath = reference_slides_dir / filename

    with open(filepath) as f:
        content = f.read()

    # Remove frontmatter if present
    if content.startswith("---\n"):
        parts = content.split("---\n", 2)
        if len(parts) >= 3:
            content = parts[2]

    return content.strip()


def normalize_markdown(text: str) -> str:
    """Normalize markdown for comparison."""
    # Remove trailing whitespace from each line
    lines = [line.rstrip() for line in text.split("\n")]
    # Remove leading/trailing empty lines
    while lines and not lines[0]:
        lines.pop(0)
    while lines and not lines[-1]:
        lines.pop()
    return "\n".join(lines)


def compare_markdown(original: str, rendered: str) -> tuple[bool, str]:
    """
    Compare original and rendered markdown.

    Returns:
        (match: bool, diff_message: str)
    """
    norm_original = normalize_markdown(original)
    norm_rendered = normalize_markdown(rendered)

    if norm_original == norm_rendered:
        return True, ""

    # Generate diff for debugging
    import difflib

    diff = difflib.unified_diff(
        norm_original.splitlines(keepends=True),
        norm_rendered.splitlines(keepends=True),
        fromfile="original",
        tofile="rendered",
    )
    diff_text = "".join(diff)
    return False, diff_text


# Parametrized test for all slide types
@pytest.mark.parametrize("slide_type", list(SLIDE_TYPE_FILES.keys()))
def test_template_restoration(renderer, sample_data, reference_slides_dir, slide_type):
    """Test that template + sample JSON restores original markdown."""

    # Get content for this slide type
    content = sample_data.get(slide_type)
    assert content is not None, f"No sample data for {slide_type}"

    # 1. Validate content against schema
    renderer.validate_content(slide_type, content)

    # 2. Render template
    rendered = renderer.render(slide_type, content, validate=True)

    # 3. Load original markdown
    original = load_original_markdown(reference_slides_dir, slide_type)

    # 4. Compare
    match, diff = compare_markdown(original, rendered)

    # Assert with helpful error message
    assert match, f"Rendered markdown differs from original:\n{diff}"


# Additional tests for renderer functionality
def test_renderer_initialization():
    """Test SlideRenderer can be initialized."""
    renderer = SlideRenderer()
    assert renderer is not None


def test_renderer_with_custom_template_dir(tmp_path):
    """Test SlideRenderer with custom template directory."""
    template_dir = tmp_path / "templates"
    template_dir.mkdir()

    # Create a simple test template
    (template_dir / "test_slide.jinja2").write_text("# {{ title }}")

    renderer = SlideRenderer(template_dir=template_dir)
    assert renderer is not None


def test_validation_error_for_invalid_content(renderer):
    """Test that validation catches invalid content."""
    invalid_content = {"title": "x" * 1000}  # Too long

    with pytest.raises(ValueError):
        renderer.validate_content("title_slide", invalid_content)


def test_render_with_validation_disabled(renderer, sample_data):
    """Test rendering with validation disabled."""
    content = sample_data["title_slide"]
    rendered = renderer.render("title_slide", content, validate=False)
    assert rendered
    assert "Slide Deck Title" in rendered


def test_render_multiple_slides(renderer, sample_data):
    """Test rendering multiple slides."""
    slides = [
        {"type": "title_slide", "content": sample_data["title_slide"]},
        {"type": "section_title", "content": sample_data["section_title"]},
    ]

    result = renderer.render_presentation(slides, validate=True)
    assert result
    assert "---" in result  # Slide separator
    assert "Slide Deck Title" in result
    assert "Section Title" in result


# Integration test
def test_complete_presentation_workflow(renderer, sample_data):
    """Test complete workflow: all 14 slides."""

    slides = []
    for slide_type in SLIDE_TYPE_FILES:
        content = sample_data.get(slide_type)
        if content:
            slides.append({"type": slide_type, "content": content})

    assert len(slides) == 14, "Should have all 14 slide types"

    # Render all slides
    result = renderer.render_presentation(slides, validate=True)

    # Check result
    assert result
    # Should have frontmatter + slide separators
    # Frontmatter has ---...---, then 13 separators for 14 slides
    assert "---" in result
    assert "Slide Deck Title" in result
    assert "Metrics Grid" in result
    assert all(
        slide_type in ["title_slide", "section_title"] or f"<!-- {chr(97 + i)}" in result
        for i, slide_type in enumerate(SLIDE_TYPE_FILES.keys())
        if i < 14
    )
