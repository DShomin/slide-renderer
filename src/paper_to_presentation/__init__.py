"""
Paper to Presentation Generator

2-Phase generation system using Solar Pro2 LLM + slide-renderer.

Usage:
    import asyncio
    from paper_to_presentation import convert_paper_to_presentation

    # Load paper JSON
    with open("paper.json") as f:
        paper_data = json.load(f)

    # Convert to presentation
    markdown = asyncio.run(convert_paper_to_presentation(
        paper_data,
        output_file="presentation.md",
        max_slides=10,
        target_language="ko"  # or "en", "ja", "zh", "es", "fr", "de"
    ))
"""

from .converter import convert_paper_to_presentation
from .models import (
    SlideType,
    PresentationPlan,
    SlideOutline,
    SLIDE_TYPE_MODELS,
)

__all__ = [
    "convert_paper_to_presentation",
    "SlideType",
    "PresentationPlan",
    "SlideOutline",
    "SLIDE_TYPE_MODELS",
]

__version__ = "2.0.0"
