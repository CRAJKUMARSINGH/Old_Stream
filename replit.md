# Contractor Bill Generator

## Overview

This is a Streamlit-based web application that processes Excel files to generate contractor bills and related documentation. The application supports two file formats - "Old Pattern" (without title sheet) and "New Pattern" (with title sheet as the first sheet). It automatically detects the file format and generates multiple document types including first page summaries, extra items, deviation statements, certificates, memorandums, and note sheets.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit for web interface
- **Layout**: Wide layout with expandable sidebar
- **Styling**: Custom CSS for professional appearance with success/error messaging
- **File Upload**: Single file upload mechanism with automatic processing

### Backend Architecture
- **Language**: Python
- **Structure**: Modular design with separate utility modules
- **Processing Pipeline**: File upload → Format detection → Data extraction → Document generation
- **Template Engine**: Jinja2 for HTML template rendering

### Document Generation
- **Multi-format Output**: HTML, PDF, and DOCX generation
- **Template System**: HTML templates for different document types
- **PDF Generation**: WeasyPrint for HTML to PDF conversion
- **Word Documents**: python-docx for DOCX generation

## Key Components

### 1. Main Application (app.py)
- Streamlit web interface
- File upload handling
- User interaction management
- Progress tracking and status updates

### 2. Excel Processor (utils/excel_processor.py)
- **File Format Detection**: Automatically detects "Old Pattern" vs "New Pattern" files
- **Data Extraction**: Processes work order items, bill quantities, and extra items
- **Title Sheet Handling**: Extracts metadata from title sheets in new format files
- **Calculations**: Computes totals and financial summaries

### 3. Document Generator (utils/document_generator.py)
- **Multi-format Generation**: Creates HTML, PDF, and DOCX versions
- **Template Rendering**: Uses Jinja2 for dynamic content generation
- **File Management**: Handles temporary file creation and cleanup
- **Format Conversion**: Converts between different document formats

### 4. Formatters (utils/formatters.py)
- **Number Formatting**: Handles decimal places and rounding
- **Currency Formatting**: Indian numbering system with rupee symbol
- **Date Formatting**: Standardized date display
- **Locale Support**: Attempts to use Indian locale settings

### 5. Template System
- **HTML Templates**: Professional document layouts
- **Responsive Design**: A4 page sizing with proper margins
- **Consistent Styling**: Shared CSS for professional appearance
- **Document Types**: 
  - First page summaries
  - Extra items
  - Deviation statements
  - Certificates and signatures
  - Memorandums
  - Note sheets

## Data Flow

1. **File Upload**: User uploads Excel file through Streamlit interface
2. **Format Detection**: System automatically detects file format (Old/New Pattern)
3. **Data Extraction**: 
   - Title sheet processing (for New Pattern files)
   - Work order items extraction
   - Bill quantity items extraction
   - Extra items processing
4. **Calculations**: Financial totals and summaries computed
5. **Document Generation**: Multiple document types generated in HTML, PDF, and DOCX formats
6. **Output Delivery**: ZIP file containing all generated documents

## External Dependencies

### Core Libraries
- **streamlit**: Web application framework
- **pandas**: Excel file processing and data manipulation
- **numpy**: Numerical calculations
- **openpyxl**: Excel file reading support

### Document Generation
- **jinja2**: Template engine for HTML generation
- **weasyprint**: HTML to PDF conversion
- **python-docx**: Microsoft Word document generation

### File Handling
- **tempfile**: Temporary file management
- **zipfile**: Archive creation for document delivery
- **os**: Operating system interface

## Deployment Strategy

### Local Development
- **Environment**: Python virtual environment
- **Dependencies**: Requirements managed through pip
- **File Storage**: Temporary directory for document generation
- **Cleanup**: Automatic temporary file removal

### Production Considerations
- **Streamlit Cloud**: Ready for deployment on Streamlit Cloud
- **Memory Management**: Efficient handling of large Excel files
- **Error Handling**: Comprehensive error reporting and logging
- **File Limits**: Configurable file size limits for uploads

### Key Features
- **Automatic Format Detection**: No manual format selection required
- **Zero Manual Input**: Fully automated processing after file upload
- **Professional Output**: High-quality document generation
- **Multi-format Support**: HTML, PDF, and DOCX output
- **Batch Processing**: Multiple documents generated simultaneously
- **World-Class Efficiency**: Real-time performance monitoring and optimization insights
- **Performance Analytics**: Efficiency scoring system with throughput metrics
- **Advanced UI**: Animated crane logo with gradient backgrounds and celebration effects

### Architecture Benefits
- **Modularity**: Clean separation of concerns
- **Extensibility**: Easy to add new document types
- **Maintainability**: Well-structured codebase
- **Scalability**: Efficient processing pipeline
- **User Experience**: Simple upload-and-process workflow