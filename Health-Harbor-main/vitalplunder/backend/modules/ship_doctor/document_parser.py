"""
Ship Doctor - Document Parser
=============================
Module 7: Medical Document AI Assistant

OCR-based document parsing for medical reports.
Uses Tesseract for text extraction.

Author: VitalPlunder Team
"""

import os
import re
import io
from PIL import Image

# Optional: Try to import pytesseract
try:
    import pytesseract
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False

# Optional: Try to import PyPDF2
try:
    from PyPDF2 import PdfReader
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False


class DocumentParser:
    """
    Medical Document Parser using OCR
    
    Extracts text from medical documents (images and PDFs)
    for further analysis.
    """
    
    # Common medical terms to identify
    MEDICAL_MARKERS = {
        'lab_values': [
            'hemoglobin', 'hb', 'wbc', 'rbc', 'platelets', 'glucose',
            'cholesterol', 'hdl', 'ldl', 'triglycerides', 'creatinine',
            'bun', 'sodium', 'potassium', 'calcium', 'tsh', 'hba1c',
            'alt', 'ast', 'bilirubin', 'albumin', 'vitamin d', 'b12'
        ],
        'vital_signs': [
            'blood pressure', 'bp', 'heart rate', 'pulse', 'temperature',
            'respiratory rate', 'oxygen saturation', 'spo2', 'weight', 'bmi'
        ],
        'flags': [
            'high', 'low', 'abnormal', 'critical', 'positive', 'negative',
            'elevated', 'decreased', 'normal', 'borderline'
        ]
    }
    
    def __init__(self):
        """Initialize document parser"""
        # Set tesseract path if on Windows
        tesseract_path = os.getenv('TESSERACT_PATH')
        if tesseract_path and TESSERACT_AVAILABLE:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
    
    def parse_image(self, image_data):
        """
        Extract text from image using OCR
        
        Args:
            image_data: Image bytes or file path
            
        Returns:
            Extracted text and metadata
        """
        if not TESSERACT_AVAILABLE:
            return self._placeholder_ocr(image_data)
        
        try:
            # Load image
            if isinstance(image_data, bytes):
                image = Image.open(io.BytesIO(image_data))
            elif isinstance(image_data, str):
                image = Image.open(image_data)
            else:
                image = image_data
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Perform OCR
            text = pytesseract.image_to_string(image)
            
            return {
                'success': True,
                'text': text,
                'method': 'tesseract_ocr',
                'character_count': len(text),
                'line_count': len(text.split('\n'))
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'OCR failed: {str(e)}',
                'method': 'tesseract_ocr'
            }
    
    def parse_pdf(self, pdf_data):
        """
        Extract text from PDF document
        
        Args:
            pdf_data: PDF bytes or file path
            
        Returns:
            Extracted text and metadata
        """
        if not PDF_AVAILABLE:
            return {
                'success': False,
                'error': 'PDF support not available. Install PyPDF2.',
                'method': 'pypdf2'
            }
        
        try:
            # Load PDF
            if isinstance(pdf_data, bytes):
                reader = PdfReader(io.BytesIO(pdf_data))
            else:
                reader = PdfReader(pdf_data)
            
            # Extract text from all pages
            text_parts = []
            for page_num, page in enumerate(reader.pages):
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(f"--- Page {page_num + 1} ---\n{page_text}")
            
            text = '\n\n'.join(text_parts)
            
            return {
                'success': True,
                'text': text,
                'method': 'pypdf2',
                'page_count': len(reader.pages),
                'character_count': len(text)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'PDF parsing failed: {str(e)}',
                'method': 'pypdf2'
            }
    
    def _placeholder_ocr(self, image_data):
        """
        Placeholder OCR when Tesseract is not available
        Returns demo data for testing
        """
        return {
            'success': True,
            'text': '''LABORATORY REPORT
Patient Name: Demo Patient
Date: January 15, 2026

COMPLETE BLOOD COUNT:
Hemoglobin: 14.2 g/dL (Normal: 12-16)
WBC: 7.5 x10^9/L (Normal: 4-11)
RBC: 4.8 x10^12/L (Normal: 4.2-5.4)
Platelets: 250 x10^9/L (Normal: 150-400)

LIPID PANEL:
Total Cholesterol: 195 mg/dL (Normal: <200)
HDL: 55 mg/dL (Normal: >40)
LDL: 120 mg/dL (Normal: <100) - ELEVATED
Triglycerides: 145 mg/dL (Normal: <150)

METABOLIC PANEL:
Glucose (Fasting): 98 mg/dL (Normal: 70-100)
HbA1c: 5.8% (Normal: <5.7) - BORDERLINE
Creatinine: 1.0 mg/dL (Normal: 0.7-1.3)

THYROID:
TSH: 2.5 mIU/L (Normal: 0.4-4.0)

Notes: LDL cholesterol slightly elevated. Consider lifestyle modifications.
''',
            'method': 'placeholder_demo',
            'note': 'Tesseract OCR not available. Using demo data.',
            'character_count': 850
        }
    
    def extract_medical_values(self, text):
        """
        Extract medical values from parsed text
        
        Args:
            text: Parsed document text
            
        Returns:
            Extracted values and findings
        """
        findings = {
            'values': [],
            'flags': [],
            'summary': []
        }
        
        text_lower = text.lower()
        lines = text.split('\n')
        
        # Look for lab values
        for line in lines:
            line_lower = line.lower()
            
            # Check for medical markers
            for marker in self.MEDICAL_MARKERS['lab_values']:
                if marker in line_lower:
                    # Try to extract value
                    value_match = re.search(r':\s*([\d.]+)', line)
                    if value_match:
                        findings['values'].append({
                            'test': marker.upper(),
                            'value': value_match.group(1),
                            'line': line.strip()
                        })
            
            # Check for flags
            for flag in self.MEDICAL_MARKERS['flags']:
                if flag in line_lower:
                    if flag in ['high', 'elevated', 'abnormal', 'critical', 'positive']:
                        findings['flags'].append({
                            'flag': flag,
                            'line': line.strip(),
                            'severity': 'attention'
                        })
        
        return findings


# Create singleton instance
document_parser = DocumentParser()


def parse_medical_image(image_data):
    """Convenience function for image parsing"""
    return document_parser.parse_image(image_data)


def parse_medical_pdf(pdf_data):
    """Convenience function for PDF parsing"""
    return document_parser.parse_pdf(pdf_data)


def extract_values(text):
    """Convenience function for value extraction"""
    return document_parser.extract_medical_values(text)
