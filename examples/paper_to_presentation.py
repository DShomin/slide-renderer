"""
Paper to Presentation Converter - Simplified Example

Demonstrates the 2-phase generation system using the modular API:
- Phase 1: Planning (decide slide types and content outline)
- Phase 2: Async parallel slide generation with validation retry

Usage:
    # Korean (default)
    python examples/paper_to_presentation.py

    # English
    python examples/paper_to_presentation.py --language en

    # Japanese with custom slide count
    python examples/paper_to_presentation.py -l ja -s 8
"""

import asyncio
import argparse
import json
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from paper_to_presentation import convert_paper_to_presentation

# Load environment variables
load_dotenv()


async def main():
    parser = argparse.ArgumentParser(description="Convert research paper to Marp presentation")
    parser.add_argument(
        "-i", "--input",
        default="sample_data/usecase/paper/attention_is_all_you_need.json",
        help="Input paper JSON file"
    )
    parser.add_argument(
        "-o", "--output",
        default=None,
        help="Output markdown file (default: auto-generated based on language)"
    )
    parser.add_argument(
        "-s", "--slides",
        type=int,
        default=10,
        help="Maximum number of slides (default: 10)"
    )
    parser.add_argument(
        "-l", "--language",
        default="ko",
        choices=["ko", "en", "ja", "zh", "es", "fr", "de"],
        help="Target language (default: ko)"
    )
    args = parser.parse_args()

    # Determine input path (relative to project root)
    project_root = Path(__file__).parent.parent
    input_path = project_root / args.input

    if not input_path.exists():
        print(f"❌ Input file not found: {input_path}")
        return 1

    # Auto-generate output filename if not specified
    if args.output is None:
        args.output = f"attention_is_all_you_need_presentation_{args.language}.md"

    # Load paper data
    print(f"📄 Loading paper: {input_path}")
    with open(input_path, "r", encoding="utf-8") as f:
        paper_data = json.load(f)

    # Convert to presentation
    try:
        markdown = await convert_paper_to_presentation(
            paper_data=paper_data,
            output_file=args.output,
            max_slides=args.slides,
            target_language=args.language
        )

        print("\n" + "=" * 70)
        print("✨ CONVERSION COMPLETE!")
        print("=" * 70)
        print(f"📝 Output file: {args.output}")
        print(f"📊 Slides generated: Check the markdown file")
        print(f"\nTo view the presentation:")
        print(f"  marp --theme custom-style.css {args.output}")
        print(f"  marp --theme custom-style.css {args.output} -o output.pdf")

        return 0

    except Exception as e:
        print(f"\n❌ Conversion failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
