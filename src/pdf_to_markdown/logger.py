"""Processing details logging for PDF to Markdown conversion."""

import json
import platform
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import docling
from docling_core.types.doc import DoclingDocument

from . import __version__
from .metadata import DocumentMetadata


class ProcessingLogger:
    """Logs processing details to JSON file."""
    
    def __init__(self) -> None:
        """Initialize the processing logger."""
        self.start_time: float | None = None
        self.end_time: float | None = None
        self.start_timestamp: datetime | None = None
        self.end_timestamp: datetime | None = None
        
    def start_timing(self) -> None:
        """Start the processing timer."""
        self.start_time = time.perf_counter()
        self.start_timestamp = datetime.now(timezone.utc)
        
    def stop_timing(self) -> float:
        """
        Stop the timer and return processing duration.
        
        Returns:
            Processing duration in seconds
        """
        if self.start_time is None:
            return 0.0
            
        self.end_time = time.perf_counter()
        self.end_timestamp = datetime.now(timezone.utc)
        
        return self.end_time - self.start_time
    
    def extract_metadata(self, result: Any, document: DoclingDocument, pdf_path: Path) -> dict[str, Any]:
        """
        Extract document metadata from Docling conversion result.
        
        Args:
            result: Docling conversion result
            document: Docling document object
            pdf_path: Path to the original PDF file
            
        Returns:
            Dictionary with extracted metadata
        """
        # Get basic document info
        doc_info = DocumentMetadata.get_document_info(document, pdf_path)
        
        # Add conversion result status if available
        if hasattr(result, 'status'):
            doc_info["conversion_status"] = str(result.status)
        
        return doc_info
    
    def create_log_entry(
        self,
        pdf_path: Path,
        output_path: Path,
        verbose: bool,
        command_line: str,
        document_metadata: dict[str, Any],
        processing_duration: float
    ) -> dict[str, Any]:
        """
        Create complete log entry structure.
        
        Args:
            pdf_path: Path to input PDF file
            output_path: Path to output Markdown file
            verbose: Whether verbose mode was enabled
            command_line: Original command line invocation
            document_metadata: Document metadata dictionary
            processing_duration: Processing time in seconds
            
        Returns:
            Complete log entry as dictionary
        """
        # Processing details
        processing_details = {
            "processing_time_seconds": round(processing_duration, 3),
            "start_time": self.start_timestamp.isoformat() if self.start_timestamp else None,
            "end_time": self.end_timestamp.isoformat() if self.end_timestamp else None
        }
        
        # Processing speed metrics
        page_count = document_metadata.get("page_count")
        processing_speed = DocumentMetadata.calculate_processing_speed(page_count, processing_duration)
        
        # Utility parameters
        utility_parameters = {
            "input_file": str(pdf_path),
            "output_file": str(output_path),
            "ocr_languages": ["en"],  # Default OCR language
            "verbose_mode": verbose,
            "command_line": command_line
        }
        
        # System information
        system_info = {
            "utility_version": __version__,
            "docling_version": getattr(docling, '__version__', 'unknown'),
            "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            "platform": platform.platform(),
            "architecture": platform.architecture()[0]
        }
        
        return {
            "processing_details": processing_details,
            "document_metadata": document_metadata,
            "processing_speed": processing_speed,
            "utility_parameters": utility_parameters,
            "system_info": system_info
        }
    
    def save_processing_log(self, log_data: dict[str, Any], output_path: Path) -> None:
        """
        Save JSON log to file.
        
        Args:
            log_data: Log data dictionary to save
            output_path: Path where to save the JSON log file
            
        Raises:
            OSError: If file cannot be written
            json.JSONEncodeError: If data cannot be serialized to JSON
        """
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(log_data, f, indent=2, ensure_ascii=False)
        except (OSError, json.JSONEncodeError) as e:
            raise OSError(f"Failed to write processing log: {e}") from e
