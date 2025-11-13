"""Slide Renderer - Render JSON slides to Marp markdown presentations.

A standalone package for converting structured slide data (JSON) into
Marp-compatible markdown presentations with Jinja2 templates.
"""

__version__ = "0.1.0"

from slide_renderer.renderer import SlideRenderer
from slide_renderer.types import SlideTypeEnum

# LLM output utilities
from slide_renderer.llm_output import (
    SLIDE_TYPE_VALUES,
    SlideTypeLiteral,
    export_enum_values,
    export_for_anthropic,
    export_for_openai,
    get_anthropic_tool_schema,
    get_anthropic_tool_schema_with_descriptions,
    get_openai_function_schema,
    get_openai_function_schema_with_descriptions,
    get_presentation_json_schema,
    get_slide_type_descriptions,
    get_slide_type_info,
    get_slide_type_json_schema,
    get_slide_type_json_schema_with_descriptions,
    validate_slide_type,
)

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
    # Main renderer
    "SlideRenderer",
    # Slide types
    "SlideTypeEnum",
    # LLM output utilities
    "SLIDE_TYPE_VALUES",
    "SlideTypeLiteral",
    "get_slide_type_json_schema",
    "get_slide_type_json_schema_with_descriptions",
    "get_openai_function_schema",
    "get_openai_function_schema_with_descriptions",
    "get_anthropic_tool_schema",
    "get_anthropic_tool_schema_with_descriptions",
    "get_presentation_json_schema",
    "get_slide_type_info",
    "validate_slide_type",
    "get_slide_type_descriptions",
    "export_for_openai",
    "export_for_anthropic",
    "export_enum_values",
    # Content schemas
    "SLIDE_CONTENT_MODELS",
    "get_content_model",
    "get_json_schema",
    "get_all_schemas",
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
    "ListItem",
    "ImageItem",
    "MetricValue",
    "MetricWithDescription",
]
