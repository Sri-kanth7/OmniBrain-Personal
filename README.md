# OmniBrain – PDF Ingestion Engine

A modular and scalable PDF Ingestion Engine designed as the foundation of the OmniBrain platform. This project extracts structured information from PDF documents, including metadata, text, images, and tables, and prepares them for downstream AI applications such as Retrieval-Augmented Generation (RAG), document understanding, and multimodal processing.

---

## Overview

OmniBrain aims to transform unstructured PDF documents into structured, machine-readable data.

The current implementation focuses on building a reliable PDF ingestion pipeline that processes a document through multiple extraction stages while maintaining a clean and extensible architecture.

---

## Features

### PDF Reader
- PDF validation
- Open and close PDF documents
- Page count retrieval
- Metadata access
- Encrypted PDF detection

### Metadata Extraction
Extracts document information including:
- File name
- File size
- Page count
- Title
- Author
- Subject
- Keywords
- Creator
- Producer
- Creation date
- Modification date

### Text Extraction
- Page-wise text extraction
- UTF-8 encoding support
- Empty page detection
- Character statistics
- Structured text output

### Image Extraction
- Embedded image extraction
- Duplicate image detection using XREF
- Image metadata collection
- Organized image storage

### Table Extraction
- Table detection using pdfplumber
- CSV export
- Table metadata generation

### Report Generation
Generates a structured JSON report summarizing:
- Metadata
- Text statistics
- Image statistics
- Table statistics

---

# Project Structure

```
OmniBrain/
│
├── app/
│   └── main.py
│
├── configs/
│   ├── settings.py
│   └── logging.yaml
│
├── src/
│   ├── ingestion/
│   │   ├── pdf_reader.py
│   │   ├── metadata.py
│   │   ├── text_extractor.py
│   │   ├── image_extractor.py
│   │   ├── table_extractor.py
│   │   ├── report_generator.py
│   │   └── pipeline.py
│   │
│   ├── preprocessing/
│   ├── embeddings/
│   ├── retrieval/
│   ├── agents/
│   ├── llm/
│   ├── utils/
│   ├── models/
│   └── exceptions/
│
├── data/
│   ├── input/
│   │   └── pdfs/
│   │
│   ├── processed/
│   │   ├── metadata/
│   │   ├── text/
│   │   ├── images/
│   │   ├── tables/
│   │   └── reports/
│   │
│   └── temp/
│
├── docs/
├── logs/
├── reports/
├── scripts/
├── tests/
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

# Processing Pipeline

```
PDF
 │
 ▼
PDF Reader
 │
 ▼
Metadata Extraction
 │
 ▼
Text Extraction
 │
 ▼
Image Extraction
 │
 ▼
Table Extraction
 │
 ▼
Report Generation
 │
 ▼
Processed Outputs
```

---

# Installation

Clone the repository

```bash
git clone <repository-url>
cd OmniBrain
```

Create and activate a virtual environment

```bash
conda create -n omnibrain python=3.11
conda activate omnibrain
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# Usage

Place a PDF inside

```
data/input/pdfs/
```

Run the application

```bash
python -m app.main
```

---

# Output Structure

```
data/
└── processed/
    ├── metadata/
    ├── text/
    ├── images/
    ├── tables/
    └── reports/
```

Each processed PDF generates:

- Metadata JSON
- Extracted text
- Embedded images
- Extracted tables (CSV)
- Processing report

---

# Technologies Used

- Python 3.11
- PyMuPDF
- pdfplumber
- EasyOCR
- Pillow
- Pandas
- NumPy
- Loguru
- LayoutParser

---

# Current Status

### Completed

- Project Architecture
- PDF Reader
- Metadata Extraction
- Text Extraction
- Image Extraction
- Table Extraction
- Report Generator
- Pipeline Orchestration

### In Progress

- OCR Integration
- Logging System
- Progress Tracking
- Exception Handling

### Planned

- Layout Analysis
- Semantic Chunking
- Embedding Generation
- Vector Database Integration
- Hybrid Retrieval
- Agentic Workflow
- Multimodal RAG

---

# Future Vision

The PDF Ingestion Engine is the first component of the OmniBrain ecosystem.

Future versions will support:

- OCR for scanned documents
- Intelligent layout understanding
- Semantic document chunking
- Vision-language models
- Vector database integration
- Multi-agent orchestration
- Enterprise-scale document processing

---

# Author

**Srikanth Chevvakula**

B.Tech Computer Science & Engineering

Rajiv Gandhi University of Knowledge Technologies (RGUKT)

---

## License

This project is currently under active development.