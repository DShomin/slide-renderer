"""Pydantic schemas for slide content validation."""

from slide_renderer.schemas.content import (
    SLIDE_CONTENT_MODELS,
    get_all_schemas,
    get_content_model,
    get_json_schema,
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
)

__all__ = [
    # Models
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
    # Mappings and helpers
    "SLIDE_CONTENT_MODELS",
    "get_content_model",
    "get_json_schema",
    "get_all_schemas",
]
