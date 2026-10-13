# AI-Powered OCR-Based KYC Document Processing and Verification System

## Project Overview

The **OCR-Based KYC Document Processing and Verification System** is a Python-based application designed to simplify Know Your Customer (KYC) document processing.

The application uses Optical Character Recognition (OCR) to extract information from PAN cards and Aadhaar cards. It applies regular expressions, data normalization, and validation logic to process extracted information and compare customer details across documents.

The project follows a modular, object-oriented programming approach to organize document processing, field extraction, validation, verification, and report generation.

## Key Features

- **Document Upload:** Accepts KYC documents for processing through a Streamlit interface.
- **OCR-Based Text Extraction:** Uses Pytesseract to extract text from document images.
- **Field Extraction:** Uses regular expressions to identify relevant information from extracted text.
- **Data Normalization:** Standardizes extracted values for consistent comparison.
- **Field Validation:** Validates extracted information using predefined rules.
- **Document Verification:** Compares selected customer details, such as name and date of birth, across documents.
- **Structured Output:** Organizes extracted information and verification results into structured data and reports.
- **Modular Architecture:** Separates processing tasks into reusable Python modules.

## Technologies Used

| Technology                  | Purpose                               |
| --------------------------- | ------------------------------------- |
| Python                      | Core application logic                |
| Streamlit                   | Web-based user interface              |
| Pytesseract                 | Optical Character Recognition         |
| Tesseract OCR               | OCR engine                            |
| Pillow (PIL)                | Image handling                        |
| Regular Expressions (Regex) | Field extraction and pattern matching |
| Pandas                      | Structured data processing            |

## System Workflow

1. Upload the required KYC document images.
2. Process the images using the application's document-processing pipeline.
3. Extract text using Pytesseract OCR.
4. Identify relevant fields using regular expressions.
5. Normalize and validate the extracted values.
6. Compare selected fields across documents when applicable.
7. Generate structured output and verification results.

## Project Structure

The exact structure may vary depending on the modules in your local project.

```text
KYC-Project/
├── .venv/
├── main.py
├── README.md
├── requirements.txt
├── <OCR and document-processing modules>
├── <validation and verification modules>
└── <output or report files, if applicable>
```

Replace the illustrative module entries with the actual filenames in your project.

## Prerequisites

Before running the application, ensure that you have:

- Python installed.
- Git installed if you plan to use GitHub.
- Tesseract OCR installed and accessible on your system.
- Visual Studio Code or another Python-compatible editor.

## Installation and Setup

### 1. Clone the repository

If you have cloned the project from GitHub:

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd <YOUR_PROJECT_FOLDER>
```

Alternatively, open your existing local project folder directly in VS Code.

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

**Windows PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install Python dependencies

After creating `requirements.txt`, install the required packages:

```bash
python -m pip install -r requirements.txt
```

### 5. Install Tesseract OCR

Install the Tesseract OCR engine separately. The Python package `pytesseract` acts as an interface to this engine and does not install the OCR executable itself.

Ensure that Tesseract is available through your system PATH or configured correctly in your application.

### 6. Run the Streamlit application

If your Streamlit entry-point file is named `main.py`:

```bash
python -m streamlit run main.py
```

If your entry-point file has a different name, replace `main.py` with the correct filename.

Streamlit will provide a local URL, usually:

```text
http://localhost:8501
```

Open that URL in your browser to access the application.

## Limitations

- OCR accuracy depends on document image quality, orientation, and readability.
- Incorrect or incomplete text extraction may affect subsequent validation and comparison.
- Regex-based extraction depends on predefined patterns and expected document formats.
- Extracted information should be reviewed before making consequential KYC decisions.
- OCR extraction and field matching do not independently establish the authenticity of a document.

## Future Enhancements

- Containerize the application using Docker.
- Automate testing and deployment using GitHub Actions.
- Deploy the application to a cloud platform.
- Add automated tests for OCR extraction, validation, and verification.
- Improve document preprocessing and error handling.
- Introduce secure handling and controlled retention of sensitive KYC data.

## Disclaimer

This project is intended for educational and development purposes. It is not a substitute for an authorized KYC verification process. Avoid uploading real customer identity documents to public repositories or exposing sensitive personal information in application logs or generated reports.

## Author

Developed as a Python-based document processing and verification project.
