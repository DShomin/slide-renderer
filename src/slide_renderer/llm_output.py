"""
LLM Structured Output Integration for SlideTypeEnum

This module provides utilities to export SlideTypeEnum for use with
LLM structured output APIs:
- OpenAI Function Calling / JSON Mode
- Anthropic Claude Tool Use
- Pydantic BaseModel schemas
- Generic JSON Schema
"""

import json
from typing import Literal

from slide_renderer.types import SlideTypeEnum

# ============================================================================
# ENUM VALUES - For LLM Structured Output
# ============================================================================

# Get all enum values as list
SLIDE_TYPE_VALUES = [t.value for t in SlideTypeEnum]

# Create Literal type for type hints
SlideTypeLiteral = Literal[
    "title_slide",
    "section_title",
    "single_content_with_image",
    "highlight",
    "two_column_list",
    "two_columns_with_grid",
    "vertical_list",
    "horizontal_3_column_list",
    "horizontal_4_column_list",
    "image_with_description_2",
    "image_with_description_3",
    "three_column_metrics",
    "metrics_grid",
    "quote",
]


# ============================================================================
# JSON SCHEMA - For OpenAI, Anthropic, etc.
# ============================================================================


def get_slide_type_json_schema() -> dict:
    """
    Get JSON Schema for slide type enum.

    Use with:
    - OpenAI function calling
    - Anthropic tool use
    - Any LLM that accepts JSON Schema

    Returns:
        JSON Schema definition for slide type
    """
    return {
        "type": "string",
        "enum": SLIDE_TYPE_VALUES,
        "description": "Type of slide layout to use",
        "examples": ["title_slide", "metrics_grid", "vertical_list"],
    }


def get_slide_type_json_schema_with_descriptions() -> dict:
    """
    Get JSON Schema with detailed descriptions for each enum value.

    Returns:
        JSON Schema with oneOf and descriptions
    """
    one_of_schemas = []

    for slide_type in SlideTypeEnum:
        one_of_schemas.append(
            {
                "const": slide_type.value,
                "title": slide_type.name.replace("_", " ").title(),
                "description": slide_type.get_llm_description(),
                "examples": [slide_type.value],
            }
        )

    return {
        "oneOf": one_of_schemas,
        "description": "Type of slide layout to use. Choose based on content type and purpose.",
    }


# ============================================================================
# OPENAI FUNCTION CALLING
# ============================================================================


def get_openai_function_schema() -> dict:
    """
    Get OpenAI function calling schema for slide generation.

    Use with OpenAI API:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[...],
            functions=[get_openai_function_schema()],
            function_call={"name": "generate_slide"}
        )

    Returns:
        OpenAI function schema
    """
    return {
        "name": "generate_slide",
        "description": "Generate a slide with specified type and content",
        "parameters": {
            "type": "object",
            "properties": {
                "slide_type": get_slide_type_json_schema(),
                "content": {
                    "type": "object",
                    "description": "Slide content matching the requirements of the selected slide type",
                    "additionalProperties": True,
                },
            },
            "required": ["slide_type", "content"],
        },
    }


def get_openai_function_schema_with_descriptions() -> dict:
    """
    Get OpenAI function schema with detailed slide type descriptions.

    Returns:
        OpenAI function schema with rich enum descriptions
    """
    return {
        "name": "generate_slide",
        "description": "Generate a slide with specified type and content. Choose slide type based on content purpose.",
        "parameters": {
            "type": "object",
            "properties": {
                "slide_type": get_slide_type_json_schema_with_descriptions(),
                "content": {
                    "type": "object",
                    "description": "Slide content matching the requirements of the selected slide type",
                    "additionalProperties": True,
                },
            },
            "required": ["slide_type", "content"],
        },
    }


# ============================================================================
# ANTHROPIC TOOL USE
# ============================================================================


def get_anthropic_tool_schema() -> dict:
    """
    Get Anthropic Claude tool use schema.

    Use with Anthropic API:
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            messages=[...],
            tools=[get_anthropic_tool_schema()]
        )

    Returns:
        Anthropic tool schema
    """
    return {
        "name": "generate_slide",
        "description": "Generate a slide with specified type and content based on presentation requirements",
        "input_schema": {
            "type": "object",
            "properties": {
                "slide_type": get_slide_type_json_schema(),
                "content": {
                    "type": "object",
                    "description": "Slide content matching the requirements of the selected slide type",
                },
            },
            "required": ["slide_type", "content"],
        },
    }


def get_anthropic_tool_schema_with_descriptions() -> dict:
    """
    Get Anthropic tool schema with detailed descriptions.

    Returns:
        Anthropic tool schema with rich enum descriptions
    """
    return {
        "name": "generate_slide",
        "description": "Generate a slide with specified type and content. Choose appropriate slide type based on content purpose and structure.",
        "input_schema": {
            "type": "object",
            "properties": {
                "slide_type": get_slide_type_json_schema_with_descriptions(),
                "content": {
                    "type": "object",
                    "description": "Slide content matching the requirements of the selected slide type",
                },
            },
            "required": ["slide_type", "content"],
        },
    }


# ============================================================================
# PRESENTATION SCHEMA - Multiple Slides
# ============================================================================


def get_presentation_json_schema() -> dict:
    """
    Get JSON Schema for complete presentation with multiple slides.

    Returns:
        JSON Schema for presentation array
    """
    return {
        "type": "object",
        "properties": {
            "title": {"type": "string", "description": "Presentation title"},
            "slides": {
                "type": "array",
                "description": "Array of slides in the presentation",
                "items": {
                    "type": "object",
                    "properties": {
                        "slide_type": get_slide_type_json_schema(),
                        "content": {"type": "object", "description": "Slide content"},
                    },
                    "required": ["slide_type", "content"],
                },
                "minItems": 1,
            },
        },
        "required": ["title", "slides"],
    }


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================


def get_slide_type_info(slide_type_value: str) -> dict:
    """
    Get detailed information about a specific slide type.

    Args:
        slide_type_value: Enum value string (e.g., "title_slide")

    Returns:
        Dictionary with slide type information

    Raises:
        ValueError: If slide type value is invalid
    """
    try:
        slide_type = SlideTypeEnum(slide_type_value)
        return slide_type.to_llm_full_dict()
    except ValueError:
        raise ValueError(
            f"Invalid slide type: {slide_type_value}. Valid types: {SLIDE_TYPE_VALUES}"
        ) from None


def validate_slide_type(slide_type_value: str) -> bool:
    """
    Validate if a string is a valid slide type.

    Args:
        slide_type_value: String to validate

    Returns:
        True if valid, False otherwise
    """
    return slide_type_value in SLIDE_TYPE_VALUES


def get_slide_type_descriptions() -> dict[str, str]:
    """
    Get mapping of slide type values to their LLM descriptions.

    Returns:
        Dictionary mapping enum values to descriptions
    """
    return {slide_type.value: slide_type.get_llm_description() for slide_type in SlideTypeEnum}


# ============================================================================
# EXPORT FUNCTIONS
# ============================================================================


def export_for_openai(include_descriptions: bool = True, output_file: str = None) -> dict:
    """
    Export schema for OpenAI API.

    Args:
        include_descriptions: Include detailed enum descriptions
        output_file: Optional file path to save JSON

    Returns:
        OpenAI function schema
    """
    if include_descriptions:
        schema = get_openai_function_schema_with_descriptions()
    else:
        schema = get_openai_function_schema()

    if output_file:
        with open(output_file, "w") as f:
            json.dump(schema, f, indent=2)

    return schema


def export_for_anthropic(include_descriptions: bool = True, output_file: str = None) -> dict:
    """
    Export schema for Anthropic API.

    Args:
        include_descriptions: Include detailed enum descriptions
        output_file: Optional file path to save JSON

    Returns:
        Anthropic tool schema
    """
    if include_descriptions:
        schema = get_anthropic_tool_schema_with_descriptions()
    else:
        schema = get_anthropic_tool_schema()

    if output_file:
        with open(output_file, "w") as f:
            json.dump(schema, f, indent=2)

    return schema


def export_enum_values(output_file: str = None) -> list[str]:
    """
    Export just the enum values.

    Args:
        output_file: Optional file path to save JSON

    Returns:
        List of enum value strings
    """
    if output_file:
        with open(output_file, "w") as f:
            json.dump(SLIDE_TYPE_VALUES, f, indent=2)

    return SLIDE_TYPE_VALUES


# ============================================================================
# EXAMPLE USAGE
# ============================================================================


def print_examples():
    """Print usage examples for different LLM APIs."""

    print("=" * 70)
    print("LLM STRUCTURED OUTPUT - USAGE EXAMPLES")
    print("=" * 70)

    # Example 1: Simple enum values
    print("\n1. SIMPLE ENUM VALUES")
    print("-" * 70)
    print("from llm_structured_output import SLIDE_TYPE_VALUES")
    print(f"\nValues: {SLIDE_TYPE_VALUES[:3]} ... (14 total)")

    # Example 2: OpenAI
    print("\n\n2. OPENAI FUNCTION CALLING")
    print("-" * 70)
    print("from llm_structured_output import get_openai_function_schema")
    print("\nschema = get_openai_function_schema()")
    print("\nUsage with OpenAI API:")
    print("""
response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "user", "content": "Create a title slide for AI presentation"}
    ],
    functions=[get_openai_function_schema()],
    function_call={"name": "generate_slide"}
)
    """)

    # Example 3: Anthropic
    print("\n3. ANTHROPIC TOOL USE")
    print("-" * 70)
    print("from llm_structured_output import get_anthropic_tool_schema")
    print("\nschema = get_anthropic_tool_schema()")
    print("\nUsage with Anthropic API:")
    print("""
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    messages=[
        {"role": "user", "content": "Create a title slide for AI presentation"}
    ],
    tools=[get_anthropic_tool_schema()]
)
    """)

    # Example 4: JSON Schema
    print("\n4. GENERIC JSON SCHEMA")
    print("-" * 70)
    print("from llm_structured_output import get_slide_type_json_schema")
    print("\nschema = get_slide_type_json_schema()")
    print(json.dumps(get_slide_type_json_schema(), indent=2))

    # Example 5: Validation
    print("\n\n5. VALIDATION")
    print("-" * 70)
    print("from llm_structured_output import validate_slide_type")
    print("\nvalidate_slide_type('title_slide')  # True")
    print("validate_slide_type('invalid_type')  # False")

    # Example 6: Type Info
    print("\n\n6. GET SLIDE TYPE INFO")
    print("-" * 70)
    print("from llm_structured_output import get_slide_type_info")
    print("\ninfo = get_slide_type_info('metrics_grid')")
    print(json.dumps(get_slide_type_info("metrics_grid"), indent=2)[:300])
    print("...")

    print("\n" + "=" * 70)
    print("✅ All schemas ready for LLM structured output!")
    print("=" * 70)


if __name__ == "__main__":
    print_examples()

    # Export schemas to files
    print("\n\nExporting schemas to files...")
    export_for_openai(output_file="openai_schema.json")
    export_for_anthropic(output_file="anthropic_schema.json")
    export_enum_values(output_file="slide_type_values.json")
    print("✅ Exported:")
    print("  - openai_schema.json")
    print("  - anthropic_schema.json")
    print("  - slide_type_values.json")
