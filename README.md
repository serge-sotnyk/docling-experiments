# PDF to Markdown Converter

A command-line utility that converts PDF documents to Markdown format using [Docling](https://github.com/DS4SD/docling) with integrated EasyOCR support.

## Features

- 📄 **PDF to Markdown conversion** - Convert any PDF document to clean Markdown format
- 🔍 **OCR integration** - Built-in EasyOCR support for text recognition in scanned documents  
- 📊 **Processing details logging** - Automatic JSON logging with timing, metadata, and performance metrics
- 🎯 **Smart file naming** - Automatically generates output files with `.pdf.md` and `.json` extensions
- ⏱️ **Performance tracking** - Detailed processing time and speed metrics (pages/minute, seconds/page)
- 📈 **Document metadata** - Extract page count, file size, OCR status, and conversion details
- 🛡️ **Error handling** - Comprehensive validation and error reporting
- 🔧 **Configurable logging** - Enable/disable JSON logging via command-line options
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
If you use Windows and don't have Visual Studio Build Tools you may need to install
Visual C++ Redistributables from https://aka.ms/vs/17/release/vc_redist.x64.exe

## Usage

### Basic Usage

```bash
# Convert PDF to Markdown with JSON logging (default)
uv run python -m src.pdf_to_markdown.cli document.pdf

# This creates:
# - document.pdf.md (Markdown content)
# - document.json (Processing details and metadata)
```

### Advanced Options

```bash
# Verbose output with detailed progress information
uv run python -m src.pdf_to_markdown.cli document.pdf --verbose

# Disable JSON logging (Markdown output only)
uv run python -m src.pdf_to_markdown.cli document.pdf --disable-logging

# Combine options
uv run python -m src.pdf_to_markdown.cli document.pdf --verbose --disable-logging
```

### Help

```bash
uv run python -m src.pdf_to_markdown.cli --help
```

## Example Output

```bash
$ uv run python -m src.pdf_to_markdown.cli document.pdf --verbose

Converting PDF: document.pdf
✅ Successfully converted PDF to Markdown: document.pdf.md
📊 Processing details saved to: document.json
```

### JSON Processing Log Example

The generated JSON file contains comprehensive processing information:

```json
{
  "processing_details": {
    "processing_time_seconds": 45.123,
    "start_time": "2024-01-15T14:30:22.123Z",
    "end_time": "2024-01-15T14:31:07.246Z"
  },
  "document_metadata": {
    "file_size_bytes": 1186101,
    "page_count": 7,
    "has_ocr_content": false,
    "estimated_text_pages": 6,
    "conversion_status": "ConversionStatus.SUCCESS"
  },
  "processing_speed": {
    "seconds_per_page": 6.45,
    "pages_per_minute": 9.31,
    "pages_per_second": 0.155
  },
  "utility_parameters": {
    "input_file": "document.pdf",
    "output_file": "document.pdf.md",
    "ocr_languages": ["en"],
    "verbose_mode": true
  },
  "system_info": {
    "utility_version": "0.1.0",
    "docling_version": "2.44.0",
    "python_version": "3.13.1",
    "platform": "Windows-10-10.0.19045-SP0"
  }
}
```

## Technical Details

### Architecture

- **Converter Core** (`src/pdf_to_markdown/converter.py`) - Main conversion logic using Docling with timing integration
- **CLI Interface** (`src/pdf_to_markdown/cli.py`) - Command-line interface built with Click
- **Processing Logger** (`src/pdf_to_markdown/logger.py`) - JSON logging system for processing details
- **Metadata Extractor** (`src/pdf_to_markdown/metadata.py`) - Document metadata and performance calculation utilities
- **OCR Integration** - EasyOCR configured through Docling's `PdfPipelineOptions`

### Dependencies

- **[Docling](https://github.com/DS4SD/docling)** (≥2.44.0) - Advanced document processing library
- **[EasyOCR](https://github.com/JaidedAI/EasyOCR)** (≥1.7.1) - OCR engine for text recognition
- **[Click](https://click.palletsprojects.com/)** (≥8.2.1) - Command-line interface framework

### JSON Logging Features

The automatic JSON logging provides:
- **Processing Timing** - Start/end timestamps and total duration
- **Document Metadata** - Page count, file size, OCR content detection
- **Performance Metrics** - Pages per minute, seconds per page, processing speed
- **System Information** - Utility version, Docling version, Python version, platform
- **Command Parameters** - Complete record of CLI arguments and settings used

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
- **JSON logging**: Minimal performance impact, can be disabled with `--disable-logging`
- **Timing accuracy**: Uses high-precision `time.perf_counter()` for accurate measurements
- **Metadata extraction**: Automatic page counting and document analysis included in timing

## Development

### Project Structure

```
src/pdf_to_markdown/
├── __init__.py          # Package initialization
├── converter.py         # Core PDF to Markdown conversion logic with timing
├── cli.py              # Command-line interface with logging options
├── logger.py           # Processing details logging and JSON export
└── metadata.py         # Document metadata extraction and performance calculations
```

### Running Tests

```bash
# Test basic conversion with JSON logging
uv run python -m src.pdf_to_markdown.cli sample.pdf

# Test with verbose output and logging disabled
uv run python -m src.pdf_to_markdown.cli sample.pdf --verbose --disable-logging

# Check generated files
ls sample.pdf.md sample.json  # (if logging enabled)
```

## License

This project is experimental and created for learning purposes.

## Contributing

Feel free to submit issues and enhancement requests!
