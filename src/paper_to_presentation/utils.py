"""
Utility functions for paper content extraction and figure management.
"""

def extract_paper_section_text(section_data, max_chars: int = 1000) -> str:
    """
    Extract text from paper section data (handles nested structure).

    Paper sections can be:
    - String: Direct text
    - List[dict]: Array with header_id and paragraphs fields

    Args:
        section_data: Section content (string or list of dicts)
        max_chars: Maximum characters to extract

    Returns:
        Extracted text, limited to max_chars
    """
    if isinstance(section_data, str):
        return section_data[:max_chars]

    if isinstance(section_data, list) and len(section_data) > 0:
        # Extract paragraphs from all sections
        all_text = []
        for item in section_data:
            if isinstance(item, dict):
                paragraphs = item.get("paragraphs", [])
                if isinstance(paragraphs, list):
                    all_text.extend(paragraphs)

        # Join and limit
        combined = " ".join(all_text)
        return combined[:max_chars]

    return ""


def build_figure_id_to_url_map(sections) -> dict:
    """
    Build a mapping from figure_id to absolute_url.

    Args:
        sections: Paper sections - can be:
          - dict with section names as keys, each value is a list of subsections
          - dict directly from paper_data

    Returns:
        Dict mapping figure_id to absolute_url
    """
    figure_map = {}

    # Handle dict with section lists (e.g., {'abstract': [...], 'method': [...]})
    if isinstance(sections, dict):
        for section_name, section_list in sections.items():
            if isinstance(section_list, list):
                for subsection in section_list:
                    if isinstance(subsection, dict):
                        section_figures = subsection.get("figures", [])
                        for fig in section_figures:
                            if isinstance(fig, dict) and "figure_id" in fig and "absolute_url" in fig:
                                figure_map[fig["figure_id"]] = fig["absolute_url"]

    return figure_map


def extract_figures_from_sections(sections) -> list:
    """
    Extract all figures with URLs and captions from paper sections.

    Args:
        sections: Paper sections dict or list

    Returns:
        List of figure dicts with url, caption, figure_id
    """
    figures = []

    if isinstance(sections, dict):
        sections = sections.values()

    if isinstance(sections, list):
        for section in sections:
            if isinstance(section, list):
                # Nested list structure
                for subsection in section:
                    if isinstance(subsection, dict):
                        section_figures = subsection.get("figures", [])
                        for fig in section_figures:
                            if isinstance(fig, dict) and "absolute_url" in fig:
                                figures.append({
                                    "url": fig.get("absolute_url", ""),
                                    "caption": fig.get("caption", ""),
                                    "figure_id": fig.get("figure_id", "")
                                })
            elif isinstance(section, dict):
                # Direct dict structure
                section_figures = section.get("figures", [])
                for fig in section_figures:
                    if isinstance(fig, dict) and "absolute_url" in fig:
                        figures.append({
                            "url": fig.get("absolute_url", ""),
                            "caption": fig.get("caption", ""),
                            "figure_id": fig.get("figure_id", "")
                        })

    return figures


def convert_figure_ids_to_urls(slides: list, figure_map: dict) -> list:
    """
    Convert Figure IDs in image URLs and text content to actual URLs or remove invalid IDs.

    Args:
        slides: List of slide content dicts
        figure_map: Dict mapping figure_id to absolute_url

    Returns:
        Slides with Figure IDs replaced by actual URLs
    """
    import copy
    slides_copy = copy.deepcopy(slides)

    for slide in slides_copy:
        # Check various image field names
        # single_content_with_image uses: image_url
        if "image_url" in slide and isinstance(slide["image_url"], str):
            if slide["image_url"] in figure_map:
                slide["image_url"] = figure_map[slide["image_url"]]
            elif slide["image_url"].startswith("S") and "." in slide["image_url"]:
                # Invalid Figure ID - remove the slide or warn
                print(f"   ⚠️  Warning: Invalid Figure ID '{slide['image_url']}' not found in paper")
                slide["image_url"] = ""  # Clear invalid ID

        # Generic image field
        if "image" in slide and isinstance(slide["image"], str):
            if slide["image"] in figure_map:
                slide["image"] = figure_map[slide["image"]]
            elif slide["image"].startswith("S") and "." in slide["image"]:
                print(f"   ⚠️  Warning: Invalid Figure ID '{slide['image']}' not found in paper")
                slide["image"] = ""

        # image_with_description_2/3 use: images list with ImageItem objects
        if "images" in slide and isinstance(slide["images"], list):
            for i, img in enumerate(slide["images"]):
                if isinstance(img, dict) and "url" in img:
                    if img["url"] in figure_map:
                        slide["images"][i]["url"] = figure_map[img["url"]]
                    elif img["url"].startswith("S") and "." in img["url"]:
                        print(f"   ⚠️  Warning: Invalid Figure ID '{img['url']}' not found in paper")
                        slide["images"][i]["url"] = ""
                elif isinstance(img, str):
                    if img in figure_map:
                        slide["images"][i] = figure_map[img]
                    elif img.startswith("S") and "." in img:
                        print(f"   ⚠️  Warning: Invalid Figure ID '{img}' not found in paper")
                        slide["images"][i] = ""

        # Also convert Figure IDs in text content (description, title, content fields)
        for field in ["description", "title", "content", "subtitle"]:
            if field in slide and isinstance(slide[field], str):
                # Find all Figure ID patterns (e.g., "S3.F1", "Figure S3.F2")
                for fig_id in figure_map.keys():
                    if fig_id in slide[field]:
                        # Replace with something more readable (not URL in text)
                        slide[field] = slide[field].replace(fig_id, "(see figure)")
                        slide[field] = slide[field].replace(f"Figure {fig_id}", "(see figure)")

        # Check items list (for list-based slides)
        if "items" in slide and isinstance(slide["items"], list):
            for item in slide["items"]:
                if isinstance(item, dict):
                    for field in ["description", "title"]:
                        if field in item and isinstance(item[field], str):
                            for fig_id in figure_map.keys():
                                if fig_id in item[field]:
                                    item[field] = item[field].replace(fig_id, "(see figure)")
                                    item[field] = item[field].replace(f"Figure {fig_id}", "(see figure)")

    return slides_copy
