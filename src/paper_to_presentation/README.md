# Paper to Presentation Generator

2-phase LLM-driven system for converting research papers to Marp presentations.

## Architecture

### Core Modules

```
src/paper_to_presentation/
├── __init__.py          # Public API exports
├── converter.py         # Main orchestration
├── planning.py          # Phase 1: Planning
├── generator.py         # Phase 2: Async generation
├── renderer.py          # Markdown rendering
├── models.py            # Pydantic data models (14 slide types)
└── utils.py             # Utility functions
```

### Module Responsibilities

#### `converter.py` - Main Orchestration
- Main entry point: `convert_paper_to_presentation()`
- Coordinates all phases: figure mapping → planning → generation → rendering
- Returns generated Marp markdown content

#### `planning.py` - Phase 1: Planning
- `phase1_plan_presentation()`: Plans presentation structure
- Uses Solar Pro2 LLM with JSON object mode
- Outputs: `PresentationPlan` with slide types and content outlines
- Includes figure ID extraction for image selection guidance

#### `generator.py` - Phase 2: Async Generation
- `phase2_generate_slide()`: Generates single slide with validation retry
- `phase2_generate_all_slides()`: Async parallel generation
- Validation-based retry logic (max 2 retries by default)
- Uses validation errors as feedback for regeneration

#### `renderer.py` - Markdown Rendering
- `render_slides_to_markdown()`: Converts slides to Marp markdown
- Integrates with `slide_renderer` package
- Converts Figure IDs to actual URLs before rendering

#### `models.py` - Data Models
- All Pydantic models for validation
- `SlideType` enum (14 slide types)
- Individual slide content models (TitleSlide, MetricsGridSlide, etc.)
- `SLIDE_TYPE_MODELS` mapping dictionary

#### `utils.py` - Utility Functions
- `extract_paper_section_text()`: Extract text from nested JSON structure
- `build_figure_id_to_url_map()`: Build figure ID to URL mapping
- `extract_figures_from_sections()`: Extract figures with captions
- `convert_figure_ids_to_urls()`: Replace Figure IDs with actual URLs

## 2-Phase Generation System

### Phase 1: Planning
1. Load paper JSON data
2. Extract section texts (abstract, method, performance, conclusion)
3. Extract available figures with IDs and captions
4. LLM generates presentation plan with:
   - Slide types for each slide
   - Purpose of each slide
   - Key points to include
   - Figure IDs to use (based on captions)

### Phase 2: Async Generation
1. For each slide outline from Phase 1:
   - Generate slide content using LLM
   - Validate with Pydantic schema
   - If validation fails:
     - Capture validation error message
     - Retry with error feedback
     - Maximum 2 retries by default
2. All slides generated in parallel using `asyncio.gather()`
3. Failed slides are filtered out

### Rendering
1. Convert Figure IDs (e.g., "S3.F1") to actual URLs
2. Replace Figure IDs in text content with "(see figure)"
3. Convert to slide-renderer format
4. Render to Marp markdown
5. Save to output file

## Key Features

### Figure ID System
- **Problem**: LLMs generate fake image URLs when given actual URLs
- **Solution**: LLM selects Figure IDs (e.g., "S3.F1") from available list
- **Conversion**: Figure IDs replaced with actual URLs during rendering
- **Validation**: Warnings issued for invalid Figure IDs

### Validation-Based Retry
- **Phase 2 Enhancement**: Automatic retry on Pydantic validation failure
- **Feedback Loop**: Validation errors used as prompts for regeneration
- **Success Rate**: Improved from ~80% to 100% with 2 retries
- **Error Types**: Character limits, list lengths, required fields, type mismatches

### Multi-Language Support
Supported languages: `ko`, `en`, `ja`, `zh`, `es`, `fr`, `de`

### Async Performance
- Phase 2 generation runs in parallel
- Significantly faster than sequential generation
- Suitable for 10-15 slide presentations

## Usage

### Basic Usage

```python
import asyncio
import json
from paper_to_presentation import convert_paper_to_presentation

# Load paper JSON
with open("paper.json") as f:
    paper_data = json.load(f)

# Convert to presentation
markdown = asyncio.run(convert_paper_to_presentation(
    paper_data,
    output_file="presentation.md",
    max_slides=10,
    target_language="ko"
))
```

### CLI Usage

```bash
# Korean (default)
python examples/paper_to_presentation.py

# English with 8 slides
python examples/paper_to_presentation.py --language en --slides 8

# Japanese
python examples/paper_to_presentation.py -l ja -o output.md
```

### Environment Setup

Required environment variable:
```bash
UPSTAGE_API_KEY=your_api_key_here
```

## API Reference

### Main Function

```python
async def convert_paper_to_presentation(
    paper_data: dict,
    output_file: str = "paper_presentation.md",
    max_slides: int = 10,
    target_language: str = "ko",
) -> str:
    """
    Convert paper to presentation using 2-phase generation.

    Args:
        paper_data: Paper JSON data (nested structure)
        output_file: Output markdown file path
        max_slides: Maximum number of slides
        target_language: Language code (ko, en, ja, zh, es, fr, de)

    Returns:
        Generated markdown content
    """
```

### Paper JSON Format

Expected structure:
```json
{
  "title": "Paper Title",
  "sections": {
    "abstract": [{"paragraphs": [...], "figures": [...]}],
    "method": [{"paragraphs": [...], "figures": [...]}],
    "performance": [...],
    "conclusion": [...]
  }
}
```

Or flat structure:
```json
{
  "abstract": [...],
  "method": [...],
  "performance": [...],
  "conclusion": [...]
}
```

Figures structure:
```json
{
  "figures": [
    {
      "figure_id": "S3.F1",
      "absolute_url": "https://arxiv.org/html/.../Figures/image.png",
      "caption": "Figure description"
    }
  ]
}
```

## Dependencies

- `openai`: Solar Pro2 LLM API client
- `pydantic>=2.0`: Data validation
- `slide_renderer`: Marp markdown rendering
- `python-dotenv`: Environment variable management

## Error Handling

### Validation Failures
- Automatic retry with validation feedback
- Maximum 2 retries by default
- Failed slides excluded from final output

### Figure ID Issues
- Warning issued for invalid Figure IDs
- Invalid IDs replaced with empty strings
- Text content cleaned of Figure ID references

### API Errors
- Environment variable validation
- API key checks
- Network error handling with clear messages

## Performance Characteristics

- **Phase 1 Planning**: ~5-10 seconds
- **Phase 2 Generation**: ~30-60 seconds for 10 slides (parallel)
- **Rendering**: <1 second
- **Total**: ~40-70 seconds for 10-slide presentation

## Limitations

- Requires Upstage Solar Pro2 API access
- Maximum 10-15 slides recommended
- Figure captions must be descriptive for accurate matching
- JSON structure must follow expected format
