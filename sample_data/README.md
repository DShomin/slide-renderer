# Sample Data

This directory contains sample JSON data for all 14 slide types supported by slide-renderer.

## Purpose

The sample data serves multiple purposes:

1. **Testing**: Validate your rendering pipeline with known-good inputs
2. **Learning**: Understand the expected JSON structure for each slide type
3. **Templates**: Use as starting points for creating your own slides
4. **Development**: Quick testing during template customization

## Origin

**These samples were extracted from real project slides** to ensure:
- Authentic, practical examples
- Realistic content lengths and structures
- Production-ready formatting
- Common use patterns

## Files

### `sample_slides.json`

Main sample file containing one example for each of the 14 slide types:

```json
{
  "title_slide": {
    "title": "Slide Deck Title",
    "subtitle": "Description or subtitle for the presentation"
  },
  "section_title": {
    "title": "Section Title"
  },
  "single_content_with_image": {
    "title": "Content Title",
    "description": "Description of the content...",
    "image_url": "https://via.placeholder.com/400",
    "image_alt": "Placeholder image"
  },
  ...
}
```

### `all_schemas.json`

Complete Pydantic JSON schemas for all slide types. Useful for:
- LLM integration
- Automated validation
- Schema documentation
- IDE autocomplete (with JSON schema plugins)

### `schemas/`

Individual JSON schema files for each slide type:
- `TitleSlideContent.json`
- `SectionTitleContent.json`
- `MetricsGridContent.json`
- ... (14 total)

## Usage Examples

### Load and Render

```python
import json
from slide_renderer import SlideRenderer

# Load sample data
with open("sample_data/sample_slides.json") as f:
    samples = json.load(f)

# Render any slide type
renderer = SlideRenderer()

# Example: Render metrics grid
markdown = renderer.render(
    "metrics_grid",
    samples["metrics_grid"]
)

print(markdown)
```

### Render All Samples

```python
import json
from slide_renderer import SlideRenderer

# Load samples
with open("sample_data/sample_slides.json") as f:
    samples = json.load(f)

# Convert to slides format
slides = [
    {"type": slide_type, "content": content}
    for slide_type, content in samples.items()
]

# Render complete presentation
renderer = SlideRenderer()
presentation = renderer.render_presentation(slides)

# Save to file
with open("all_samples.md", "w") as f:
    f.write(presentation)
```

### Use as Template

```python
import json

# Load sample as template
with open("sample_data/sample_slides.json") as f:
    samples = json.load(f)

# Modify for your needs
my_slide = samples["vertical_list"].copy()
my_slide["title"] = "My Custom Title"
my_slide["items"][0]["title"] = "My First Item"

# Render
renderer = SlideRenderer()
markdown = renderer.render("vertical_list", my_slide)
```

### Validation Testing

```python
from slide_renderer import SlideRenderer

renderer = SlideRenderer()

# Load sample
with open("sample_data/sample_slides.json") as f:
    samples = json.load(f)

# Validate all samples
for slide_type, content in samples.items():
    try:
        validated = renderer.validate_content(slide_type, content)
        print(f"✅ {slide_type}: Valid")
    except Exception as e:
        print(f"❌ {slide_type}: {e}")
```

## Slide Type Details

### Title Slides

**title_slide** - Presentation opening
```json
{
  "title": "Main title (max 80 chars)",
  "subtitle": "Subtitle or tagline (max 120 chars)"
}
```

**section_title** - Section breaks
```json
{
  "title": "Section title (max 60 chars)"
}
```

### Content Slides

**single_content_with_image** - Feature spotlight
```json
{
  "title": "Content title (max 60 chars)",
  "description": "Description text (max 300 chars)",
  "image_url": "https://...",
  "image_alt": "Image description"
}
```

**highlight** - Key messages, CTAs
```json
{
  "title": "Highlight title (max 40 chars)",
  "content": "Message or CTA (max 200 chars)"
}
```

### List Slides

**two_column_list** - Bullet points (2-4 items)
```json
{
  "title": "List title",
  "items": [
    {"title": "Item title", "description": "Item description"},
    {"title": "Item 2", "description": "Description 2"}
  ]
}
```

**vertical_list** - Detailed features (3-6 items)
```json
{
  "title": "List title",
  "items": [
    {"title": "Item 1", "description": "Description 1"},
    {"title": "Item 2", "description": "Description 2"},
    {"title": "Item 3", "description": "Description 3"}
  ]
}
```

**horizontal_3_column_list** - Three-way comparison (exactly 3)
```json
{
  "title": "List title",
  "items": [
    {"title": "Column 1", "description": "Description"},
    {"title": "Column 2", "description": "Description"},
    {"title": "Column 3", "description": "Description"}
  ]
}
```

**two_columns_with_grid** - 2x2 matrix (exactly 4)
```json
{
  "title": "Grid title",
  "items": [
    {"title": "Q1", "description": "Description"},
    {"title": "Q2", "description": "Description"},
    {"title": "Q3", "description": "Description"},
    {"title": "Q4", "description": "Description"}
  ]
}
```

**horizontal_4_column_list** - Four-step process (exactly 4)
```json
{
  "title": "Process title",
  "items": [
    {"title": "Step 1", "description": "Description"},
    {"title": "Step 2", "description": "Description"},
    {"title": "Step 3", "description": "Description"},
    {"title": "Step 4", "description": "Description"}
  ]
}
```

### Image Slides

**image_with_description_2** - Before/after (2 images + 2 texts)
```json
{
  "title": "Comparison title",
  "images": [
    {"url": "https://...", "alt": "Before"},
    {"url": "https://...", "alt": "After"}
  ],
  "items": [
    {"title": "Before", "description": "Description"},
    {"title": "After", "description": "Description"}
  ]
}
```

**image_with_description_3** - Product gallery (3 images + 3 texts)
```json
{
  "title": "Gallery title",
  "images": [
    {"url": "https://...", "alt": "Product 1"},
    {"url": "https://...", "alt": "Product 2"},
    {"url": "https://...", "alt": "Product 3"}
  ],
  "items": [
    {"title": "Product 1", "description": "Description"},
    {"title": "Product 2", "description": "Description"},
    {"title": "Product 3", "description": "Description"}
  ]
}
```

### Metrics Slides

**three_column_metrics** - KPI dashboard (3 metrics)
```json
{
  "title": "Metrics title",
  "metrics": [
    {"value": "87%", "description": "Metric 1 description"},
    {"value": "$2.5M", "description": "Metric 2 description"},
    {"value": "1,234", "description": "Metric 3 description"}
  ]
}
```

**metrics_grid** - Quarterly metrics (4 metrics in 2x2)
```json
{
  "title": "Quarterly Results",
  "description": "Description about the data",
  "metrics": [
    {"value": "61%", "label": "Q1"},
    {"value": "56%", "label": "Q2"},
    {"value": "55%", "label": "Q3"},
    {"value": "48%", "label": "Q4"}
  ]
}
```

### Special Slides

**quote** - Testimonials, impactful statements
```json
{
  "quote": "Quote text without quotes (max 200 chars)",
  "author": "Author Name · Location"
}
```

## Field Constraints

All fields have validation constraints defined in Pydantic schemas:

- **Titles**: 40-80 characters (varies by type)
- **Descriptions**: 150-300 characters (varies by type)
- **Quotes**: 200 characters
- **Item counts**: Fixed for grid types (3, 4), ranges for lists (2-4, 3-6)
- **URLs**: Valid HTTP/HTTPS or relative paths
- **Alt text**: 100 characters max

## Tips

1. **Start with samples**: Copy a sample and modify it for your needs
2. **Validate early**: Use `renderer.validate_content()` to catch errors
3. **Check constraints**: See `src/slide_renderer/schemas/content.py` for exact limits
4. **Use schemas**: Load `all_schemas.json` for IDE autocomplete
5. **Test incrementally**: Start with one slide type, then expand

## Troubleshooting

### "ValidationError: field required"
- Check that all required fields are present
- See schema for field names

### "ValidationError: string too long"
- Check field length constraints
- Common limits: title (60-80), description (200-300)

### "ValidationError: items must have X items"
- Grid types require exact counts (3 or 4)
- Check `min_length` and `max_length` in schemas

### "Invalid URL"
- Use full URLs: `https://...`
- Or relative paths: `./images/photo.jpg`
- Placeholder: `https://via.placeholder.com/400`

---

For complete API documentation, see the main [README.md](../README.md).
