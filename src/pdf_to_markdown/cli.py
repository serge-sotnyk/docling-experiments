"""Command line interface for PDF to Markdown conversion."""

import sys
from pathlib import Path

import click

from .converter import PDFToMarkdownConverter


@click.command()
@click.argument('pdf_path', type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
@click.option('--disable-logging', is_flag=True, help='Disable JSON processing details logging')
def main(pdf_path: Path, verbose: bool, disable_logging: bool) -> None:
    """
    Convert a PDF file to Markdown using Docling with EasyOCR.
    
    PDF_PATH: Path to the PDF file to convert. The resulting Markdown file
    will be saved in the same directory with a .md suffix added to the original filename.
    By default, also creates a JSON file with processing details.
    
    Example:
        pdf-to-md document.pdf
        # Creates document.pdf.md and document.json in the same directory
        
        pdf-to-md document.pdf --disable-logging
        # Creates only document.pdf.md (no JSON log)
    """
    try:
        if verbose:
            click.echo(f"Converting PDF: {pdf_path}")
        
        # Capture command line for logging
        command_line = f"pdf-to-md {pdf_path}"
        if verbose:
            command_line += " --verbose"
        if disable_logging:
            command_line += " --disable-logging"
        
        # Initialize converter with logging preference
        enable_logging = not disable_logging
        converter = PDFToMarkdownConverter(enable_logging=enable_logging)
        
        # Convert and save
        output_path = converter.convert_and_save(
            pdf_path=pdf_path,
            verbose=verbose,
            command_line=command_line
        )
        
        # Report success
        click.echo(f"✅ Successfully converted PDF to Markdown: {output_path}")
        
        if enable_logging:
            _, json_path = converter._generate_output_paths(pdf_path)
            click.echo(f"📊 Processing details saved to: {json_path}")
        
    except FileNotFoundError as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)
        
    except ValueError as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)
        
    except RuntimeError as e:
        click.echo(f"❌ Conversion failed: {e}", err=True)
        sys.exit(1)
        
    except OSError as e:
        click.echo(f"❌ File write error: {e}", err=True)
        sys.exit(1)
        
    except Exception as e:
        click.echo(f"❌ Unexpected error: {e}", err=True)
        if verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()