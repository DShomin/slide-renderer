"""
Phase 2: Async slide generation with validation retry.
"""

import asyncio
import json
import os
from typing import List
from openai import AsyncOpenAI

from .models import PresentationPlan, SlideOutline, SLIDE_TYPE_MODELS
from .utils import extract_paper_section_text, extract_figures_from_sections


async def phase2_generate_slide(
    client: AsyncOpenAI,
    slide_outline: SlideOutline,
    paper_data: dict,
    target_language: str = "ko",
    max_retries: int = 2
) -> dict:
    """
    Phase 2: Generate a single slide based on outline with retry on validation failure.

    Args:
        client: AsyncOpenAI client
        slide_outline: Slide outline from Phase 1
        paper_data: Full paper data for context
        target_language: Target language code
        max_retries: Maximum number of retry attempts (default: 2)

    Returns:
        Generated slide content as dict (or None if all attempts failed)
    """
    slide_type = slide_outline.type
    content_model = SLIDE_TYPE_MODELS[slide_type]

    # Build context from paper
    # Try both formats: {title, sections: {...}} or {abstract, method, ...}
    if "sections" in paper_data:
        title = paper_data.get("title", "")
        sections = paper_data.get("sections", {})
    else:
        # Flat structure: sections at top level
        title = "Attention Is All You Need"
        sections = paper_data

    # Extract text from nested structure
    abstract = extract_paper_section_text(sections.get("abstract", ""), max_chars=500)
    method = extract_paper_section_text(sections.get("method", ""), max_chars=400)
    performance = extract_paper_section_text(sections.get("performance", ""), max_chars=400)
    conclusion = extract_paper_section_text(sections.get("conclusion", ""), max_chars=300)

    # Extract figures with URLs and captions
    all_figures = extract_figures_from_sections(sections)
    figures_info = ""
    if all_figures:
        figures_info = "\n\n**Available Figures** (Select by Figure ID):\n"
        for i, fig in enumerate(all_figures[:5], 1):
            figures_info += f"{i}. Figure ID: {fig['figure_id']}\n   Caption: {fig['caption']}\n\n"
        figures_info += "\n**IMPORTANT**: For image URLs, use the Figure ID (e.g., 'S3.F1'), NOT the actual URL. The system will convert it to the real URL automatically."

    # Language names
    lang_names = {
        "ko": "한국어", "en": "English", "ja": "日本語",
        "zh": "中文", "es": "Español", "fr": "Français", "de": "Deutsch"
    }
    lang_name = lang_names.get(target_language, target_language)

    # Get JSON schema
    schema_info = content_model.model_json_schema()

    prompt = f"""Generate slide content following the plan.

**Slide Plan**:
- Number: {slide_outline.slide_number}
- Type: {slide_type.value}
- Purpose: {slide_outline.purpose}
- Key Points: {slide_outline.key_points}

**Paper Context**:
- Title: {title}
- Abstract: {abstract}
- Method: {method}
- Performance: {performance}
- Conclusion: {conclusion}{figures_info}

**Instructions**:
- Generate content in {lang_name}
- Follow the exact schema for {slide_type.value}
- Include the specific key points mentioned in the plan
- CRITICAL: Keep within ALL character limits:
  * highlight.content: MAX 200 chars
  * quote.quote: MAX 200 chars
  * All titles: Check schema limits
  * All descriptions: MAX 300 chars
- **CRITICAL - Image URLs** (for image-based slides):
  * Use Figure IDs from "Available Figures" list (e.g., 'S3.F1')
  * Match figure to slide content using caption
  * Use caption text to write image descriptions
  * DO NOT create URLs or fake Figure IDs
  * Example: If caption matches, use 'S3.F1' as the URL field value
  * System will automatically convert Figure ID to real URL during rendering
  * If this slide type requires images but no suitable figures exist, report error
- Output valid JSON matching the schema

**Schema**: {json.dumps(schema_info, ensure_ascii=False)}

Generate the slide as JSON now.
"""

    validation_feedback = None
    last_error = None

    for attempt in range(max_retries + 1):
        try:
            # Build messages with validation feedback if this is a retry
            messages = [
                {"role": "system", "content": f"Generate a {slide_type.value} slide in {lang_name}. Output valid JSON only. Respect ALL character limits. For images, use Figure IDs (e.g., 'S3.F1') from Available Figures list - do NOT create fake IDs."}
            ]

            if validation_feedback and attempt > 0:
                # Add feedback from previous validation failure
                retry_prompt = f"""{prompt}

**VALIDATION FEEDBACK FROM PREVIOUS ATTEMPT**:
The previous generation failed validation with the following error:
{validation_feedback}

**CRITICAL**: Fix the above validation errors. Pay special attention to:
- Character limits (must be STRICTLY followed)
- List length constraints (min/max items)
- Required fields (all must be present)
- Field types (strings, numbers, lists)

Regenerate the slide with ALL validation errors fixed.
"""
                messages.append({"role": "user", "content": retry_prompt})
            else:
                messages.append({"role": "user", "content": prompt})

            response = await client.chat.completions.create(
                model="solar-pro2-250909",
                messages=messages,
                reasoning_effort="high",
                response_format={"type": "json_object"},
                temperature=0.05,
            )

            # Parse JSON and validate with Pydantic
            slide_data = json.loads(response.choices[0].message.content)
            slide_content = content_model(**slide_data)

            # Success!
            if attempt > 0:
                print(f"   ✅ Slide {slide_outline.slide_number:2d} [{slide_type.value:20s}] generated (retry {attempt})")
            else:
                print(f"   ✅ Slide {slide_outline.slide_number:2d} [{slide_type.value:20s}] generated")

            return slide_content.model_dump()

        except Exception as e:
            last_error = e
            validation_feedback = str(e)

            if attempt < max_retries:
                # Will retry
                print(f"   ⚠️  Slide {slide_outline.slide_number:2d} [{slide_type.value:20s}] validation failed (attempt {attempt + 1}/{max_retries + 1}), retrying...")
            else:
                # Final attempt failed
                print(f"   ❌ Slide {slide_outline.slide_number:2d} [{slide_type.value:20s}] failed after {max_retries + 1} attempts: {str(e)[:100]}")
                # Return None for failed slides
                return None


async def phase2_generate_all_slides(
    plan: PresentationPlan,
    paper_data: dict,
    target_language: str = "ko"
) -> List[dict]:
    """
    Phase 2: Generate all slides asynchronously.

    Args:
        plan: Presentation plan from Phase 1
        paper_data: Full paper data
        target_language: Target language code

    Returns:
        List of generated slide contents (excluding failed slides)
    """
    api_key = os.getenv("UPSTAGE_API_KEY")
    if not api_key:
        raise ValueError("UPSTAGE_API_KEY not found in environment variables")

    client = AsyncOpenAI(api_key=api_key, base_url="https://api.upstage.ai/v1/solar")

    print("\n" + "=" * 70)
    print("PHASE 2: GENERATING SLIDES ASYNCHRONOUSLY")
    print("=" * 70)
    print(f"🚀 Generating {len(plan.slides)} slides in parallel...")

    # Create async tasks for all slides
    tasks = [
        phase2_generate_slide(client, slide_outline, paper_data, target_language)
        for slide_outline in plan.slides
    ]

    # Execute all tasks concurrently
    slides = await asyncio.gather(*tasks, return_exceptions=True)

    # Filter out failed slides (None or exceptions)
    successful_slides = []
    for i, slide in enumerate(slides, 1):
        if isinstance(slide, Exception):
            print(f"   ⚠️  Slide {i} exception: {str(slide)[:60]}")
        elif slide is None:
            print(f"   ⚠️  Slide {i} returned None")
        else:
            successful_slides.append(slide)

    print(f"\n✅ Generated {len(successful_slides)}/{len(plan.slides)} slides successfully")

    return successful_slides
