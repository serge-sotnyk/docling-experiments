"""PDF to Markdown converter using Docling with EasyOCR integration."""

from pathlib import Path
from typing import Optional

from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions, EasyOcrOptions
from docling.document_converter import DocumentConverter, PdfFormatOption


class PDFToMarkdownConverter:
    """Converts PDF documents to Markdown using Docling with EasyOCR."""

    def __init__(self, ocr_languages: Optional[list[str]] = None):
        """Initialize the converter with optional OCR language configuration.
        
        Args:
            ocr_languages: List of language codes for OCR (default: ["en"])
        """
        self.ocr_languages = ocr_languages or ["en"]
        self._setup_converter()

    def _setup_converter(self) -> None:
        """Setup the Docling DocumentConverter with EasyOCR configuration."""
        # Configure pipeline options with OCR enabled
        pipeline_options = PdfPipelineOptions()
        pipeline_options.do_ocr = True
        
        # Configure EasyOCR options
        ocr_options = EasyOcrOptions()
        ocr_options.lang = self.ocr_languages
        pipeline_options.ocr_options = ocr_options
        
        # Initialize DocumentConverter with PDF format options
        self.doc_converter = DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
            }
        )

    def convert_pdf_to_markdown(self, pdf_path: Path) -> str:
        """Convert a PDF file to Markdown format.
        
        Args:
            pdf_path: Path to the PDF file to convert
            
        Returns:
            Markdown content as string
            
        Raises:
            FileNotFoundError: If PDF file doesn't exist
            PermissionError: If PDF file can't be read
            Exception: For other conversion errors
        """
        # Validate input file
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        if not pdf_path.is_file():
            raise ValueError(f"Path is not a file: {pdf_path}")
        
        if pdf_path.suffix.lower() != '.pdf':
            raise ValueError(f"File is not a PDF: {pdf_path}")
        
        try:
            # Convert PDF using Docling
            result = self.doc_converter.convert(str(pdf_path))
            
            # Check conversion status
            if result.status.name != "SUCCESS":
                raise Exception(f"PDF conversion failed with status: {result.status}")
            
            # Export to Markdown
            markdown_content = result.document.export_to_markdown()
            
            return markdown_content
            
        except PermissionError as e:
            raise PermissionError(f"Cannot read PDF file {pdf_path}: {e}")
        except Exception as e:
            raise Exception(f"Failed to convert PDF {pdf_path}: {e}")

    def save_markdown(self, content: str, output_path: Path) -> None:
        """Save Markdown content to a file.
        
        Args:
            content: Markdown content to save
            output_path: Path where to save the Markdown file
            
        Raises:
            PermissionError: If output file can't be written
            Exception: For other file writing errors
        """
        try:
            # Create parent directories if they don't exist
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write Markdown content to file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
        except PermissionError as e:
            raise PermissionError(f"Cannot write to output file {output_path}: {e}")
        except Exception as e:
            raise Exception(f"Failed to save Markdown to {output_path}: {e}")

    def convert_and_save(self, pdf_path: Path, output_path: Optional[Path] = None) -> Path:
        """Convert PDF to Markdown and save to file.
        
        Args:
            pdf_path: Path to the PDF file to convert
            output_path: Optional output path (default: PDF path with .md suffix)
            
        Returns:
            Path to the saved Markdown file
            
        Raises:
            Same exceptions as convert_pdf_to_markdown and save_markdown
        """
        # Generate output path if not provided
        if output_path is None:
            output_path = pdf_path.with_suffix(pdf_path.suffix + '.md')
        
        # Convert PDF to Markdown
        markdown_content = self.convert_pdf_to_markdown(pdf_path)
        
        # Save Markdown content
        self.save_markdown(markdown_content, output_path)
        
        return output_path
