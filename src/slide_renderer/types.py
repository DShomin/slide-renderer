"""
Slide type enumeration based on actual marp_example.md slides with LLM integration.

This module defines the SlideTypeEnum class that represents all 14 slide types
found in the split slides from marp_example.md, enhanced with metadata for
LLM-driven slide generation.

Each enum value includes:
- Technical documentation for developers
- LLM-friendly descriptions for AI decision-making
- Content requirements for validation
- Use case guidance for appropriate selection

Supports two LLM usage patterns:
1. Full Generation: Type + content in one LLM call
2. Selection First: Type selection → content generation in separate calls
"""

from enum import Enum


class SlideTypeEnum(str, Enum):
    """
    Enumeration of all slide types with LLM integration metadata.

    Each type represents a specific layout pattern with:
    - Technical structure (HTML/CSS) for developers
    - LLM-friendly descriptions for AI understanding
    - Content requirements for validation
    - Use cases for appropriate selection

    Attributes:
        value: Snake_case identifier
        _description: Technical description with HTML/CSS details
        _file_reference: Source markdown file
        _css_classes: Required CSS classes
        _llm_description: Simple, non-technical description for LLM
        _use_case: When to use this slide type
        _content_requirements: Structure and validation rules
    """

    def __new__(
        cls,
        value: str,
        description: str,
        file_reference: str,
        css_classes: list[str],
        llm_description: str,
        use_case: str,
        content_requirements: dict,
    ):
        """
        Create new enum member with full metadata.

        Args:
            value: Enum value (snake_case identifier)
            description: Technical description with structure details
            file_reference: Source markdown filename
            css_classes: List of CSS class names
            llm_description: LLM-friendly simple description
            use_case: Primary use cases
            content_requirements: Dict with validation rules
        """
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj._description = description
        obj._file_reference = file_reference
        obj._css_classes = css_classes
        obj._llm_description = llm_description
        obj._use_case = use_case
        obj._content_requirements = content_requirements
        return obj

    # ========================================================================
    # BASIC SLIDES
    # ========================================================================

    TITLE_SLIDE = (
        "title_slide",
        """Title slide with main heading and subtitle.

Structure:
    # Slide Title
    ## Subtitle text

HTML: Pure markdown, no wrapper divs
CSS Classes: None (default h1/h2 styling)
Use Case: Opening slide, presentation title""",
        "a-title-slide.md",
        [],
        "Opening slide with a main title and subtitle",
        "Presentation opening, cover slide, title page, introduction",
        {
            "required_fields": ["title", "subtitle"],
            "optional_fields": [],
            "item_count": None,
            "has_images": False,
            "max_title_length": 80,
            "max_subtitle_length": 120,
            "description": "Simple two-line text slide with large heading and smaller subheading",
        },
    )

    SECTION_TITLE = (
        "section_title",
        """Section divider with centered title.

Structure:
    <!-- _class: center -->
    # Section title

HTML: Markdown with center class directive
CSS Classes: .center (via _class directive)
Use Case: Section breaks, chapter transitions""",
        "b-section-title.md",
        ["center"],
        "Centered title slide for dividing presentation sections",
        "Section breaks, chapter transitions, topic changes, agenda items",
        {
            "required_fields": ["title"],
            "optional_fields": [],
            "item_count": None,
            "has_images": False,
            "max_title_length": 60,
            "description": "Single centered title for section breaks",
        },
    )

    # ========================================================================
    # TWO-COLUMN LAYOUTS
    # ========================================================================

    SINGLE_CONTENT_WITH_IMAGE = (
        "single_content_with_image",
        """Single content block with optional image on the right.

Structure:
    <div class="two-column">
      <div class="left">
        <h1>Header</h1>
        <p>Description</p>
      </div>
      <div class="right">
        <div class="placeholder">
          <img src="..." alt="...">
        </div>
      </div>
    </div>

HTML: two-column layout with left text and right image
CSS Classes: .two-column, .left, .right, .placeholder
Use Case: Feature spotlight, product showcase""",
        "c-single-content-with-image.md",
        ["two-column", "left", "right", "placeholder"],
        "Text content on the left with a large image on the right",
        "Feature spotlight, product showcase, concept explanation with visual",
        {
            "required_fields": ["title", "description"],
            "optional_fields": ["image_url", "image_alt"],
            "item_count": None,
            "has_images": True,
            "max_title_length": 60,
            "max_description_length": 300,
            "image_count": 1,
            "description": "Single concept with explanatory text and supporting image",
        },
    )

    HIGHLIGHT = (
        "highlight",
        """Highlight slide with title on left, emphasis text on right.

Structure:
    <div class="two-column">
      <div class="left">
        <h1>Highlight</h1>
      </div>
      <div class="right">
        <p>Key message or call to action</p>
      </div>
    </div>

HTML: two-column with minimal left content
CSS Classes: .two-column, .left, .right
Use Case: Key messages, important callouts""",
        "d-highlight.md",
        ["two-column", "left", "right"],
        "Emphasized message or call-to-action with title on left",
        "Key messages, important callouts, memorable quotes, CTAs",
        {
            "required_fields": ["title", "message"],
            "optional_fields": [],
            "item_count": None,
            "has_images": False,
            "max_title_length": 40,
            "max_message_length": 200,
            "description": "Short, impactful message split between title and content",
        },
    )

    TWO_COLUMN_LIST = (
        "two_column_list",
        """Two-column layout with title on left, vertical list on right.

Structure:
    <div class="two-column">
      <div class="left">
        <h1>Simple list</h1>
      </div>
      <div class="right">
        <div class="list-vertical">
          <div class="list-item">
            <h3>Item Title</h3>
            <p>Description</p>
          </div>
          ...
        </div>
      </div>
    </div>

HTML: two-column with left title and right vertical list
CSS Classes: .two-column, .left, .right, .list-vertical, .list-item
Use Case: Bullet points, feature lists""",
        "e-two-column-list.md",
        ["two-column", "left", "right", "list-vertical", "list-item"],
        "Title on left with 2-4 list items stacked vertically on right",
        "Bullet points, feature lists, step-by-step instructions, benefits",
        {
            "required_fields": ["title", "items"],
            "optional_fields": [],
            "item_count": {"min": 2, "max": 4},
            "has_images": False,
            "max_title_length": 40,
            "item_structure": {"title": 50, "description": 150},
            "description": "Vertical list of 2-4 items with titles and descriptions",
        },
    )

    TWO_COLUMNS_WITH_GRID = (
        "two_columns_with_grid",
        """Two-column layout with title on left, 2x2 grid on right.

Structure:
    <div class="two-column">
      <div class="left">
        <h1>Two columns</h1>
      </div>
      <div class="right">
        <div class="grid-2x2">
          <div class="list-item">...</div>
          <div class="list-item">...</div>
          <div class="list-item">...</div>
          <div class="list-item">...</div>
        </div>
      </div>
    </div>

HTML: two-column with 2x2 grid on right
CSS Classes: .two-column, .left, .right, .grid-2x2, .list-item
Use Case: Four-quadrant comparisons, 2x2 matrices""",
        "h-two-columns-with-2x2-grid.md",
        ["two-column", "left", "right", "grid-2x2", "list-item"],
        "Title on left with exactly 4 items arranged in a 2x2 grid on right",
        "Four-quadrant analysis, 2x2 matrices, SWOT analysis, four key points",
        {
            "required_fields": ["title", "items"],
            "optional_fields": [],
            "item_count": {"min": 4, "max": 4},
            "has_images": False,
            "max_title_length": 40,
            "item_structure": {"title": 40, "description": 100},
            "description": "Exactly 4 items in 2x2 grid layout",
        },
    )

    # ========================================================================
    # SECTION CONTAINER LAYOUTS
    # ========================================================================

    VERTICAL_LIST = (
        "vertical_list",
        """Full-width vertical list with section title.

Structure:
    <div class="section-title-container">
      <h1 class="section-title">Simple list</h1>
      <div class="section-content">
        <div class="list-vertical">
          <div class="list-item">...</div>
          ...
        </div>
      </div>
    </div>

HTML: section-title-container with vertical list
CSS Classes: .section-title-container, .section-title, .section-content, .list-vertical
Use Case: Multiple items in vertical layout""",
        "f-vertical-list.md",
        ["section-title-container", "section-title", "section-content", "list-vertical"],
        "Full-width title with 3-6 items stacked vertically below",
        "Detailed feature lists, step-by-step processes, agenda items, multiple points",
        {
            "required_fields": ["title", "items"],
            "optional_fields": [],
            "item_count": {"min": 3, "max": 6},
            "has_images": False,
            "max_title_length": 60,
            "item_structure": {"title": 60, "description": 200},
            "description": "Vertical stack of 3-6 items with ample space for detail",
        },
    )

    HORIZONTAL_3_COLUMN_LIST = (
        "horizontal_3_column_list",
        """Three-column horizontal grid layout.

Structure:
    <div class="section-title-container">
      <h1 class="section-title">Simple list</h1>
      <div class="section-content">
        <div class="grid-3col">
          <div class="list-item">...</div>
          <div class="list-item">...</div>
          <div class="list-item">...</div>
        </div>
      </div>
    </div>

HTML: section-title-container with 3-column grid
CSS Classes: .section-title-container, .grid-3col, .list-item
Use Case: Three-way comparisons, feature trios""",
        "g-horizontal-3-column-list.md",
        ["section-title-container", "grid-3col", "list-item"],
        "Title with exactly 3 items arranged horizontally side-by-side",
        "Three-way comparisons, feature trios, pricing tiers, three options",
        {
            "required_fields": ["title", "items"],
            "optional_fields": [],
            "item_count": {"min": 3, "max": 3},
            "has_images": False,
            "max_title_length": 60,
            "item_structure": {"title": 50, "description": 150},
            "description": "Exactly 3 items in horizontal layout",
        },
    )

    HORIZONTAL_4_COLUMN_LIST = (
        "horizontal_4_column_list",
        """Four-column horizontal grid layout.

Structure:
    <div class="section-title-container">
      <h1 class="section-title">Simple list</h1>
      <div class="section-content">
        <div class="grid-4col">
          <div class="list-item">...</div>
          <div class="list-item">...</div>
          <div class="list-item">...</div>
          <div class="list-item">...</div>
        </div>
      </div>
    </div>

HTML: section-title-container with 4-column grid
CSS Classes: .section-title-container, .grid-4col, .list-item
Use Case: Four-step processes, quarterly breakdowns""",
        "i-horizontal-4-column-list.md",
        ["section-title-container", "grid-4col", "list-item"],
        "Title with exactly 4 items arranged horizontally side-by-side",
        "Four-step processes, quarterly results, four phases, four categories",
        {
            "required_fields": ["title", "items"],
            "optional_fields": [],
            "item_count": {"min": 4, "max": 4},
            "has_images": False,
            "max_title_length": 60,
            "item_structure": {"title": 40, "description": 120},
            "description": "Exactly 4 items in horizontal layout",
        },
    )

    # ========================================================================
    # IMAGE LAYOUTS
    # ========================================================================

    IMAGE_WITH_DESCRIPTION_2 = (
        "image_with_description_2",
        """Two images with corresponding text descriptions.

Structure:
    <div class="section-title-container">
      <h1 class="section-title">Image with description</h1>
      <div class="section-content">
        <div class="image-grid-2">
          <div class="placeholder-small"><img ...></div>
          <div class="placeholder-small"><img ...></div>
        </div>
        <div class="text-grid-2">
          <div class="list-item">...</div>
          <div class="list-item">...</div>
        </div>
      </div>
    </div>

HTML: 2-column image grid + 2-column text grid
CSS Classes: .section-title-container, .image-grid-2, .text-grid-2, .placeholder-small
Use Case: Before/after comparisons, dual products""",
        "j-image-with-description---2-images-text.md",
        ["section-title-container", "image-grid-2", "text-grid-2", "placeholder-small"],
        "Two images displayed side-by-side with corresponding descriptions below each",
        "Before/after comparisons, dual products, two options, A/B comparison",
        {
            "required_fields": ["title", "items"],
            "optional_fields": [],
            "item_count": {"min": 2, "max": 2},
            "has_images": True,
            "image_count": 2,
            "max_title_length": 60,
            "item_structure": {
                "title": 50,
                "description": 150,
                "image_url": "required",
                "image_alt": "required",
            },
            "description": "Exactly 2 images with matching text descriptions",
        },
    )

    IMAGE_WITH_DESCRIPTION_3 = (
        "image_with_description_3",
        """Three images with corresponding text descriptions.

Structure:
    <div class="section-title-container">
      <h1 class="section-title">Image with description</h1>
      <div class="section-content">
        <div class="image-grid-3">
          <div class="placeholder-small"><img ...></div>
          <div class="placeholder-small"><img ...></div>
          <div class="placeholder-small"><img ...></div>
        </div>
        <div class="grid-3col">
          <div class="list-item">...</div>
          <div class="list-item">...</div>
          <div class="list-item">...</div>
        </div>
      </div>
    </div>

HTML: 3-column image grid + 3-column text grid
CSS Classes: .section-title-container, .image-grid-3, .grid-3col, .placeholder-small
Use Case: Product galleries, step-by-step visuals""",
        "k-image-with-description---3-images-text.md",
        ["section-title-container", "image-grid-3", "grid-3col", "placeholder-small"],
        "Three images displayed side-by-side with corresponding descriptions below each",
        "Product galleries, step-by-step visuals, three examples, feature showcase",
        {
            "required_fields": ["title", "items"],
            "optional_fields": [],
            "item_count": {"min": 3, "max": 3},
            "has_images": True,
            "image_count": 3,
            "max_title_length": 60,
            "item_structure": {
                "title": 40,
                "description": 120,
                "image_url": "required",
                "image_alt": "required",
            },
            "description": "Exactly 3 images with matching text descriptions",
        },
    )

    # ========================================================================
    # METRICS LAYOUTS
    # ========================================================================

    THREE_COLUMN_METRICS = (
        "three_column_metrics",
        """Three-column metrics display with values and descriptions.

Structure:
    <div class="section-title-container">
      <h1 class="section-title">3 column metric</h1>
      <div class="section-content">
        <div class="grid-3col">
          <div class="metric">
            <div class="metric-value">XX%</div>
            <p>Description</p>
          </div>
          ...
        </div>
      </div>
    </div>

HTML: 3-column grid with metric components
CSS Classes: .section-title-container, .grid-3col, .metric, .metric-value
Use Case: KPI displays, statistics overview""",
        "l-3-column-metrics.md",
        ["section-title-container", "grid-3col", "metric", "metric-value"],
        "Display three key metrics side-by-side with numeric values and labels",
        "KPI dashboard, performance metrics, statistics overview, key numbers",
        {
            "required_fields": ["title", "metrics"],
            "optional_fields": [],
            "item_count": {"min": 3, "max": 3},
            "has_images": False,
            "max_title_length": 60,
            "metric_format": "percentage, number, currency, or custom",
            "metric_structure": {"value": "numeric string", "label": 60, "description": 100},
            "description": "Exactly 3 metrics with prominent numeric values",
        },
    )

    METRICS_GRID = (
        "metrics_grid",
        """Metrics dashboard with description on left, 2x2 grid on right.

Structure:
    <div class="container">
      <div class="left-col">
        <h2>Metrics</h2>
        <p>Description about the data</p>
      </div>
      <div class="right-col">
        <div class="metric-item">
          <h2>61%</h2>
          <p>Metric 1</p>
        </div>
        ...
      </div>
    </div>

HTML: container with left description and right 2x2 metrics
CSS Classes: .container, .left-col, .right-col, .metric-item
Use Case: Dashboard views, quarterly metrics""",
        "m-metrics-grid.md",
        ["container", "left-col", "right-col", "metric-item"],
        "Title and description on left with exactly 4 metrics in a 2x2 grid on right",
        "Dashboard views, quarterly metrics, four KPIs, performance summary",
        {
            "required_fields": ["title", "description", "metrics"],
            "optional_fields": [],
            "item_count": {"min": 4, "max": 4},
            "has_images": False,
            "max_title_length": 40,
            "max_description_length": 200,
            "metric_format": "percentage, number, currency, or custom",
            "metric_structure": {"value": "numeric string", "label": 50},
            "description": "Exactly 4 metrics in 2x2 grid with contextual description",
        },
    )

    # ========================================================================
    # SPECIAL SLIDES
    # ========================================================================

    QUOTE = (
        "quote",
        """Centered quote slide with attribution.

Structure:
    <!-- _class: center -->
    <div class="quote">
      <div class="avatar"></div>
      <blockquote>"Quote text"</blockquote>
      <cite>Full Name · Location</cite>
    </div>

HTML: centered quote container with avatar
CSS Classes: .center, .quote, .avatar
Use Case: Testimonials, impactful quotes""",
        "n-quote.md",
        ["center", "quote", "avatar"],
        "Centered quote with author attribution and optional avatar",
        "Testimonials, customer quotes, impactful statements, endorsements",
        {
            "required_fields": ["quote_text", "author_name"],
            "optional_fields": ["author_title", "avatar_url"],
            "item_count": None,
            "has_images": False,
            "max_quote_length": 200,
            "max_author_name_length": 60,
            "max_author_title_length": 80,
            "description": "Single impactful quote with attribution",
        },
    )

    # ========================================================================
    # GETTER METHODS - Original functionality
    # ========================================================================

    def get_description(self) -> str:
        """
        Get the technical description for developers.

        Returns:
            Full technical description with HTML/CSS details
        """
        return self._description

    def get_file_reference(self) -> str:
        """
        Get the source file reference for this slide type.

        Returns:
            Filename of the original split slide
        """
        return self._file_reference

    def get_css_classes(self) -> list[str]:
        """
        Get CSS classes for this slide type.

        Returns:
            List of CSS class names used by this slide type
        """
        return self._css_classes

    # ========================================================================
    # GETTER METHODS - New LLM metadata
    # ========================================================================

    def get_llm_description(self) -> str:
        """
        Get simple, non-technical description for LLM understanding.

        Returns:
            Plain language description suitable for LLM decision-making
        """
        return self._llm_description

    def get_use_case(self) -> str:
        """
        Get primary use cases for this slide type.

        Returns:
            Comma-separated use cases describing when to use this type
        """
        return self._use_case

    def get_content_requirements(self) -> dict:
        """
        Get content structure requirements for validation.

        Returns:
            Dictionary with validation rules:
            - required_fields: List of mandatory fields
            - optional_fields: List of optional fields
            - item_count: Dict with min/max or None
            - has_images: Boolean
            - field length limits
            - additional constraints
        """
        return self._content_requirements.copy()

    def get_category(self) -> str:
        """
        Get category for this slide type based on its primary function.

        Returns:
            Category string: 'basic', 'layout', 'content', 'metrics', or 'special'
        """
        if self in [SlideTypeEnum.TITLE_SLIDE, SlideTypeEnum.SECTION_TITLE]:
            return "basic"
        elif self in [
            SlideTypeEnum.SINGLE_CONTENT_WITH_IMAGE,
            SlideTypeEnum.HIGHLIGHT,
            SlideTypeEnum.TWO_COLUMN_LIST,
            SlideTypeEnum.TWO_COLUMNS_WITH_GRID,
        ]:
            return "layout"
        elif self in [
            SlideTypeEnum.VERTICAL_LIST,
            SlideTypeEnum.HORIZONTAL_3_COLUMN_LIST,
            SlideTypeEnum.HORIZONTAL_4_COLUMN_LIST,
            SlideTypeEnum.IMAGE_WITH_DESCRIPTION_2,
            SlideTypeEnum.IMAGE_WITH_DESCRIPTION_3,
        ]:
            return "content"
        elif self in [SlideTypeEnum.THREE_COLUMN_METRICS, SlideTypeEnum.METRICS_GRID]:
            return "metrics"
        elif self == SlideTypeEnum.QUOTE:
            return "special"
        return "unknown"

    # ========================================================================
    # LLM INTEGRATION METHODS - For AI-driven generation
    # ========================================================================

    def to_llm_selection_dict(self) -> dict:
        """
        Get minimal information for LLM type selection (Scenario 2, Step 1).

        Use this when LLM needs to select slide types first, then generate
        content separately for each selected type.

        Returns:
            Dictionary with essential selection information:
            - type: Enum value string
            - name: Human-readable name
            - description: Simple description
            - use_case: When to use this type
        """
        return {
            "type": self.value,
            "name": self.name.replace("_", " ").title(),
            "description": self._llm_description,
            "use_case": self._use_case,
        }

    def to_llm_full_dict(self) -> dict:
        """
        Get complete information for LLM full generation (Scenario 1).

        Use this when LLM generates both slide type and content in a single call.

        Returns:
            Dictionary with comprehensive information:
            - type: Enum value string
            - name: Human-readable name
            - description: Simple description
            - use_case: When to use this type
            - content_requirements: Full structure and validation rules
            - category: Slide category
        """
        return {
            "type": self.value,
            "name": self.name.replace("_", " ").title(),
            "description": self._llm_description,
            "use_case": self._use_case,
            "content_requirements": self._content_requirements.copy(),
            "category": self.get_category(),
        }

    # ========================================================================
    # CLASS METHODS - Collection operations
    # ========================================================================

    @classmethod
    def get_all_for_selection(cls) -> list[dict]:
        """
        Get all slide types with minimal info for Scenario 2 (Selection First).

        Use this to provide LLM with a list of available slide types for
        selection, before generating detailed content.

        Returns:
            List of dictionaries with selection information for all 14 types

        Example:
            >>> types = SlideTypeEnum.get_all_for_selection()
            >>> print(f"Found {len(types)} slide types")
            >>> # LLM selects: ["title_slide", "metrics_grid", "quote"]
        """
        return [slide_type.to_llm_selection_dict() for slide_type in cls]

    @classmethod
    def get_all_for_full_generation(cls) -> list[dict]:
        """
        Get all slide types with complete info for Scenario 1 (Full Generation).

        Use this when LLM needs to generate both slide types and their
        content in a single call.

        Returns:
            List of dictionaries with full information for all 14 types

        Example:
            >>> types = SlideTypeEnum.get_all_for_full_generation()
            >>> # LLM generates: [
            >>> #   {"type": "title_slide", "content": {...}},
            >>> #   {"type": "three_column_metrics", "content": {...}}
            >>> # ]
        """
        return [slide_type.to_llm_full_dict() for slide_type in cls]

    @classmethod
    def generate_selection_prompt(cls) -> str:
        """
        Generate formatted prompt text for LLM type selection (Scenario 2).

        Use this to create a human-readable prompt that lists all slide types
        with their descriptions and use cases, suitable for LLM to understand
        and select appropriate types.

        Returns:
            Formatted multi-line string with all slide type information

        Example:
            >>> prompt = SlideTypeEnum.generate_selection_prompt()
            >>> print(prompt)
            Available slide types:

            1. TITLE_SLIDE - Opening slide with a main title and subtitle
               Use case: Presentation opening, cover slide, title page
            ...
        """
        lines = ["Available slide types:", ""]
        for idx, slide_type in enumerate(cls, 1):
            lines.append(f"{idx}. {slide_type.name} ({slide_type.value})")
            lines.append(f"   Description: {slide_type._llm_description}")
            lines.append(f"   Use case: {slide_type._use_case}")
            lines.append("")
        return "\n".join(lines)

    @classmethod
    def generate_full_prompt(cls) -> str:
        """
        Generate formatted prompt text for LLM full generation (Scenario 1).

        Use this to create a comprehensive prompt that includes all slide types
        with their content requirements, suitable for LLM to generate complete
        presentations with proper structure.

        Returns:
            Formatted multi-line string with detailed type information

        Example:
            >>> prompt = SlideTypeEnum.generate_full_prompt()
            >>> print(prompt)
            Slide type specifications:

            1. TITLE_SLIDE
               Description: Opening slide with a main title and subtitle
               Requirements: title (max 80 chars), subtitle (max 120 chars)
            ...
        """
        lines = ["Slide type specifications:", ""]
        for idx, slide_type in enumerate(cls, 1):
            req = slide_type._content_requirements
            lines.append(f"{idx}. {slide_type.name} ({slide_type.value})")
            lines.append(f"   Description: {slide_type._llm_description}")
            lines.append(f"   Use case: {slide_type._use_case}")
            lines.append(f"   Category: {slide_type.get_category()}")

            # Format requirements
            lines.append("   Requirements:")
            lines.append(f"      - Required fields: {', '.join(req['required_fields'])}")
            if req.get("optional_fields"):
                lines.append(f"      - Optional fields: {', '.join(req['optional_fields'])}")
            if req.get("item_count"):
                ic = req["item_count"]
                lines.append(f"      - Item count: {ic.get('min', 0)}-{ic.get('max', 'unlimited')}")
            if req.get("has_images"):
                lines.append(f"      - Images: {req.get('image_count', 'yes')}")
            lines.append(f"      - {req['description']}")
            lines.append("")
        return "\n".join(lines)

    @classmethod
    def get_by_file(cls, filename: str) -> "SlideTypeEnum":
        """
        Find slide type by source filename.

        Args:
            filename: The slide filename (e.g., 'a-title-slide.md')

        Returns:
            Matching SlideTypeEnum value

        Raises:
            ValueError: If filename doesn't match any slide type
        """
        for slide_type in cls:
            if slide_type.get_file_reference() == filename:
                return slide_type
        raise ValueError(f"No slide type found for file: {filename}")

    @classmethod
    def get_by_category(cls, category: str) -> list["SlideTypeEnum"]:
        """
        Get all slide types in a specific category.

        Args:
            category: Category name ('basic', 'layout', 'content', 'metrics', 'special')

        Returns:
            List of slide types in the specified category

        Example:
            >>> metrics_types = SlideTypeEnum.get_by_category('metrics')
            >>> print([t.value for t in metrics_types])
            ['three_column_metrics', 'metrics_grid']
        """
        return [slide_type for slide_type in cls if slide_type.get_category() == category]


# ============================================================================
# HELPER FUNCTIONS - Smart type suggestions
# ============================================================================


def get_type_by_content(content_type: str) -> list[SlideTypeEnum]:
    """
    Suggest slide types based on content type.

    Args:
        content_type: Type of content - one of:
            - "metrics": Numeric data, KPIs, statistics
            - "images": Visual content, photos, diagrams
            - "list": Bullet points, features, steps
            - "text": Paragraphs, explanations
            - "quote": Testimonials, quotations

    Returns:
        List of suitable slide types for the content type

    Example:
        >>> types = get_type_by_content("metrics")
        >>> print([t.value for t in types])
        ['three_column_metrics', 'metrics_grid']
    """
    content_map = {
        "metrics": [SlideTypeEnum.THREE_COLUMN_METRICS, SlideTypeEnum.METRICS_GRID],
        "images": [
            SlideTypeEnum.SINGLE_CONTENT_WITH_IMAGE,
            SlideTypeEnum.IMAGE_WITH_DESCRIPTION_2,
            SlideTypeEnum.IMAGE_WITH_DESCRIPTION_3,
        ],
        "list": [
            SlideTypeEnum.TWO_COLUMN_LIST,
            SlideTypeEnum.VERTICAL_LIST,
            SlideTypeEnum.HORIZONTAL_3_COLUMN_LIST,
            SlideTypeEnum.HORIZONTAL_4_COLUMN_LIST,
            SlideTypeEnum.TWO_COLUMNS_WITH_GRID,
        ],
        "text": [
            SlideTypeEnum.SINGLE_CONTENT_WITH_IMAGE,
            SlideTypeEnum.HIGHLIGHT,
            SlideTypeEnum.TWO_COLUMN_LIST,
            SlideTypeEnum.VERTICAL_LIST,
        ],
        "quote": [SlideTypeEnum.QUOTE],
    }

    return content_map.get(content_type.lower(), [])


def get_type_by_item_count(count: int) -> list[SlideTypeEnum]:
    """
    Suggest slide types based on number of items to display.

    Args:
        count: Number of items/points to display (1-6)

    Returns:
        List of slide types that can handle this item count

    Example:
        >>> types = get_type_by_item_count(3)
        >>> print([t.value for t in types])
        ['horizontal_3_column_list', 'three_column_metrics', 'vertical_list']
    """
    suitable_types = []

    for slide_type in SlideTypeEnum:
        req = slide_type.get_content_requirements()
        item_count = req.get("item_count")

        if item_count is None:
            # No specific item count requirement
            if count == 1 and slide_type in [
                SlideTypeEnum.TITLE_SLIDE,
                SlideTypeEnum.SECTION_TITLE,
                SlideTypeEnum.SINGLE_CONTENT_WITH_IMAGE,
                SlideTypeEnum.HIGHLIGHT,
                SlideTypeEnum.QUOTE,
            ]:
                suitable_types.append(slide_type)
        else:
            # Check if count falls within min/max range
            min_count = item_count.get("min", 0)
            max_count = item_count.get("max", float("inf"))
            if min_count <= count <= max_count:
                suitable_types.append(slide_type)

    return suitable_types


# ============================================================================
# CONVENIENCE MAPPING - Quick file lookup
# ============================================================================

SLIDE_TYPE_BY_FILE = {
    "a-title-slide.md": SlideTypeEnum.TITLE_SLIDE,
    "b-section-title.md": SlideTypeEnum.SECTION_TITLE,
    "c-single-content-with-image.md": SlideTypeEnum.SINGLE_CONTENT_WITH_IMAGE,
    "d-highlight.md": SlideTypeEnum.HIGHLIGHT,
    "e-two-column-list.md": SlideTypeEnum.TWO_COLUMN_LIST,
    "f-vertical-list.md": SlideTypeEnum.VERTICAL_LIST,
    "g-horizontal-3-column-list.md": SlideTypeEnum.HORIZONTAL_3_COLUMN_LIST,
    "h-two-columns-with-2x2-grid.md": SlideTypeEnum.TWO_COLUMNS_WITH_GRID,
    "i-horizontal-4-column-list.md": SlideTypeEnum.HORIZONTAL_4_COLUMN_LIST,
    "j-image-with-description---2-images-text.md": SlideTypeEnum.IMAGE_WITH_DESCRIPTION_2,
    "k-image-with-description---3-images-text.md": SlideTypeEnum.IMAGE_WITH_DESCRIPTION_3,
    "l-3-column-metrics.md": SlideTypeEnum.THREE_COLUMN_METRICS,
    "m-metrics-grid.md": SlideTypeEnum.METRICS_GRID,
    "n-quote.md": SlideTypeEnum.QUOTE,
}
