"""
Phase 1: Presentation planning with LLM.
"""

import json
import os
from openai import OpenAI

from .models import PresentationPlan
from .utils import extract_paper_section_text, extract_figures_from_sections


def phase1_plan_presentation(
    paper_data: dict,
    max_slides: int = 10,
    target_language: str = "ko"
) -> PresentationPlan:
    """
    Phase 1: Plan the presentation structure.

    Args:
        paper_data: Paper JSON data
        max_slides: Maximum number of slides
        target_language: Target language code

    Returns:
        PresentationPlan with slide types and content outlines
    """
    api_key = os.getenv("UPSTAGE_API_KEY")
    if not api_key:
        raise ValueError("UPSTAGE_API_KEY not found in environment variables")

    client = OpenAI(api_key=api_key, base_url="https://api.upstage.ai/v1/solar")

    # Extract paper info
    # Try both formats: {title, sections: {...}} or {abstract, method, ...}
    if "sections" in paper_data:
        title = paper_data.get("title", "Research Paper")
        sections = paper_data.get("sections", {})
    else:
        # Flat structure: sections at top level
        title = "Attention Is All You Need"  # Default title for this paper
        sections = paper_data

    # Extract text from nested structure
    abstract = extract_paper_section_text(sections.get("abstract", ""), max_chars=800)
    method = extract_paper_section_text(sections.get("method", ""), max_chars=500)
    performance = extract_paper_section_text(sections.get("performance", ""), max_chars=500)
    conclusion = extract_paper_section_text(sections.get("conclusion", ""), max_chars=400)

    # Extract figures with URLs and captions
    all_figures = extract_figures_from_sections(sections)
    figures_info = ""
    if all_figures:
        figures_info = "\n\n**Available Figures** (Select by Figure ID):\n"
        for i, fig in enumerate(all_figures[:5], 1):  # Limit to 5 figures
            figures_info += f"{i}. Figure ID: {fig['figure_id']}\n   Caption: {fig['caption']}\n\n"
        figures_info += "\n**IMPORTANT**: For image URLs, use the Figure ID (e.g., 'S3.F1'), NOT the actual URL. The system will convert it to the real URL automatically."

    # Language names
    lang_names = {
        "ko": "한국어", "en": "English", "ja": "日本語",
        "zh": "中文", "es": "Español", "fr": "Français", "de": "Deutsch"
    }
    lang_name = lang_names.get(target_language, target_language)

    prompt = f"""You are a presentation planning expert. Analyze this paper and create a presentation plan.

**Paper Information**:
- Title: {title}
- Abstract: {abstract}
- Method: {method}
- Performance: {performance}
- Conclusion: {conclusion}{figures_info}

**Your Task**:
Create a presentation plan with {max_slides} slides maximum in {lang_name}.

**Available Slide Types (14 types)**:
1. title_slide: Opening slide with title and subtitle
2. section_title: Section divider slide (Abstract, Method, Results, Conclusion)
3. single_content_with_image: Feature spotlight with image
4. highlight: Emphasize a key point (max 200 chars content)
5. two_column_list: 2-4 items in two columns
6. vertical_list: 3-6 items with titles and descriptions
7. horizontal_3_column_list: Exactly 3 items in horizontal layout
8. two_columns_with_grid: Exactly 4 items in 2x2 grid
9. horizontal_4_column_list: Exactly 4 items in horizontal layout
10. image_with_description_2: Exactly 2 images with 2 descriptions
11. image_with_description_3: Exactly 3 images with 3 descriptions
12. three_column_metrics: Exactly 3 metrics with values and descriptions
13. metrics_grid: Exactly 4 metrics in 2x2 grid
14. quote: Quote with author (max 200 chars quote)

**Planning Guidelines**:
- Start with title_slide (paper title and authors)
- Use section_title for major sections (Abstract, Method, Results, Conclusion)
- Use highlight for key contributions (keep content under 200 chars)
- Use metrics_grid or three_column_metrics for performance results
- End with quote for takeaway message
- Distribute content evenly across slides
- **CRITICAL - Image Selection**: When planning image slides (single_content_with_image, image_with_description_2/3):
  * Use Figure IDs from the "Available Figures" list (e.g., 'S3.F1')
  * Match figures to slide content using their captions
  * DO NOT create fake Figure IDs - only use provided ones
  * If no suitable figures exist, use text-only slide types instead
  * In key_points field, specify which Figure IDs to use and why based on caption

**CRITICAL - Character Limits**:
- highlight.content: MAX 200 characters
- quote.quote: MAX 200 characters
- All descriptions: MAX 300 characters
- purpose field: MAX 200 characters
- key_points field: MAX 500 characters

**Output Format** (JSON):
{{
  "title": "Presentation title in {lang_name}",
  "total_slides": {max_slides},
  "slides": [
    {{
      "slide_number": 1,
      "type": "title_slide",
      "purpose": "Introduce paper and authors",
      "key_points": "Paper title, authors, publication year"
    }},
    {{
      "slide_number": 2,
      "type": "section_title",
      "purpose": "Abstract section",
      "key_points": "Section divider for abstract"
    }},
    {{
      "slide_number": 3,
      "type": "highlight",
      "purpose": "Highlight key contribution",
      "key_points": "Main innovation, why it matters (under 200 chars for content)"
    }},
    {{
      "slide_number": 4,
      "type": "metrics_grid",
      "purpose": "Show performance metrics",
      "key_points": "4 key metrics with values and labels"
    }},
    {{
      "slide_number": 5,
      "type": "quote",
      "purpose": "Closing takeaway",
      "key_points": "Memorable quote from paper (under 200 chars)"
    }}
  ]
}}

**CRITICAL**: Every slide MUST have ALL 4 fields: slide_number, type, purpose, key_points.

Generate the plan as JSON now. Ensure all content fits character limits.
"""

    print("=" * 70)
    print("PHASE 1: PLANNING PRESENTATION STRUCTURE")
    print("=" * 70)
    print(f"📊 Max slides: {max_slides}")
    print(f"🌐 Language: {lang_name} ({target_language})")

    try:
        response = client.chat.completions.create(
            model="solar-pro2-250909",
            messages=[
                {"role": "system", "content": "You are a presentation planning expert. Output valid JSON only."},
                {"role": "user", "content": prompt}
            ],
            reasoning_effort="high",
            response_format={"type": "json_object"},
            temperature=0.5,
        )

        # Parse JSON and validate with Pydantic
        plan_data = json.loads(response.choices[0].message.content)
        plan = PresentationPlan(**plan_data)

        print(f"\n✅ Planning Complete!")
        print(f"   Title: {plan.title}")
        print(f"   Total slides: {plan.total_slides}")
        print(f"\n📋 Slide Plan:")
        for slide_outline in plan.slides:
            print(f"   {slide_outline.slide_number}. [{slide_outline.type.value:20s}] {slide_outline.purpose[:50]}...")

        return plan

    except Exception as e:
        print(f"❌ Planning failed: {e}")
        raise
