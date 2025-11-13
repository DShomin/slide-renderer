"""
LLM Integration example for slide-renderer.

This script demonstrates how to use slide-renderer with LLM APIs
(OpenAI, Anthropic, etc.) for AI-powered slide generation.
"""

import json

from slide_renderer import (
    SlideRenderer,
    SlideTypeEnum,
    SLIDE_TYPE_VALUES,
    get_openai_function_schema,
    get_anthropic_tool_schema,
    get_presentation_json_schema,
)


def example_1_openai_function_calling():
    """Example: OpenAI function calling schema."""
    print("=" * 70)
    print("EXAMPLE 1: OpenAI Function Calling")
    print("=" * 70)

    # Get schema for OpenAI
    schema = get_openai_function_schema()

    print("\nSchema for OpenAI API:")
    print(json.dumps(schema, indent=2)[:500])
    print("...")

    print("\nUsage with OpenAI SDK:")
    print("""
    from openai import OpenAI
    from slide_renderer import get_openai_function_schema

    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{
            "role": "user",
            "content": "Create a title slide for AI in Healthcare presentation"
        }],
        functions=[get_openai_function_schema()],
        function_call={"name": "generate_slide"}
    )

    # Extract slide data
    slide_data = json.loads(response.choices[0].message.function_call.arguments)

    # Render with slide-renderer
    renderer = SlideRenderer()
    markdown = renderer.render(
        slide_type=slide_data["slide_type"],
        content=slide_data["content"]
    )
    """)


def example_2_anthropic_tool_use():
    """Example: Anthropic Claude tool use schema."""
    print("\n\n")
    print("=" * 70)
    print("EXAMPLE 2: Anthropic Claude Tool Use")
    print("=" * 70)

    # Get schema for Anthropic
    schema = get_anthropic_tool_schema()

    print("\nSchema for Anthropic API:")
    print(json.dumps(schema, indent=2)[:500])
    print("...")

    print("\nUsage with Anthropic SDK:")
    print("""
    from anthropic import Anthropic
    from slide_renderer import get_anthropic_tool_schema

    client = Anthropic()
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        messages=[{
            "role": "user",
            "content": "Create a metrics grid slide showing quarterly results"
        }],
        tools=[get_anthropic_tool_schema()]
    )

    # Extract slide data from tool use
    tool_use = response.content[0]
    slide_data = tool_use.input

    # Render with slide-renderer
    renderer = SlideRenderer()
    markdown = renderer.render(
        slide_type=slide_data["slide_type"],
        content=slide_data["content"]
    )
    """)


def example_3_available_slide_types():
    """Example: Explore available slide types."""
    print("\n\n")
    print("=" * 70)
    print("EXAMPLE 3: Available Slide Types")
    print("=" * 70)

    print(f"\n Total slide types: {len(SLIDE_TYPE_VALUES)}")
    print("\nSlide types:")

    for slide_type in SlideTypeEnum:
        print(f"\n  {slide_type.value}:")
        print(f"    Description: {slide_type.get_llm_description()[:60]}...")
        print(f"    Use case: {slide_type.get_use_case()[:60]}...")


def example_4_presentation_schema():
    """Example: Full presentation schema for multi-slide generation."""
    print("\n\n")
    print("=" * 70)
    print("EXAMPLE 4: Full Presentation Schema")
    print("=" * 70)

    # Get presentation schema
    schema = get_presentation_json_schema()

    print("\nPresentation schema (for generating multiple slides):")
    print(json.dumps(schema, indent=2))

    print("\nUsage example:")
    print("""
    # Prompt LLM to generate full presentation
    prompt = '''
    Create a 5-slide presentation about "Remote Work Best Practices".
    Use the following schema:
    {schema}

    Include: title slide, section title, 2 content slides, and a quote.
    '''

    # LLM returns:
    {
        "title": "Remote Work Best Practices",
        "slides": [
            {"slide_type": "title_slide", "content": {...}},
            {"slide_type": "section_title", "content": {...}},
            {"slide_type": "vertical_list", "content": {...}},
            {"slide_type": "metrics_grid", "content": {...}},
            {"slide_type": "quote", "content": {...}}
        ]
    }

    # Render all slides
    renderer = SlideRenderer()
    markdown = renderer.render_presentation(
        llm_response["slides"],
        validate=True
    )
    """)


def example_5_smart_type_selection():
    """Example: Helper functions for intelligent slide type selection."""
    print("\n\n")
    print("=" * 70)
    print("EXAMPLE 5: Smart Type Selection")
    print("=" * 70)

    from slide_renderer.types import get_type_by_content, get_type_by_item_count

    print("\nScenario: User wants to show 3 key metrics")

    # Get types suitable for metrics
    metrics_types = get_type_by_content("metrics")
    print(f"\nTypes for metrics: {[t.value for t in metrics_types]}")

    # Get types that display 3 items
    three_item_types = get_type_by_item_count(3)
    print(f"Types for 3 items: {[t.value for t in three_item_types]}")

    # Find intersection
    recommended = [t for t in metrics_types if t in three_item_types]
    print(f"\nRecommended type: {recommended[0].value if recommended else 'N/A'}")

    if recommended:
        best_type = recommended[0]
        print(f"\nSelected: {best_type.value}")
        print(f"Description: {best_type.get_llm_description()}")
        print(f"Requirements: {json.dumps(best_type.get_content_requirements(), indent=2)[:200]}...")


def main():
    """Run all examples."""
    print("\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 15 + "SLIDE-RENDERER LLM INTEGRATION" + " " * 23 + "║")
    print("║" + " " * 24 + "Examples" + " " * 36 + "║")
    print("╚" + "═" * 68 + "╝")
    print()

    example_1_openai_function_calling()
    example_2_anthropic_tool_use()
    example_3_available_slide_types()
    example_4_presentation_schema()
    example_5_smart_type_selection()

    print("\n\n")
    print("=" * 70)
    print("✅ LLM INTEGRATION EXAMPLES COMPLETE")
    print("=" * 70)
    print("\nKey Takeaways:")
    print("  - slide-renderer provides ready-to-use schemas for LLM APIs")
    print("  - Support for OpenAI function calling and Anthropic tool use")
    print("  - Helper functions for intelligent slide type selection")
    print("  - Full presentation schema for multi-slide generation")
    print("\nNext steps:")
    print("  - Integrate with your LLM API of choice")
    print("  - Use sample_data/ for testing and validation")
    print("  - Explore custom template modifications")


if __name__ == "__main__":
    main()
