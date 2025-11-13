.PHONY: help install examples basic llm clean test format lint

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Install package in development mode
	pip install -e .

examples: basic llm ## Run all examples

basic: ## Run basic usage example
	@echo "Running basic usage example..."
	@python examples/basic_usage.py

llm: ## Run LLM integration example
	@echo "Running LLM integration example..."
	@python examples/llm_integration.py

solar: ## Run Solar Pro2 example (requires .env with UPSTAGE_API_KEY)
	@echo "Running Solar Pro2 example..."
	@python examples/solar_pro2_example.py

paper: ## Convert paper JSON to presentation (requires .env with UPSTAGE_API_KEY)
	@echo "Converting paper to presentation..."
	@python examples/paper_to_presentation.py

paper-en: ## Convert paper to English presentation
	@echo "Converting paper to English presentation..."
	@python examples/paper_to_presentation.py --language en

paper-ja: ## Convert paper to Japanese presentation
	@echo "Converting paper to Japanese presentation..."
	@python examples/paper_to_presentation.py --language ja

sample: ## Render sample_slides.json to markdown
	@python scripts/render_sample.py

clean: ## Clean generated files
	@echo "Cleaning generated files..."
	@rm -f output_presentation.md
	@rm -f sample_presentation.md
	@rm -f solar_pro2_presentation.md
	@rm -f attention_is_all_you_need_presentation.md
	@rm -f example_presentation.json
	@rm -f *.pdf
	@rm -f *.html
	@rm -f *.pptx
	@rm -rf __pycache__
	@rm -rf .pytest_cache
	@rm -rf .mypy_cache
	@rm -rf .ruff_cache
	@rm -rf src/slide_renderer/__pycache__
	@rm -rf examples/__pycache__
	@rm -rf tests/__pycache__
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete
	@echo "✅ Cleaned"

test: ## Run tests
	pytest tests/

format: ## Format code with ruff
	ruff format .

lint: ## Lint code with ruff
	ruff check .

typecheck: ## Type check with mypy
	mypy src/

# Marp-related commands
marp-install: ## Install Marp CLI (requires npm)
	@echo "Installing Marp CLI..."
	@command -v npm >/dev/null 2>&1 || { echo "Error: npm is required but not installed. Install Node.js first."; exit 1; }
	npm install -g @marp-team/marp-cli
	@echo "✅ Marp CLI installed"

marp-check: ## Check if Marp CLI is installed
	@command -v marp >/dev/null 2>&1 && echo "✅ Marp CLI is installed" || echo "❌ Marp CLI is not installed. Run 'make marp-install'"

render-pdf: ## Render markdown to PDF (requires MARKDOWN_FILE variable)
	@if [ -z "$(MARKDOWN_FILE)" ]; then \
		echo "Error: MARKDOWN_FILE variable is required"; \
		echo "Usage: make render-pdf MARKDOWN_FILE=output_presentation.md"; \
		exit 1; \
	fi
	@command -v marp >/dev/null 2>&1 || { echo "Error: Marp CLI is not installed. Run 'make marp-install'"; exit 1; }
	marp --theme ../custom-style.css $(MARKDOWN_FILE) --pdf
	@echo "✅ PDF generated: $(basename $(MARKDOWN_FILE) .md).pdf"

render-html: ## Render markdown to HTML (requires MARKDOWN_FILE variable)
	@if [ -z "$(MARKDOWN_FILE)" ]; then \
		echo "Error: MARKDOWN_FILE variable is required"; \
		echo "Usage: make render-html MARKDOWN_FILE=output_presentation.md"; \
		exit 1; \
	fi
	@command -v marp >/dev/null 2>&1 || { echo "Error: Marp CLI is not installed. Run 'make marp-install'"; exit 1; }
	marp --theme ../custom-style.css $(MARKDOWN_FILE) --html
	@echo "✅ HTML generated: $(basename $(MARKDOWN_FILE) .md).html"

render-pptx: ## Render markdown to PowerPoint (requires MARKDOWN_FILE variable)
	@if [ -z "$(MARKDOWN_FILE)" ]; then \
		echo "Error: MARKDOWN_FILE variable is required"; \
		echo "Usage: make render-pptx MARKDOWN_FILE=output_presentation.md"; \
		exit 1; \
	fi
	@command -v marp >/dev/null 2>&1 || { echo "Error: Marp CLI is not installed. Run 'make marp-install'"; exit 1; }
	marp --theme ../custom-style.css $(MARKDOWN_FILE) --pptx
	@echo "✅ PowerPoint generated: $(basename $(MARKDOWN_FILE) .md).pptx"

# Quick workflow: generate and render
demo: basic render-pdf-demo ## Generate example and render to PDF
	@echo "✅ Demo complete: check output_presentation.pdf"

sample-demo: sample render-pdf-sample ## Generate sample presentation and render to PDF
	@echo "✅ Sample demo complete: check sample_presentation.pdf"

render-pdf-sample: ## Render sample_presentation.md to PDF
	@if [ ! -f sample_presentation.md ]; then \
		echo "Error: sample_presentation.md not found. Run 'make sample' first."; \
		exit 1; \
	fi
	@make render-pdf MARKDOWN_FILE=sample_presentation.md

render-pdf-demo: ## Render the output_presentation.md to PDF
	@if [ ! -f output_presentation.md ]; then \
		echo "Error: output_presentation.md not found. Run 'make basic' first."; \
		exit 1; \
	fi
	@make render-pdf MARKDOWN_FILE=output_presentation.md
