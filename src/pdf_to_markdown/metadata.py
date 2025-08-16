"""Document metadata extraction utilities for Docling documents."""

import os
from pathlib import Path
from typing import Any

from docling_core.types.doc import DoclingDocument


class DocumentMetadata:
    """Extracts metadata from Docling documents."""
    
    @staticmethod
    def get_page_count(document: DoclingDocument) -> int | None:
        """
        Extract page count from Docling document.
        
        Args:
            document: Docling document object
            
        Returns:
            Number of pages or None if unavailable
        """
        try:
            # Try to get page count from document structure
            if hasattr(document, 'pages') and document.pages:
                return len(document.pages)
            
            # Alternative: check page numbers in document elements
            page_numbers = set()
            for element in document.main_text:
                if hasattr(element, 'page') and element.page is not None:
                    page_numbers.add(element.page)
            
            if page_numbers:
                return max(page_numbers) + 1  # Pages are 0-indexed
            
            return None
            
        except Exception:
            return None
    
    @staticmethod
    def get_document_info(document: DoclingDocument, pdf_path: Path) -> dict[str, Any]:
        """
        Extract additional document information.
        
        Args:
            document: Docling document object
            pdf_path: Path to the original PDF file
            
        Returns:
            Dictionary with document information
        """
        info = {}
        
        try:
            # File size
            info["file_size_bytes"] = os.path.getsize(pdf_path)
        except OSError:
            info["file_size_bytes"] = None
        
        # Page count
        info["page_count"] = DocumentMetadata.get_page_count(document)
        
        # Check if document has OCR content
        info["has_ocr_content"] = DocumentMetadata._has_ocr_content(document)
        
        # Estimate text pages
        info["estimated_text_pages"] = DocumentMetadata._estimate_text_pages(document)
        
        # Document status
        info["conversion_status"] = "SUCCESS"
        
        return info
    
    @staticmethod
    def _has_ocr_content(document: DoclingDocument) -> bool:
        """Check if document contains OCR-processed content."""
        try:
            # Check if there are any elements that might indicate OCR processing
            # This is a heuristic - we look for image-derived text content
            for element in document.main_text:
                if hasattr(element, 'source') and element.source:
                    # If source indicates OCR or image processing
                    if 'ocr' in str(element.source).lower():
                        return True
            return False
        except Exception:
            return False
    
    @staticmethod
    def _estimate_text_pages(document: DoclingDocument) -> int:
        """Estimate number of pages with text content."""
        try:
            text_pages = set()
            for element in document.main_text:
                if hasattr(element, 'page') and element.page is not None:
                    if hasattr(element, 'text') and element.text and element.text.strip():
                        text_pages.add(element.page)
            return len(text_pages)
        except Exception:
            return 0
    
    @staticmethod
    def calculate_processing_speed(page_count: int | None, duration: float) -> dict[str, Any]:
        """
        Calculate processing speed metrics.
        
        Args:
            page_count: Number of pages in document
            duration: Processing time in seconds
            
        Returns:
            Dictionary with speed metrics
        """
        if page_count is None or page_count == 0 or duration <= 0:
            return {
                "seconds_per_page": None,
                "pages_per_minute": None,
                "pages_per_second": None
            }
        
        seconds_per_page = duration / page_count
        pages_per_minute = (page_count / duration) * 60
        pages_per_second = page_count / duration
        
        return {
            "seconds_per_page": round(seconds_per_page, 2),
            "pages_per_minute": round(pages_per_minute, 2), 
            "pages_per_second": round(pages_per_second, 4)
        }
