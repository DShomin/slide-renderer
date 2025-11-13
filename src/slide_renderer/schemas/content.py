"""
Pydantic schemas for slide content - for LLM structured output.

These models define the data structure that LLMs should generate
to fill in the Jinja2 templates. Each schema corresponds to one
slide type template.

Usage with LLM APIs:
- OpenAI: Use model_json_schema() with function calling
- Anthropic: Use model_json_schema() with tool use
- Others: Export schema and use with structured output
"""

from pydantic import BaseModel, Field

# ============================================================================
# SHARED COMPONENT MODELS
# ============================================================================


class ListItem(BaseModel):
    """List item with title and description."""

    title: str = Field(..., max_length=100, description="Item title")
    description: str = Field(..., max_length=300, description="Item description")


class ImageItem(BaseModel):
    """Image with URL and alt text."""

    url: str = Field(..., description="Image URL (can be relative or absolute)")
    alt: str = Field(..., max_length=100, description="Image alt text for accessibility")


class MetricValue(BaseModel):
    """Metric with value and label (for metrics grid)."""

    value: str = Field(..., max_length=20, description="Metric value (e.g., '61%', '$2.5M')")
    label: str = Field(..., max_length=50, description="Metric label")


class MetricWithDescription(BaseModel):
    """Metric with value and description (for 3-column metrics)."""

    value: str = Field(..., max_length=20, description="Metric value (e.g., 'XX%', '1.2K')")
    description: str = Field(..., max_length=150, description="Metric description")


# ============================================================================
# SLIDE CONTENT MODELS - One per slide type
# ============================================================================


class TitleSlideContent(BaseModel):
    """
    Content for title slide (a-title-slide).

    Use case: Presentation opening, cover slide, title page
    """

    title: str = Field(..., max_length=80, description="Main presentation title")
    subtitle: str = Field(..., max_length=120, description="Subtitle or tagline")


class SectionTitleContent(BaseModel):
    """
    Content for section title slide (b-section-title).

    Use case: Section breaks, chapter transitions
    """

    title: str = Field(..., max_length=60, description="Section title")


class SingleContentWithImageContent(BaseModel):
    """
    Content for single content with image slide (c-single-content-with-image).

    Use case: Feature spotlight, product showcase
    """

    title: str = Field(..., max_length=60, description="Content title")
    description: str = Field(..., max_length=300, description="Content description")
    image_url: str = Field(..., description="Image URL")
    image_alt: str = Field(..., max_length=100, description="Image alt text")


class HighlightContent(BaseModel):
    """
    Content for highlight slide (d-highlight).

    Use case: Key messages, important callouts, CTAs
    """

    title: str = Field(..., max_length=40, description="Highlight title")
    content: str = Field(..., max_length=200, description="Highlight message or call-to-action")


class TwoColumnListContent(BaseModel):
    """
    Content for two column list slide (e-two-column-list).

    Use case: Bullet points, feature lists, 2-4 items
    """

    title: str = Field(..., max_length=40, description="List title")
    items: list[ListItem] = Field(..., min_length=2, max_length=4, description="2-4 list items")


class VerticalListContent(BaseModel):
    """
    Content for vertical list slide (f-vertical-list).

    Use case: Detailed feature lists, 3-6 items with more space
    """

    title: str = Field(..., max_length=60, description="List title")
    items: list[ListItem] = Field(..., min_length=3, max_length=6, description="3-6 list items")


class Horizontal3ColumnListContent(BaseModel):
    """
    Content for horizontal 3 column list slide (g-horizontal-3-column-list).

    Use case: Three-way comparisons, feature trios, exactly 3 items
    """

    title: str = Field(..., max_length=60, description="List title")
    items: list[ListItem] = Field(..., min_length=3, max_length=3, description="Exactly 3 items")


class TwoColumnsWithGridContent(BaseModel):
    """
    Content for two columns with 2x2 grid slide (h-two-columns-with-2x2-grid).

    Use case: Four-quadrant analysis, 2x2 matrices, exactly 4 items
    """

    title: str = Field(..., max_length=40, description="Grid title")
    items: list[ListItem] = Field(
        ..., min_length=4, max_length=4, description="Exactly 4 items for 2x2 grid"
    )


class Horizontal4ColumnListContent(BaseModel):
    """
    Content for horizontal 4 column list slide (i-horizontal-4-column-list).

    Use case: Four-step processes, quarterly results, exactly 4 items
    """

    title: str = Field(..., max_length=60, description="List title")
    items: list[ListItem] = Field(..., min_length=4, max_length=4, description="Exactly 4 items")


class ImageWithDescription2Content(BaseModel):
    """
    Content for image with description slide - 2 images (j-image-with-description---2-images-text).

    Use case: Before/after comparisons, dual products, exactly 2 images + 2 descriptions
    """

    title: str = Field(..., max_length=60, description="Slide title")
    images: list[ImageItem] = Field(..., min_length=2, max_length=2, description="Exactly 2 images")
    items: list[ListItem] = Field(
        ..., min_length=2, max_length=2, description="Exactly 2 text descriptions matching images"
    )


class ImageWithDescription3Content(BaseModel):
    """
    Content for image with description slide - 3 images (k-image-with-description---3-images-text).

    Use case: Product galleries, step-by-step visuals, exactly 3 images + 3 descriptions
    """

    title: str = Field(..., max_length=60, description="Slide title")
    images: list[ImageItem] = Field(..., min_length=3, max_length=3, description="Exactly 3 images")
    items: list[ListItem] = Field(
        ..., min_length=3, max_length=3, description="Exactly 3 text descriptions matching images"
    )


class ThreeColumnMetricsContent(BaseModel):
    """
    Content for 3 column metrics slide (l-3-column-metrics).

    Use case: KPI dashboard, statistics overview, exactly 3 metrics
    """

    title: str = Field(..., max_length=60, description="Metrics title")
    metrics: list[MetricWithDescription] = Field(
        ..., min_length=3, max_length=3, description="Exactly 3 metrics"
    )


class MetricsGridContent(BaseModel):
    """
    Content for metrics grid slide (m-metrics-grid).

    Use case: Dashboard views, quarterly metrics, exactly 4 metrics in 2x2 grid
    """

    title: str = Field(..., max_length=40, description="Metrics title")
    description: str = Field(..., max_length=200, description="Description about the metrics")
    metrics: list[MetricValue] = Field(
        ..., min_length=4, max_length=4, description="Exactly 4 metrics for 2x2 grid"
    )


class QuoteContent(BaseModel):
    """
    Content for quote slide (n-quote).

    Use case: Testimonials, customer quotes, impactful statements
    """

    quote: str = Field(..., max_length=200, description="Quote text (without quotes)")
    author: str = Field(
        ...,
        max_length=80,
        description="Author name and optional location (e.g., 'Full Name · Location')",
    )


# ============================================================================
# MAPPING: Slide type value → Content model
# ============================================================================

SLIDE_CONTENT_MODELS = {
    "title_slide": TitleSlideContent,
    "section_title": SectionTitleContent,
    "single_content_with_image": SingleContentWithImageContent,
    "highlight": HighlightContent,
    "two_column_list": TwoColumnListContent,
    "vertical_list": VerticalListContent,
    "horizontal_3_column_list": Horizontal3ColumnListContent,
    "two_columns_with_grid": TwoColumnsWithGridContent,
    "horizontal_4_column_list": Horizontal4ColumnListContent,
    "image_with_description_2": ImageWithDescription2Content,
    "image_with_description_3": ImageWithDescription3Content,
    "three_column_metrics": ThreeColumnMetricsContent,
    "metrics_grid": MetricsGridContent,
    "quote": QuoteContent,
}


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================


def get_content_model(slide_type: str) -> type[BaseModel]:
    """
    Get Pydantic model for a slide type.

    Args:
        slide_type: Slide type value (e.g., "title_slide")

    Returns:
        Pydantic model class

    Raises:
        ValueError: If slide type is invalid
    """
    if slide_type not in SLIDE_CONTENT_MODELS:
        raise ValueError(
            f"Invalid slide type: {slide_type}. Valid types: {list(SLIDE_CONTENT_MODELS.keys())}"
        )
    return SLIDE_CONTENT_MODELS[slide_type]


def get_json_schema(slide_type: str) -> dict:
    """
    Get JSON schema for a slide type.

    Args:
        slide_type: Slide type value (e.g., "title_slide")

    Returns:
        JSON Schema dictionary
    """
    model = get_content_model(slide_type)
    return model.model_json_schema()


def get_all_schemas() -> dict[str, dict]:
    """
    Get JSON schemas for all slide types.

    Returns:
        Dictionary mapping slide type to JSON schema
    """
    return {
        slide_type: model.model_json_schema() for slide_type, model in SLIDE_CONTENT_MODELS.items()
    }


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    import json

    print("=" * 70)
    print("SLIDE CONTENT SCHEMAS - FOR LLM STRUCTURED OUTPUT")
    print("=" * 70)

    # Example 1: Get schema for a specific slide type
    print("\n1. Get schema for 'metrics_grid':")
    print("-" * 70)
    schema = get_json_schema("metrics_grid")
    print(json.dumps(schema, indent=2)[:500])
    print("...\n")

    # Example 2: Validate data
    print("\n2. Validate sample data:")
    print("-" * 70)
    sample_data = {
        "title": "Metrics",
        "description": "Description about the data beside. Lorem ipsum dolor sit amet.",
        "metrics": [
            {"value": "61%", "label": "Metric 1"},
            {"value": "56%", "label": "Metric 2"},
            {"value": "55%", "label": "Metric 3"},
            {"value": "48%", "label": "Metric 4"},
        ],
    }

    try:
        validated = MetricsGridContent(**sample_data)
        print("✅ Valid data:")
        print(validated.model_dump_json(indent=2))
    except Exception as e:
        print(f"❌ Validation error: {e}")

    # Example 3: List all available schemas
    print("\n\n3. Available slide content schemas:")
    print("-" * 70)
    for slide_type, model in SLIDE_CONTENT_MODELS.items():
        print(f"{slide_type:30} → {model.__name__}")

    # Example 4: Export all schemas to file
    print("\n\n4. Exporting all schemas...")
    print("-" * 70)
    all_schemas = get_all_schemas()
    with open("../sample_data/all_schemas.json", "w") as f:
        json.dump(all_schemas, f, indent=2)
    print("✅ Exported to sample_data/all_schemas.json")
    print(f"   Total schemas: {len(all_schemas)}")
