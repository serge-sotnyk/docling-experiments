"""Command-line interface for PDF to Markdown converter."""

import sys
from pathlib import Path
from typing import Optional

import click

from .converter import PDFToMarkdownConverter


@click.command()
@click.argument('pdf_path', type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option(
    '--output', '-o',
    type=click.Path(path_type=Path),
    help='Output Markdown file path (default: PDF path with .md suffix)'
)
@click.option(
    '--languages', '-l',
    type=str,
    default='en',
    help='OCR languages (comma-separated, default: en)'
)
@click.option(
    '--verbose', '-v',
    is_flag=True,
    help='Enable verbose output'
)
def main(pdf_path: Path, output: Optional[Path], languages: str, verbose: bool) -> None:
    """Convert PDF file to Markdown using Docling with EasyOCR.
    
    PDF_PATH: Path to the PDF file to convert
    
    Examples:
        pdf-to-md document.pdf
        pdf-to-md document.pdf -o output.md
        pdf-to-md document.pdf --languages en,fr,de
    """
    try:
        # Parse OCR languages
        ocr_languages = [lang.strip() for lang in languages.split(',') if lang.strip()]
        
        if verbose:
            click.echo(f"Input PDF: {pdf_path}")
            click.echo(f"OCR Languages: {', '.join(ocr_languages)}")
        
        # Initialize converter
        if verbose:
            click.echo("Initializing PDF to Markdown converter...")
        
        converter = PDFToMarkdownConverter(ocr_languages=ocr_languages)
        
        # Convert and save
        if verbose:
            click.echo("Converting PDF to Markdown...")
        
        output_path = converter.convert_and_save(pdf_path, output)
        
        # Success message
        click.echo(f"✅ Successfully converted PDF to Markdown")
        click.echo(f"📄 Input: {pdf_path}")
        click.echo(f"📝 Output: {output_path}")
        
        if verbose:
            # Show file sizes
            input_size = pdf_path.stat().st_size
            output_size = output_path.stat().st_size
            click.echo(f"📊 Input size: {input_size:,} bytes")
            click.echo(f"📊 Output size: {output_size:,} bytes")
        
    except FileNotFoundError as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)
    except PermissionError as e:
        click.echo(f"❌ Permission Error: {e}", err=True)
        sys.exit(1)
    except ValueError as e:
        click.echo(f"❌ Validation Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"❌ Conversion Error: {e}", err=True)
        if verbose:
            import traceback
            click.echo("Full traceback:", err=True)
            click.echo(traceback.format_exc(), err=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
