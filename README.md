# slide-renderer

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)

**Render JSON slides to Marp markdown presentations** with Jinja2 templates. Perfect for AI-powered slide generation, programmatic presentations, and template-based workflows.

---

## Features

- **🎨 14 Slide Types**: Title, lists, metrics, quotes, images, and more
- **🤖 LLM Integration**: Built-in schemas for OpenAI, Anthropic, and other LLM APIs
- **✨ Template-Based**: Customizable Jinja2 templates for full control
- **✅ Validation**: Pydantic schemas ensure data integrity
- **📦 Zero Dependencies**: Only requires `jinja2` and `pydantic`
- **🚀 Easy to Use**: Simple API for rendering single slides or complete presentations

---

## Installation

### From GitHub

```bash
pip install git+https://github.com/your-username/slide-renderer.git
```

### For Development

```bash
git clone https://github.com/your-username/slide-renderer.git
cd slide-renderer
pip install -e .
```

---

## Quick Start

### Basic Usage

```python
from slide_renderer import SlideRenderer

# Create renderer
renderer = SlideRenderer()

# Render a single slide
markdown = renderer.render("title_slide", {
    "title": "My Presentation",
    "subtitle": "Powered by slide-renderer"
})

print(markdown)
```

### Multiple Slides

```python
slides = [
    {
        "type": "title_slide",
        "content": {"title": "Welcome", "subtitle": "Introduction"}
    },
    {
        "type": "vertical_list",
        "content": {
            "title": "Key Features",
            "items": [
                {"title": "Feature 1", "description": "Description here"},
                {"title": "Feature 2", "description": "Another description"}
            ]
        }
    },
    {
        "type": "quote",
        "content": {
            "quote": "Simplicity is the ultimate sophistication.",
            "author": "Leonardo da Vinci"
        }
    }
]

# Render complete presentation
presentation = renderer.render_presentation(slides)

# Save to file
renderer.save_presentation(slides, "output.md")
```

---

## Slide Types

slide-renderer supports **14 different slide types**:

| Slide Type | Use Case | Items |
|------------|----------|-------|
| `title_slide` | Presentation opening | - |
| `section_title` | Section breaks | - |
| `single_content_with_image` | Feature spotlight | 1 image |
| `highlight` | Key messages, CTAs | - |
| `two_column_list` | Bullet points | 2-4 |
| `vertical_list` | Detailed features | 3-6 |
| `horizontal_3_column_list` | Three-way comparison | 3 |
| `two_columns_with_grid` | 2x2 matrix | 4 |
| `horizontal_4_column_list` | Four-step process | 4 |
| `image_with_description_2` | Before/after comparison | 2 images + 2 texts |
| `image_with_description_3` | Product gallery | 3 images + 3 texts |
| `three_column_metrics` | KPI dashboard | 3 metrics |
| `metrics_grid` | Quarterly metrics | 4 metrics (2x2) |
| `quote` | Testimonials, quotes | - |

See [sample_data/README.md](sample_data/README.md) for detailed examples of each type.

---

## LLM Integration

slide-renderer provides ready-to-use schemas for AI-powered slide generation.

### OpenAI Function Calling

```python
from openai import OpenAI
from slide_renderer import get_openai_function_schema, SlideRenderer

client = OpenAI()

# Get schema
schema = get_openai_function_schema()

# Generate slide with OpenAI
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{
        "role": "user",
        "content": "Create a title slide about AI in Healthcare"
    }],
    functions=[schema],
    function_call={"name": "generate_slide"}
)

# Extract and render
import json
slide_data = json.loads(response.choices[0].message.function_call.arguments)

renderer = SlideRenderer()
markdown = renderer.render(
    slide_type=slide_data["slide_type"],
    content=slide_data["content"]
)
```

### Anthropic Claude Tool Use

```python
from anthropic import Anthropic
from slide_renderer import get_anthropic_tool_schema, SlideRenderer

client = Anthropic()

# Get schema
schema = get_anthropic_tool_schema()

# Generate slide with Claude
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    messages=[{
        "role": "user",
        "content": "Create a metrics grid showing Q4 results"
    }],
    tools=[schema]
)

# Extract and render
tool_use = response.content[0]
slide_data = tool_use.input

renderer = SlideRenderer()
markdown = renderer.render(
    slide_type=slide_data["slide_type"],
    content=slide_data["content"]
)
```

### Smart Type Selection

```python
from slide_renderer.types import get_type_by_content, get_type_by_item_count

# Find types suitable for metrics with 3 items
metrics_types = get_type_by_content("metrics")
three_item_types = get_type_by_item_count(3)
recommended = [t for t in metrics_types if t in three_item_types]

print(f"Recommended: {recommended[0].value}")
# Output: "three_column_metrics"
```

See [examples/llm_integration.py](examples/llm_integration.py) for more examples.

---

## Sample Data

The `sample_data/` directory contains JSON examples for all 14 slide types. Use these for:

- **Testing**: Verify your rendering pipeline
- **Learning**: Understand the expected JSON structure
- **Templates**: Use as starting points for your own slides

```python
import json
from pathlib import Path
from slide_renderer import SlideRenderer

# Load sample data
with open("sample_data/sample_slides.json") as f:
    samples = json.load(f)

# Render any slide type
renderer = SlideRenderer()
markdown = renderer.render("metrics_grid", samples["metrics_grid"])
```

**Note**: Sample data was extracted from real project slides to ensure authenticity and practical examples.

See [sample_data/README.md](sample_data/README.md) for details.

---

## Reference Slides

The `reference_slides/` directory contains the expected markdown output for each slide type. These serve as:

- **Validation**: Compare your output against reference implementations
- **Documentation**: See what each template produces
- **Template Development**: Use as targets when customizing templates

Mapping:

| Slide Type | Reference File |
|------------|---------------|
| `title_slide` | `a-title-slide.md` |
| `section_title` | `b-section-title.md` |
| `single_content_with_image` | `c-single-content-with-image.md` |
| ... | ... |
| `quote` | `n-quote.md` |

See [reference_slides/README.md](reference_slides/README.md) for details.

---

## Custom Templates

All templates are located in `templates/` and use Jinja2 syntax. To customize:

1. **Find the template**: `templates/{slide_type}.jinja2`
2. **Modify**: Edit the Jinja2 template
3. **Reload**: Create a new `SlideRenderer` instance

```python
from slide_renderer import SlideRenderer

# Use custom template directory
renderer = SlideRenderer(template_dir="path/to/custom/templates")
```

Template variables match the Pydantic schema fields. See `src/slide_renderer/schemas/content.py` for available fields.

---

## API Reference

### SlideRenderer

Main class for rendering slides.

```python
from slide_renderer import SlideRenderer

renderer = SlideRenderer(template_dir=None)
```

**Methods**:

- `render(slide_type, content, validate=True)` → `str`
  - Render a single slide
- `render_presentation(slides, validate=True, include_frontmatter=True)` → `str`
  - Render multiple slides into a complete presentation
- `save_presentation(slides, output_file, validate=True)`
  - Render and save to file
- `validate_content(slide_type, content)` → `BaseModel`
  - Validate content against schema

### LLM Schemas

Functions for LLM integration:

- `get_openai_function_schema()` → OpenAI function calling schema
- `get_anthropic_tool_schema()` → Anthropic tool use schema
- `get_presentation_json_schema()` → Full presentation schema
- `get_slide_type_json_schema()` → Simple enum schema

### Type Helpers

Smart slide type selection:

- `get_type_by_content(content_type)` → List of suitable types
- `get_type_by_item_count(count)` → Types that support `count` items
- `SlideTypeEnum.get_by_category(category)` → Types in category

---

## Development

### Running Tests

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/

# With coverage
pytest tests/ --cov=slide_renderer --cov-report=term-missing
```

### Code Quality

```bash
# Format code
ruff format .

# Lint
ruff check .

# Type checking
mypy src/
```

---

## Examples

See the `examples/` directory for complete examples:

- [basic_usage.py](examples/basic_usage.py) - Core functionality
- [llm_integration.py](examples/llm_integration.py) - AI-powered generation

Run examples:

```bash
python examples/basic_usage.py
python examples/llm_integration.py
```

---

## Project Structure

```
slide-renderer/
├── src/slide_renderer/
│   ├── __init__.py          # Public API
│   ├── renderer.py          # SlideRenderer class
│   ├── types.py             # SlideTypeEnum
│   ├── llm_output.py        # LLM integration utilities
│   └── schemas/
│       ├── __init__.py
│       └── content.py       # Pydantic models (14 types)
├── templates/               # 14 Jinja2 templates (.jinja2)
├── sample_data/            # Sample JSON for all types
├── reference_slides/       # Expected markdown output
├── examples/               # Usage examples
├── tests/                  # Test suite
├── pyproject.toml         # Package configuration
├── LICENSE                # MIT License
└── README.md              # This file
```

---

## Requirements

- **Python**: 3.9+
- **Dependencies**:
  - `jinja2>=3.0.0` - Template rendering
  - `pydantic>=2.0.0,<3.0.0` - Data validation

---

## License

MIT License - see [LICENSE](LICENSE) file for details.

---

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

---

## Related Projects

- [Marp](https://marp.app/) - Markdown presentation ecosystem
- [marp-cli](https://github.com/marp-team/marp-cli) - Convert Marp markdown to PDF/HTML/PPTX

---

## Support

- 📖 [Documentation](https://github.com/your-username/slide-renderer#readme)
- 🐛 [Issues](https://github.com/your-username/slide-renderer/issues)
- 💬 [Discussions](https://github.com/your-username/slide-renderer/discussions)

---

## Changelog

### v0.1.0 (2025-01-13)

- Initial release
- 14 slide types supported
- LLM integration with OpenAI and Anthropic
- Complete documentation and examples

---

**Made with ❤️ by the B-Lab Theme Contributors**
