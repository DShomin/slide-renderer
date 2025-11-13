"""
Pydantic models for paper-to-presentation generation.

Defines all slide types and content models with validation.
"""

from enum import Enum
from typing import List
from pydantic import BaseModel, Field


# ============================================================================
# SLIDE TYPE ENUM
# ============================================================================

class SlideType(str, Enum):
    """Available slide types (all 14 types from templates)."""
    title_slide = "title_slide"
    section_title = "section_title"
    single_content_with_image = "single_content_with_image"
    highlight = "highlight"
    two_column_list = "two_column_list"
    vertical_list = "vertical_list"
    horizontal_3_column_list = "horizontal_3_column_list"
    two_columns_with_grid = "two_columns_with_grid"
    horizontal_4_column_list = "horizontal_4_column_list"
    image_with_description_2 = "image_with_description_2"
    image_with_description_3 = "image_with_description_3"
    three_column_metrics = "three_column_metrics"
    metrics_grid = "metrics_grid"
    quote = "quote"


# ============================================================================
# PHASE 1: PLANNING MODELS
# ============================================================================

class SlideOutline(BaseModel):
    """Outline for a single slide (planning phase)."""
    slide_number: int = Field(description="Slide sequence number (1-based)")
    type: SlideType = Field(description="Slide type to use")
    purpose: str = Field(max_length=200, description="What this slide should communicate")
    key_points: str = Field(max_length=500, description="Key information to include")


class PresentationPlan(BaseModel):
    """Complete presentation plan (Phase 1 output)."""
    title: str = Field(max_length=100, description="Presentation title")
    total_slides: int = Field(description="Total number of slides planned")
    slides: List[SlideOutline] = Field(description="Outline for each slide")


# ============================================================================
# COMPONENT MODELS
# ============================================================================

class ListItem(BaseModel):
    """List item component."""
    title: str = Field(max_length=100)
    description: str = Field(max_length=300)


class ImageItem(BaseModel):
    """Image item component."""
    url: str = Field(max_length=500, description="Image URL or Figure ID")
    alt_text: str = Field(max_length=200, description="Alt text for accessibility")


class MetricValue(BaseModel):
    """Metric for metrics_grid (2x2 grid)."""
    value: str = Field(max_length=20)
    label: str = Field(max_length=50)


class MetricWithDescription(BaseModel):
    """Metric for three_column_metrics."""
    value: str = Field(max_length=20)
    description: str = Field(max_length=150)


# ============================================================================
# PHASE 2: INDIVIDUAL SLIDE CONTENT MODELS
# ============================================================================

class TitleSlideContent(BaseModel):
    """Title slide content."""
    type: SlideType = Field(description="Must be 'title_slide'")
    title: str = Field(max_length=80)
    subtitle: str = Field(max_length=120)


class SectionTitleContent(BaseModel):
    """Section title content."""
    type: SlideType = Field(description="Must be 'section_title'")
    title: str = Field(max_length=60)


class SingleContentWithImageContent(BaseModel):
    """Single content with image."""
    type: SlideType = Field(description="Must be 'single_content_with_image'")
    title: str = Field(max_length=60)
    description: str = Field(max_length=300)
    image_url: str = Field(max_length=500, description="Image URL or Figure ID")
    image_alt: str = Field(max_length=200)


class HighlightContent(BaseModel):
    """Highlight slide content."""
    type: SlideType = Field(description="Must be 'highlight'")
    title: str = Field(max_length=40)
    content: str = Field(max_length=200)


class TwoColumnListContent(BaseModel):
    """Two column list content."""
    type: SlideType = Field(description="Must be 'two_column_list'")
    title: str = Field(max_length=60)
    items: List[ListItem] = Field(min_length=2, max_length=4)


class VerticalListContent(BaseModel):
    """Vertical list content."""
    type: SlideType = Field(description="Must be 'vertical_list'")
    title: str = Field(max_length=60)
    items: List[ListItem] = Field(min_length=3, max_length=6)


class Horizontal3ColumnListContent(BaseModel):
    """Horizontal 3-column list content."""
    type: SlideType = Field(description="Must be 'horizontal_3_column_list'")
    title: str = Field(max_length=60)
    items: List[ListItem] = Field(min_length=3, max_length=3)


class TwoColumnsWithGridContent(BaseModel):
    """Two columns with grid (2x2) content."""
    type: SlideType = Field(description="Must be 'two_columns_with_grid'")
    title: str = Field(max_length=60)
    items: List[ListItem] = Field(min_length=4, max_length=4)


class Horizontal4ColumnListContent(BaseModel):
    """Horizontal 4-column list content."""
    type: SlideType = Field(description="Must be 'horizontal_4_column_list'")
    title: str = Field(max_length=60)
    items: List[ListItem] = Field(min_length=4, max_length=4)


class ImageWithDescription2Content(BaseModel):
    """Image with description (2 images) content."""
    type: SlideType = Field(description="Must be 'image_with_description_2'")
    title: str = Field(max_length=60)
    images: List[ImageItem] = Field(min_length=2, max_length=2)
    items: List[ListItem] = Field(min_length=2, max_length=2)


class ImageWithDescription3Content(BaseModel):
    """Image with description (3 images) content."""
    type: SlideType = Field(description="Must be 'image_with_description_3'")
    title: str = Field(max_length=60)
    images: List[ImageItem] = Field(min_length=3, max_length=3)
    items: List[ListItem] = Field(min_length=3, max_length=3)


class ThreeColumnMetricsContent(BaseModel):
    """Three column metrics content."""
    type: SlideType = Field(description="Must be 'three_column_metrics'")
    title: str = Field(max_length=60)
    metrics: List[MetricWithDescription] = Field(min_length=3, max_length=3)


class MetricsGridContent(BaseModel):
    """Metrics grid (2x2) content."""
    type: SlideType = Field(description="Must be 'metrics_grid'")
    title: str = Field(max_length=40)
    description: str = Field(max_length=200)
    metrics: List[MetricValue] = Field(min_length=4, max_length=4)


class QuoteContent(BaseModel):
    """Quote slide content."""
    type: SlideType = Field(description="Must be 'quote'")
    quote: str = Field(max_length=200)
    author: str = Field(max_length=80)


# ============================================================================
# SLIDE TYPE TO MODEL MAPPING
# ============================================================================

SLIDE_TYPE_MODELS = {
    SlideType.title_slide: TitleSlideContent,
    SlideType.section_title: SectionTitleContent,
    SlideType.single_content_with_image: SingleContentWithImageContent,
    SlideType.highlight: HighlightContent,
    SlideType.two_column_list: TwoColumnListContent,
    SlideType.vertical_list: VerticalListContent,
    SlideType.horizontal_3_column_list: Horizontal3ColumnListContent,
    SlideType.two_columns_with_grid: TwoColumnsWithGridContent,
    SlideType.horizontal_4_column_list: Horizontal4ColumnListContent,
    SlideType.image_with_description_2: ImageWithDescription2Content,
    SlideType.image_with_description_3: ImageWithDescription3Content,
    SlideType.three_column_metrics: ThreeColumnMetricsContent,
    SlideType.metrics_grid: MetricsGridContent,
    SlideType.quote: QuoteContent,
}
