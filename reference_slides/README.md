# Reference Slides

This directory contains the **expected markdown output** for each of the 14 slide types. These reference files serve as the "ground truth" for template rendering.

## Purpose

Reference slides are used for:

1. **Validation**: Compare your renderer output against these references
2. **Documentation**: See exactly what each template produces
3. **Template Development**: Use as targets when creating or modifying templates
4. **Testing**: Automated tests verify that rendering matches these outputs

## Origin

These markdown files were **created from the actual Marp theme project** that slide-renderer is based on. They represent production-quality, tested slide layouts that work with the custom Marp theme.

## File Naming Convention

Files are named alphabetically to match the original slide order:

| Prefix | Slide Type | File Name |
|--------|------------|-----------|
| `a-` | Title | `a-title-slide.md` |
| `b-` | Section Title | `b-section-title.md` |
| `c-` | Single Content | `c-single-content-with-image.md` |
| `d-` | Highlight | `d-highlight.md` |
| `e-` | Two Column List | `e-two-column-list.md` |
| `f-` | Vertical List | `f-vertical-list.md` |
| `g-` | 3 Column List | `g-horizontal-3-column-list.md` |
| `h-` | 2x2 Grid | `h-two-columns-with-2x2-grid.md` |
| `i-` | 4 Column List | `i-horizontal-4-column-list.md` |
| `j-` | 2 Images | `j-image-with-description---2-images-text.md` |
| `k-` | 3 Images | `k-image-with-description---3-images-text.md` |
| `l-` | 3 Metrics | `l-3-column-metrics.md` |
| `m-` | Metrics Grid | `m-metrics-grid.md` |
| `n-` | Quote | `n-quote.md` |

### `_frontmatter.md`

Contains the Marp frontmatter configuration:

```markdown
---
marp: true
theme: custom-style
---
```

This is automatically added by `SlideRenderer` when `include_frontmatter=True`.

## Usage

### Compare Output

```python
from pathlib import Path
from slide_renderer import SlideRenderer

# Load sample and reference
import json
with open("sample_data/sample_slides.json") as f:
    samples = json.load(f)

reference_file = Path("reference_slides/m-metrics-grid.md")
reference = reference_file.read_text()

# Render sample
renderer = SlideRenderer()
rendered = renderer.render("metrics_grid", samples["metrics_grid"])

# Compare
if rendered.strip() == reference.strip():
    print("✅ Output matches reference")
else:
    print("❌ Output differs from reference")
```

### Automated Testing

```python
import pytest
from pathlib import Path
from slide_renderer import SlideRenderer

SLIDE_TYPE_FILES = {
    "title_slide": "a-title-slide.md",
    "metrics_grid": "m-metrics-grid.md",
    # ... etc
}

@pytest.mark.parametrize("slide_type", SLIDE_TYPE_FILES.keys())
def test_rendering_matches_reference(slide_type):
    """Test that rendering matches reference markdown."""
    renderer = SlideRenderer()

    # Load sample data
    with open("sample_data/sample_slides.json") as f:
        samples = json.load(f)

    # Render
    rendered = renderer.render(slide_type, samples[slide_type])

    # Load reference
    ref_file = Path("reference_slides") / SLIDE_TYPE_FILES[slide_type]
    reference = ref_file.read_text()

    # Compare (normalize whitespace)
    assert rendered.strip() == reference.strip()
```

### Template Customization

When customizing templates:

1. **Modify template**: Edit `templates/{slide_type}.jinja2`
2. **Render sample**: Use sample data to generate output
3. **Compare**: Check against reference to see what changed
4. **Update reference**: If changes are intentional, update the reference file

```python
from slide_renderer import SlideRenderer

# Use custom template
renderer = SlideRenderer(template_dir="my_custom_templates")

# Render with sample data
with open("sample_data/sample_slides.json") as f:
    samples = json.load(f)

custom_output = renderer.render("metrics_grid", samples["metrics_grid"])

# Load original reference
with open("reference_slides/m-metrics-grid.md") as f:
    reference = f.read()

# Show differences
import difflib
diff = difflib.unified_diff(
    reference.splitlines(),
    custom_output.splitlines(),
    lineterm="",
    fromfile="reference",
    tofile="custom"
)
print("\n".join(diff))
```

## File Structure

Each reference file contains:

### 1. Frontmatter (in `_frontmatter.md`)

```markdown
---
marp: true
theme: custom-style
---
```

### 2. Slide Content

Pure markdown with Marp-specific features:

- **HTML classes**: `<div class="two-column">` for layouts
- **CSS classes**: `.container`, `.grid-3col`, etc.
- **Placeholders**: For images when actual images aren't available
- **Semantic HTML**: Proper structure for accessibility

### 3. Metadata Comments (optional)

Some files include HTML comments with metadata:

```markdown
<!-- slide type: metrics_grid -->
<!-- version: 1.0 -->
```

## Slide Type Examples

### Title Slide (`a-title-slide.md`)

```markdown
# Slide Deck Title

## Description or subtitle for the presentation
```

### Metrics Grid (`m-metrics-grid.md`)

```markdown
<div class="container">

<div style="flex: 1;">

# Metrics Grid

Description about the data beside. Lorem ipsum dolor sit amet...

</div>

<div class="two-column">

<div class="metric-item">
<div class="metric-value">61%</div>
<div class="metric-label">Metric 1</div>
</div>

...

</div>

</div>
```

### Quote (`n-quote.md`)

```markdown
<!-- _class: center -->

> "This is a quote or testimonial..."

**Full Name · Location**
```

## Validation Notes

When comparing rendered output to references:

### Normalize Whitespace

```python
def normalize(text):
    lines = [line.rstrip() for line in text.split("\n")]
    while lines and not lines[0]:
        lines.pop(0)
    while lines and not lines[-1]:
        lines.pop()
    return "\n".join(lines)

assert normalize(rendered) == normalize(reference)
```

### Ignore Frontmatter

```python
def remove_frontmatter(text):
    if text.startswith("---\n"):
        parts = text.split("---\n", 2)
        if len(parts) >= 3:
            return parts[2]
    return text
```

### Line Ending Differences

```python
rendered = rendered.replace("\r\n", "\n")
reference = reference.replace("\r\n", "\n")
```

## Marp Theme Compatibility

These reference files are designed for use with the **custom-style** Marp theme. Key features:

- **Layout Classes**: `.two-column`, `.container`, `.grid-3col`, etc.
- **Typography**: Pretendard font family
- **Metrics**: `.metric-item`, `.metric-value`, `.metric-label`
- **Placeholders**: `.placeholder`, `.placeholder-small`

If you're using a different Marp theme, you may need to adjust:

1. CSS class names
2. HTML structure
3. Layout patterns

## Tips

1. **Use references as templates**: Copy structure and adapt content
2. **Validate incrementally**: Check one slide type at a time
3. **Watch whitespace**: Trailing spaces and newlines matter
4. **Test with real theme**: Render with Marp CLI to see final output
5. **Version control**: Keep references in sync with template changes

## Troubleshooting

### Rendering doesn't match reference

1. **Check template**: Ensure template hasn't been modified
2. **Check sample data**: Use exact data from `sample_slides.json`
3. **Normalize comparison**: Use whitespace normalization
4. **Check Jinja2 config**: Ensure `trim_blocks` and `lstrip_blocks` match

### Marp rendering looks wrong

1. **Theme mismatch**: Ensure using `custom-style` theme
2. **CSS classes**: Check that theme includes required classes
3. **HTML validation**: Validate HTML structure
4. **Marp version**: Some features require specific Marp versions

### Reference seems outdated

1. **Check template**: See if template was updated
2. **Regenerate**: Render with current template and compare
3. **Update reference**: If template change is intentional, update reference

---

For complete documentation, see the main [README.md](../README.md).
