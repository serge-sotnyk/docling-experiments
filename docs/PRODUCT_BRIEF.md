# Product Brief: Docling Experiments

## Project Overview / Description

This repository serves as an experimental playground for testing and evaluating the functionality of the [Docling library](https://github.com/docling-project/docling). Docling is an advanced document processing library that simplifies parsing diverse document formats and provides seamless integrations with the generative AI ecosystem.

The project aims to explore Docling's capabilities in document conversion, advanced PDF understanding, table extraction, OCR functionality, and various export formats to assess its potential for production use cases.

## Target Audience

- **Data Scientists and AI Engineers** working with document processing pipelines
- **Developers** building applications that require document parsing and content extraction
- **Researchers** exploring document understanding and multimodal AI applications
- **Technical Teams** evaluating Docling for enterprise document processing workflows

## Primary Benefits / Features

- **Multi-format Document Processing**: Test parsing of PDF, DOCX, PPTX, XLSX, HTML, audio files (WAV, MP3), and images
- **Advanced PDF Understanding**: Experiment with page layout analysis, reading order detection, table structure recognition, and image classification
- **Export Format Testing**: Evaluate various output formats including Markdown, HTML, DocTags, and lossless JSON
- **OCR Capabilities**: Test optical character recognition for scanned documents and images
- **AI Integration Experiments**: Explore integrations with LangChain, LlamaIndex, and other AI frameworks
- **Visual Language Model Support**: Test SmolDocling and other VLM capabilities
- **Local Processing**: Evaluate air-gapped and sensitive data processing scenarios

## High-level Tech/Architecture Used

- **Programming Language**: Python 3.13
- **Package Manager**: uv (fast Python package installer and resolver)
- **Core Library**: Docling for document processing and conversion
- **Architecture**: Local execution environment with potential for:
  - Document ingestion pipelines
  - Content extraction and transformation workflows
  - Integration with AI/ML frameworks
  - Export to various structured formats

## Development Environment

- Modern Python environment with type annotations and latest language features
- Dependency management via uv.lock for reproducible builds
- Modular structure for testing different Docling features and use cases
