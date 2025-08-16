"""PDF to Markdown conversion using Docling with EasyOCR integration."""

from pathlib import Path
from typing import Any

from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling_core.types.doc import DoclingDocument

from .logger import ProcessingLogger


class PDFToMarkdownConverter:
    """Converts PDF documents to Markdown using Docling with EasyOCR."""
    
    def __init__(self, enable_logging: bool = True) -> None:
        """
        Initialize the converter with Docling pipeline and EasyOCR configuration.
        
        Args:
            enable_logging: Whether to enable processing details logging
        """
        self.enable_logging = enable_logging
        self.logger = ProcessingLogger() if enable_logging else None
        
        # Configure PDF pipeline with OCR enabled
        pipeline_options = PdfPipelineOptions()
        pipeline_options.do_ocr = True
        
        # Initialize DocumentConverter with PDF format options
        self.doc_converter = DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
            }
        )
    
    def convert_pdf_to_markdown(self, pdf_path: Path) -> str:
        """
        Convert a PDF file to Markdown content.
        
        Args:
            pdf_path: Path to the PDF file to convert
            
        Returns:
            Markdown content as string
            
        Raises:
            FileNotFoundError: If the PDF file doesn't exist
            ValueError: If the file is not a PDF
            RuntimeError: If conversion fails
        """
        # Validate input file
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        if pdf_path.suffix.lower() != '.pdf':
            raise ValueError(f"File must be a PDF: {pdf_path}")
        
        try:
            # Convert PDF using Docling
            result = self.doc_converter.convert(pdf_path)
            
            # Extract the document
            doc: DoclingDocument = result.document
            
            # Export to Markdown
            markdown_content = doc.export_to_markdown()
            
            return markdown_content
            
        except Exception as e:
            raise RuntimeError(f"Failed to convert PDF to Markdown: {e}") from e
    
    def save_markdown(self, content: str, output_path: Path) -> None:
        """
        Save Markdown content to a file.
        
        Args:
            content: Markdown content to save
            output_path: Path where to save the Markdown file
            
        Raises:
            OSError: If file cannot be written
        """
        try:
            output_path.write_text(content, encoding='utf-8')
        except OSError as e:
            raise OSError(f"Failed to write Markdown file: {e}") from e
    
    def convert_with_logging(
        self, 
        pdf_path: Path, 
        verbose: bool = False, 
        command_line: str = ""
    ) -> tuple[str, Any, DoclingDocument]:
        """
        Convert PDF to Markdown with logging and timing.
        
        Args:
            pdf_path: Path to the PDF file to convert
            verbose: Whether verbose mode is enabled
            command_line: Original command line invocation
            
        Returns:
            Tuple of (markdown_content, conversion_result, document)
            
        Raises:
            FileNotFoundError: If the PDF file doesn't exist
            ValueError: If the file is not a PDF
            RuntimeError: If conversion fails
        """
        # Validate input file
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        if pdf_path.suffix.lower() != '.pdf':
            raise ValueError(f"File must be a PDF: {pdf_path}")
        
        # Start timing if logging is enabled
        if self.logger:
            self.logger.start_timing()
        
        try:
            # Convert PDF using Docling
            result = self.doc_converter.convert(pdf_path)
            
            # Extract the document
            doc: DoclingDocument = result.document
            
            # Export to Markdown
            markdown_content = doc.export_to_markdown()
            
            # Stop timing if logging is enabled
            if self.logger:
                processing_duration = self.logger.stop_timing()
                
                # Extract metadata
                document_metadata = self.logger.extract_metadata(result, doc, pdf_path)
                
                # Generate output paths
                markdown_output_path = pdf_path.with_suffix(pdf_path.suffix + '.md')
                json_output_path = pdf_path.with_suffix('.json')
                
                # Create log entry
                log_data = self.logger.create_log_entry(
                    pdf_path=pdf_path,
                    output_path=markdown_output_path,
                    verbose=verbose,
                    command_line=command_line,
                    document_metadata=document_metadata,
                    processing_duration=processing_duration
                )
                
                # Save processing log
                self.logger.save_processing_log(log_data, json_output_path)
            
            return markdown_content, result, doc
            
        except Exception as e:
            raise RuntimeError(f"Failed to convert PDF to Markdown: {e}") from e
    
    def convert_and_save(
        self, 
        pdf_path: Path, 
        verbose: bool = False, 
        command_line: str = ""
    ) -> Path:
        """
        Convert PDF to Markdown and save to the same directory.
        
        Args:
            pdf_path: Path to the PDF file to convert
            verbose: Whether verbose mode is enabled  
            command_line: Original command line invocation
            
        Returns:
            Path to the created Markdown file
            
        Raises:
            FileNotFoundError: If the PDF file doesn't exist
            ValueError: If the file is not a PDF
            RuntimeError: If conversion fails
            OSError: If output file cannot be written
        """
        if self.enable_logging:
            # Use logging-enabled conversion
            markdown_content, result, doc = self.convert_with_logging(pdf_path, verbose, command_line)
        else:
            # Use simple conversion
            markdown_content = self.convert_pdf_to_markdown(pdf_path)
        
        # Generate output filename by appending .md to original PDF name
        output_path = pdf_path.with_suffix(pdf_path.suffix + '.md')
        
        # Save Markdown content
        self.save_markdown(markdown_content, output_path)
        
        return output_path