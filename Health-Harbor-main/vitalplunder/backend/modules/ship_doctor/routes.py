"""
Ship Doctor - API Routes
========================
Module 7: Medical Document AI Assistant

REST API endpoints for medical document analysis.

Author: VitalPlunder Team

⚠️ IMPORTANT: This module provides INFORMATIONAL content only.
It does NOT provide medical advice, diagnosis, or treatment.
"""

import os
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from .document_parser import parse_medical_image, parse_medical_pdf, extract_values
from .gemini_analyzer import analyze_medical_document, get_medical_disclaimer

# Create Blueprint
ship_doctor_bp = Blueprint('ship_doctor', __name__)

# Allowed file extensions
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'tiff'}
ALLOWED_PDF_EXTENSIONS = {'pdf'}


def allowed_file(filename, extensions):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in extensions


@ship_doctor_bp.route('/', methods=['GET'])
def index():
    """Module info endpoint"""
    return jsonify({
        'module': 'Ship Doctor',
        'description': 'Medical Document AI Assistant - Analyze medical reports',
        'disclaimer': 'FOR INFORMATIONAL PURPOSES ONLY. NOT MEDICAL ADVICE.',
        'endpoints': {
            'POST /analyze-image': 'Analyze medical document image',
            'POST /analyze-pdf': 'Analyze medical document PDF',
            'POST /analyze-text': 'Analyze extracted text directly',
            'GET /disclaimer': 'Get medical disclaimer'
        }
    })


@ship_doctor_bp.route('/disclaimer', methods=['GET'])
def disclaimer():
    """
    Get medical disclaimer
    
    Returns:
        JSON with medical disclaimer text
    """
    return jsonify({
        'success': True,
        'disclaimer': get_medical_disclaimer(),
        'important': 'This tool is NOT a substitute for professional medical advice.'
    }), 200


@ship_doctor_bp.route('/analyze-image', methods=['POST'])
def analyze_image():
    """
    Analyze medical document from image
    
    Form Data:
        document: Image file (PNG, JPG, etc.)
        
    Returns:
        JSON with document analysis
    """
    try:
        # Check for file
        if 'document' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No document file uploaded'
            }), 400
        
        file = request.files['document']
        
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400
        
        if not allowed_file(file.filename, ALLOWED_IMAGE_EXTENSIONS):
            return jsonify({
                'success': False,
                'error': f'Invalid file type. Allowed: {", ".join(ALLOWED_IMAGE_EXTENSIONS)}'
            }), 400
        
        # Read file data
        image_data = file.read()
        
        # Step 1: Parse document (OCR)
        parse_result = parse_medical_image(image_data)
        
        if not parse_result.get('success'):
            return jsonify({
                'success': False,
                'error': 'Failed to parse document',
                'details': parse_result.get('error')
            }), 500
        
        extracted_text = parse_result.get('text', '')
        
        # Step 2: Extract medical values
        values = extract_values(extracted_text)
        
        # Step 3: Analyze with AI
        analysis = analyze_medical_document(extracted_text)
        
        return jsonify({
            'success': True,
            'parsing': {
                'method': parse_result.get('method'),
                'character_count': parse_result.get('character_count')
            },
            'extracted_text': extracted_text[:2000] + ('...' if len(extracted_text) > 2000 else ''),
            'values_found': values,
            'analysis': analysis.get('analysis'),
            'analysis_method': analysis.get('method'),
            'disclaimer': analysis.get('disclaimer')
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Analysis failed: {str(e)}'
        }), 500


@ship_doctor_bp.route('/analyze-pdf', methods=['POST'])
def analyze_pdf():
    """
    Analyze medical document from PDF
    
    Form Data:
        document: PDF file
        
    Returns:
        JSON with document analysis
    """
    try:
        # Check for file
        if 'document' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No document file uploaded'
            }), 400
        
        file = request.files['document']
        
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400
        
        if not allowed_file(file.filename, ALLOWED_PDF_EXTENSIONS):
            return jsonify({
                'success': False,
                'error': 'File must be a PDF'
            }), 400
        
        # Read file data
        pdf_data = file.read()
        
        # Step 1: Parse PDF
        parse_result = parse_medical_pdf(pdf_data)
        
        if not parse_result.get('success'):
            return jsonify({
                'success': False,
                'error': 'Failed to parse PDF',
                'details': parse_result.get('error')
            }), 500
        
        extracted_text = parse_result.get('text', '')
        
        # Step 2: Extract medical values
        values = extract_values(extracted_text)
        
        # Step 3: Analyze with AI
        analysis = analyze_medical_document(extracted_text)
        
        return jsonify({
            'success': True,
            'parsing': {
                'method': parse_result.get('method'),
                'page_count': parse_result.get('page_count'),
                'character_count': parse_result.get('character_count')
            },
            'extracted_text': extracted_text[:2000] + ('...' if len(extracted_text) > 2000 else ''),
            'values_found': values,
            'analysis': analysis.get('analysis'),
            'analysis_method': analysis.get('method'),
            'disclaimer': analysis.get('disclaimer')
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Analysis failed: {str(e)}'
        }), 500


@ship_doctor_bp.route('/analyze-text', methods=['POST'])
def analyze_text():
    """
    Analyze medical document from text directly
    
    Request Body:
    {
        "text": "LABORATORY REPORT\nHemoglobin: 14.2 g/dL..."
    }
    
    Returns:
        JSON with document analysis
    """
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({
                'success': False,
                'error': 'Please provide document text',
                'example': {'text': 'LABORATORY REPORT\nHemoglobin: 14.2 g/dL...'}
            }), 400
        
        text = data['text']
        
        if len(text.strip()) < 20:
            return jsonify({
                'success': False,
                'error': 'Text too short for analysis'
            }), 400
        
        # Extract medical values
        values = extract_values(text)
        
        # Analyze with AI
        analysis = analyze_medical_document(text)
        
        return jsonify({
            'success': True,
            'values_found': values,
            'analysis': analysis.get('analysis'),
            'analysis_method': analysis.get('method'),
            'disclaimer': analysis.get('disclaimer')
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Analysis failed: {str(e)}'
        }), 500


@ship_doctor_bp.route('/supported-formats', methods=['GET'])
def supported_formats():
    """
    Get supported file formats
    
    Returns:
        JSON with supported formats
    """
    return jsonify({
        'success': True,
        'image_formats': list(ALLOWED_IMAGE_EXTENSIONS),
        'document_formats': list(ALLOWED_PDF_EXTENSIONS),
        'max_file_size': '16MB',
        'tips': [
            'Ensure document is clearly visible',
            'Good lighting improves OCR accuracy',
            'PDF with selectable text works best',
            'Avoid blurry or low-resolution images'
        ]
    }), 200
