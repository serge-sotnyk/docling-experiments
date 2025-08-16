# PDF to Markdown Converter

A command-line utility that converts PDF documents to Markdown format using [Docling](https://github.com/DS4SD/docling) with integrated EasyOCR support.

## Features

- 📄 **PDF to Markdown conversion** - Convert any PDF document to clean Markdown format
- 🔍 **OCR integration** - Built-in EasyOCR support for text recognition in scanned documents
- 🌍 **Multi-language OCR** - Support for multiple languages (English, French, German, Spanish, etc.)
- 🎯 **Smart file naming** - Automatically generates output files with `.pdf.md` extension
- 🛡️ **Error handling** - Comprehensive validation and error reporting
- 📊 **Progress tracking** - Verbose mode with file size statistics
- ⚡ **Modern stack** - Built with Docling v2, Click CLI framework, and EasyOCR

## Installation

This project uses [uv](https://github.com/astral-sh/uv) for dependency management:

```bash
# Clone the repository
git clone <repository-url>
cd docling-experiments

# Install dependencies
uv sync
```

## Usage

### Basic Usage

```bash
# Convert PDF to Markdown
uv run python -m src.pdf_to_markdown.cli document.pdf

# The output will be saved as: document.pdf.md
```

### Advanced Options

```bash
# Specify custom output file
uv run python -m src.pdf_to_markdown.cli document.pdf -o output.md

# Enable multiple OCR languages
uv run python -m src.pdf_to_markdown.cli document.pdf --languages en,fr,de

# Verbose output with statistics
uv run python -m src.pdf_to_markdown.cli document.pdf --verbose
```

### Help

```bash
uv run python -m src.pdf_to_markdown.cli --help
```

## Example Output

```bash
$ uv run python -m src.pdf_to_markdown.cli document.pdf --verbose

Input PDF: document.pdf
OCR Languages: en
Initializing PDF to Markdown converter...
Converting PDF to Markdown...
✅ Successfully converted PDF to Markdown
📄 Input: document.pdf
📝 Output: document.pdf.md
📊 Input size: 680,979 bytes
📊 Output size: 980,518 bytes
```

## Technical Details

### Architecture

- **Converter Core** (`src/pdf_to_markdown/converter.py`) - Main conversion logic using Docling
- **CLI Interface** (`src/pdf_to_markdown/cli.py`) - Command-line interface built with Click
- **OCR Integration** - EasyOCR configured through Docling's `PdfPipelineOptions`

### Dependencies

- **[Docling](https://github.com/DS4SD/docling)** (≥2.44.0) - Advanced document processing library
- **[EasyOCR](https://github.com/JaidedAI/EasyOCR)** (≥1.7.1) - OCR engine for text recognition
- **[Click](https://click.palletsprojects.com/)** (≥8.2.1) - Command-line interface framework

### Supported OCR Languages

EasyOCR supports 80+ languages including:
- `en` - English (default)
- `fr` - French
- `de` - German
- `es` - Spanish
- `ru` - Russian
- `zh` - Chinese
- And many more...

## Requirements

- Python ≥3.13
- Windows/Linux/macOS
- Internet connection (for initial model downloads)

## Error Handling

The utility includes comprehensive error handling for:
- File not found errors
- Permission errors
- Invalid file formats (non-PDF files)
- Docling conversion failures
- OCR processing errors
- Output file write errors

## Performance Notes

- **First run**: May take longer due to automatic model downloads
- **GPU support**: EasyOCR can utilize GPU if available (CUDA)
- **Memory usage**: Depends on PDF size and complexity
- **Processing time**: Varies with document length and OCR requirements

## Development

### Project Structure

```
src/pdf_to_markdown/
├── __init__.py          # Package initialization
├── converter.py         # Core PDF to Markdown conversion logic
└── cli.py              # Command-line interface
```

### Running Tests

```bash
# Test with a sample PDF
uv run python -m src.pdf_to_markdown.cli sample.pdf --verbose
```

## License

This project is experimental and created for learning purposes.

## Contributing

Feel free to submit issues and enhancement requests!
