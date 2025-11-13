"""
Main converter: Orchestrates paper to presentation conversion.
"""

from .planning import phase1_plan_presentation
from .generator import phase2_generate_all_slides
from .renderer import render_slides_to_markdown
from .utils import build_figure_id_to_url_map


async def convert_paper_to_presentation(
    paper_data: dict,
    output_file: str = "paper_presentation.md",
    max_slides: int = 10,
    target_language: str = "ko",
) -> str:
    """
    Convert paper to presentation using 2-phase generation.

    Args:
        paper_data: Paper JSON data
        output_file: Output markdown file path
        max_slides: Maximum number of slides
        target_language: Target language code (ko, en, ja, zh, es, fr, de)

    Returns:
        Generated markdown content
    """
    # Build figure_id to URL mapping
    if "sections" in paper_data:
        sections = paper_data.get("sections", {})
    else:
        sections = paper_data
    figure_map = build_figure_id_to_url_map(sections)
    print(f"\n📸 Built figure map: {len(figure_map)} figures")
    for fig_id, url in figure_map.items():
        print(f"   {fig_id} → {url[:80]}...")

    # Phase 1: Plan presentation structure
    plan = phase1_plan_presentation(paper_data, max_slides, target_language)

    # Phase 2: Generate slides asynchronously
    slides = await phase2_generate_all_slides(plan, paper_data, target_language)

    # Render to Markdown (with figure_map for ID to URL conversion)
    markdown = render_slides_to_markdown(slides, output_file, figure_map)

    return markdown
