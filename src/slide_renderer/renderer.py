"""
Template renderer for Marp slides.

This module renders Jinja2 templates with JSON data to generate
Marp markdown slides. It validates data against Pydantic schemas
before rendering.

Usage:
    renderer = SlideRenderer()
    markdown = renderer.render("title_slide", {"title": "...", "subtitle": "..."})

Or render multiple slides:
    slides_data = [
        {"type": "title_slide", "content": {...}},
        {"type": "metrics_grid", "content": {...}}
    ]
    presentation = renderer.render_presentation(slides_data)
"""

import json
from pathlib import Path
from typing import Any, Union

from jinja2 import Environment, FileSystemLoader, Template
from pydantic import ValidationError

from slide_renderer.schemas.content import get_content_model


class SlideRenderer:
    """
    Renders Marp slides from Jinja2 templates and JSON data.

    Attributes:
        template_dir: Path to templates directory
        env: Jinja2 environment
    """

    def __init__(self, template_dir: Union[str, Path] = None):
        """
        Initialize renderer with template directory.

        Args:
            template_dir: Path to templates directory (default: ./templates/)
        """
        if template_dir is None:
            # Find templates directory - go up from src/slide_templates to package root
            package_root = Path(__file__).parent.parent.parent
            template_dir = package_root / "templates"
        else:
            template_dir = Path(template_dir)

        if not template_dir.exists():
            raise FileNotFoundError(f"Template directory not found: {template_dir}")

        self.template_dir = template_dir
        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            trim_blocks=False,
            lstrip_blocks=False,
            keep_trailing_newline=True,
        )

    def _get_template(self, slide_type: str) -> Template:
        """
        Get Jinja2 template for slide type.

        Args:
            slide_type: Slide type value (e.g., "title_slide")

        Returns:
            Jinja2 Template object

        Raises:
            ValueError: If slide type is invalid
        """
        template_file = f"{slide_type}.jinja2"
        template_path = self.template_dir / template_file

        if not template_path.exists():
            raise ValueError(
                f"Template not found for slide type: {slide_type}\nExpected file: {template_path}"
            )

        return self.env.get_template(template_file)

    def validate_content(self, slide_type: str, content: dict[str, Any]) -> Any:
        """
        Validate content data against Pydantic schema.

        Args:
            slide_type: Slide type value
            content: Content data dictionary

        Returns:
            Validated Pydantic model instance

        Raises:
            ValueError: If slide type is invalid
            ValidationError: If content doesn't match schema
        """
        model_class = get_content_model(slide_type)

        try:
            validated = model_class(**content)
            return validated
        except ValidationError as e:
            # Re-raise with additional context as ValueError
            raise ValueError(f"Validation error for slide type '{slide_type}':\n{e}") from e

    def render(self, slide_type: str, content: dict[str, Any], validate: bool = True) -> str:
        """
        Render a single slide.

        Args:
            slide_type: Slide type value (e.g., "title_slide")
            content: Content data dictionary
            validate: Whether to validate content against schema (default: True)

        Returns:
            Rendered markdown string

        Raises:
            ValueError: If slide type is invalid or template not found
            ValidationError: If validation enabled and content invalid

        Example:
            >>> renderer = SlideRenderer()
            >>> markdown = renderer.render("title_slide", {
            ...     "title": "My Presentation",
            ...     "subtitle": "An Amazing Journey"
            ... })
        """
        # Validate content if requested
        if validate:
            validated = self.validate_content(slide_type, content)
            # Use model_dump() to get dict with validated data
            content = validated.model_dump()

        # Get template and render
        template = self._get_template(slide_type)
        rendered = template.render(**content)

        return rendered

    def render_presentation(
        self, slides: list[dict[str, Any]], validate: bool = True, include_frontmatter: bool = True
    ) -> str:
        """
        Render multiple slides into a complete presentation.

        Args:
            slides: List of slide dictionaries with 'type' and 'content' keys
            validate: Whether to validate content (default: True)
            include_frontmatter: Whether to include Marp frontmatter (default: True)

        Returns:
            Complete Marp presentation markdown

        Example:
            >>> renderer = SlideRenderer()
            >>> slides = [
            ...     {"type": "title_slide", "content": {"title": "...", "subtitle": "..."}},
            ...     {"type": "metrics_grid", "content": {...}}
            ... ]
            >>> presentation = renderer.render_presentation(slides)
        """
        rendered_slides = []

        # Render each slide
        for i, slide_data in enumerate(slides):
            try:
                slide_type = slide_data.get("type")
                content = slide_data.get("content", {})

                if not slide_type:
                    raise ValueError(f"Slide {i}: Missing 'type' field")

                rendered = self.render(slide_type, content, validate=validate)
                rendered_slides.append(rendered)

            except Exception as e:
                raise ValueError(f"Error rendering slide {i} ({slide_type}): {e}") from e

        # Join slides with separators
        slides_content = "\n---\n\n".join(rendered_slides)

        # Add frontmatter if requested
        if include_frontmatter:
            frontmatter = """---
marp: true
theme: custom-style
---

"""
            return frontmatter + slides_content

        return slides_content

    def render_from_file(self, json_file: Union[str, Path], validate: bool = True) -> str:
        """
        Render presentation from JSON file.

        Args:
            json_file: Path to JSON file with slides data
            validate: Whether to validate content (default: True)

        Returns:
            Complete Marp presentation markdown

        Expected JSON format:
            [
                {"type": "title_slide", "content": {...}},
                {"type": "metrics_grid", "content": {...}}
            ]
        """
        json_path = Path(json_file)

        if not json_path.exists():
            raise FileNotFoundError(f"JSON file not found: {json_path}")

        with open(json_path) as f:
            slides = json.load(f)

        if not isinstance(slides, list):
            raise ValueError("JSON file must contain an array of slides")

        return self.render_presentation(slides, validate=validate)

    def save_presentation(
        self, slides: list[dict[str, Any]], output_file: Union[str, Path], validate: bool = True
    ):
        """
        Render and save presentation to file.

        Args:
            slides: List of slide dictionaries
            output_file: Output markdown file path
            validate: Whether to validate content (default: True)
        """
        presentation = self.render_presentation(slides, validate=validate)
        output_path = Path(output_file)

        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w") as f:
            f.write(presentation)

        print(f"✅ Presentation saved to: {output_path}")


# ============================================================================
# EXAMPLE USAGE
# ============================================================================


def main():
    """Example usage and demonstration."""

    print("=" * 70)
    print("SLIDE TEMPLATE RENDERER")
    print("=" * 70)

    renderer = SlideRenderer()

    # Example 1: Render single slide
    print("\n1. Render single slide:")
    print("-" * 70)

    title_content = {"title": "My Awesome Presentation", "subtitle": "Powered by LLM and Marp"}

    title_markdown = renderer.render("title_slide", title_content)
    print(title_markdown)

    # Example 2: Render presentation from sample data
    print("\n\n2. Render from sample data file:")
    print("-" * 70)

    # Load sample data
    sample_file = Path(__file__).parent / "sample_data" / "sample_slides.json"

    if sample_file.exists():
        with open(sample_file) as f:
            sample_data = json.load(f)

        # Convert to presentation format
        slides = [
            {"type": slide_type, "content": content}
            for slide_type, content in list(sample_data.items())[:3]  # First 3 slides
        ]

        presentation = renderer.render_presentation(slides)
        print(presentation[:500])
        print("...")
        print(f"\nTotal length: {len(presentation)} characters")

    # Example 3: Validate content
    print("\n\n3. Content validation:")
    print("-" * 70)

    # Valid content
    try:
        renderer.validate_content(
            "metrics_grid",
            {
                "title": "Metrics",
                "description": "Description about the data.",
                "metrics": [
                    {"value": "61%", "label": "Metric 1"},
                    {"value": "56%", "label": "Metric 2"},
                    {"value": "55%", "label": "Metric 3"},
                    {"value": "48%", "label": "Metric 4"},
                ],
            },
        )
        print("✅ Valid content - validation passed")
    except ValidationError as e:
        print(f"❌ Validation failed: {e}")

    # Invalid content (wrong number of metrics)
    try:
        renderer.validate_content(
            "metrics_grid",
            {
                "title": "Metrics",
                "description": "Description",
                "metrics": [
                    {"value": "61%", "label": "Metric 1"},
                    {"value": "56%", "label": "Metric 2"},  # Only 2 metrics (need 4)
                ],
            },
        )
    except ValidationError as e:
        print("✅ Validation correctly caught error:")
        print(f"   {str(e)[:100]}...")

    print("\n" + "=" * 70)
    print("✅ Template renderer ready!")
    print("=" * 70)


if __name__ == "__main__":
    main()
