"""Slide Renderer - Render JSON slides to Marp markdown presentations.

A standalone package for converting structured slide data (JSON) into
Marp-compatible markdown presentations with Jinja2 templates.

Core Purpose:
    - Render slide JSON to Marp markdown using Jinja2 templates
    - Validate slide content with Pydantic schemas
    - Support 14 different slide layouts

Usage:
    from slide_renderer import SlideRenderer

    renderer = SlideRenderer()
    markdown = renderer.render_presentation(slides_data, validate=True)
"""

__version__ = "0.1.0"

from slide_renderer.renderer import SlideRenderer
from slide_renderer.types import SlideTypeEnum

# Content schemas
from slide_renderer.schemas import (
    SLIDE_CONTENT_MODELS,
    HighlightContent,
    Horizontal3ColumnListContent,
    Horizontal4ColumnListContent,
    ImageItem,
    ImageWithDescription2Content,
    ImageWithDescription3Content,
    ListItem,
    MetricsGridContent,
    MetricValue,
    MetricWithDescription,
    QuoteContent,
    SectionTitleContent,
    SingleContentWithImageContent,
    ThreeColumnMetricsContent,
    TitleSlideContent,
    TwoColumnListContent,
    TwoColumnsWithGridContent,
    VerticalListContent,
    get_all_schemas,
    get_content_model,
    get_json_schema,
)

__all__ = [
    # Version
    "__version__",
    # Core renderer
    "SlideRenderer",
    "SlideTypeEnum",
    # Validation schemas
    "SLIDE_CONTENT_MODELS",
    "get_content_model",
    "get_json_schema",
    "get_all_schemas",
    # Slide content models (14 types)
    "TitleSlideContent",
    "SectionTitleContent",
    "SingleContentWithImageContent",
    "HighlightContent",
    "TwoColumnListContent",
    "VerticalListContent",
    "Horizontal3ColumnListContent",
    "TwoColumnsWithGridContent",
    "Horizontal4ColumnListContent",
    "ImageWithDescription2Content",
    "ImageWithDescription3Content",
    "ThreeColumnMetricsContent",
    "MetricsGridContent",
    "QuoteContent",
    # Component models
    "ListItem",
    "ImageItem",
    "MetricValue",
    "MetricWithDescription",
]
