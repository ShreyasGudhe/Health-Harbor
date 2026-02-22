"""
VitalPlunder Backend - Main Application
========================================
"Plunder Health Risks Before They Strike" ☠️

This is the main Flask application that serves as the central hub
for all VitalPlunder modules. Each module is registered as a Blueprint
for clean, modular architecture.

Author: VitalPlunder Team
Date: January 2026
"""

import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import all module blueprints
from modules.storm_watch.routes import storm_watch_bp
from modules.mind_compass.routes import mind_compass_bp
from modules.captains_orders.routes import captains_orders_bp
from modules.supply_check.routes import supply_check_bp
from modules.night_watch.routes import night_watch_bp
from modules.galley_log.routes import galley_log_bp
from modules.ship_doctor.routes import ship_doctor_bp
from modules.firebase_client import require_firebase_user

# New productivity modules
from modules.treasure_ledger.routes import treasure_ledger_bp
from modules.captains_log.routes import captains_log_bp
from modules.daily_sails.routes import daily_sails_bp


def create_app():
    """
    Application Factory Pattern
    Creates and configures the Flask application
    
    Returns:
        Flask app instance
    """
    app = Flask(__name__)
    
    # ==========================================
    # Configuration
    # ==========================================
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'vitalplunder-secret-key-2026')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')
    
    # Create upload folder if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # ==========================================
    # Enable CORS for React frontend
    # ==========================================
    # Get allowed origins from environment or use defaults
    allowed_origins = os.getenv('ALLOWED_ORIGINS', '').split(',') if os.getenv('ALLOWED_ORIGINS') else [
        "http://localhost:3000",
        "http://localhost:5173",
        "https://*.vercel.app"  # Allow all Vercel deployments
    ]
    
    CORS(app, resources={
        r"/api/*": {
            "origins": allowed_origins + ["https://*.vercel.app"],
            "methods": ["GET", "POST", "PUT", "DELETE"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })
    
    # ==========================================
    # Register Module Blueprints
    # ==========================================
    # Each module has its own Blueprint for modularity
    
    # Module 1: Storm Watch - Health Risk Scanner
    app.register_blueprint(storm_watch_bp, url_prefix='/api/storm-watch')
    
    # Module 2: Mind Compass - Mental Health Monitor
    app.register_blueprint(mind_compass_bp, url_prefix='/api/mind-compass')
    
    # Module 3: Captain's Orders - Lifestyle Coaching
    app.register_blueprint(captains_orders_bp, url_prefix='/api/captains-orders')
    
    # Module 4: Supply Check - Medication Adherence
    app.register_blueprint(supply_check_bp, url_prefix='/api/supply-check')
    
    # Module 5: Night Watch - Sleep Quality Analyzer
    app.register_blueprint(night_watch_bp, url_prefix='/api/night-watch')
    
    # Module 6: Galley Log - Diet & Nutrition Tracker
    app.register_blueprint(galley_log_bp, url_prefix='/api/galley-log')
    
    # Module 7: Ship Doctor - Medical Document Assistant
    app.register_blueprint(ship_doctor_bp, url_prefix='/api/ship-doctor')
    
    # Module 8: Treasure Ledger - Personal Finance
    app.register_blueprint(treasure_ledger_bp)
    
    # Module 9: Captain's Log - Digital Diary
    app.register_blueprint(captains_log_bp)
    
    # Module 10: Daily Sails - Habit Tracker
    app.register_blueprint(daily_sails_bp)
    
    # ==========================================
    # Root Routes
    # ==========================================
    
    @app.route('/')
    def home():
        """
        Home route - Welcome message
        """
        return jsonify({
            'name': 'VitalPlunder API',
            'tagline': 'Plunder Health Risks Before They Strike ☠️',
            'version': '1.0.0',
            'status': 'operational',
            'modules': {
                'storm_watch': '/api/storm-watch',
                'mind_compass': '/api/mind-compass',
                'captains_orders': '/api/captains-orders',
                'supply_check': '/api/supply-check',
                'night_watch': '/api/night-watch',
                'galley_log': '/api/galley-log',
                'ship_doctor': '/api/ship-doctor'
            }
        })
    
    @app.route('/api/health')
    def health_check():
        """
        Health check endpoint for monitoring
        """
        return jsonify({
            'status': 'healthy',
            'message': 'All systems operational, Captain!'
        })

    @app.route('/api/secure/ping')
    @require_firebase_user
    def secure_ping():
        """
        Example protected route using Firebase ID token (Bearer token required)
        """
        return jsonify({
            'status': 'ok',
            'uid': request.firebase_user.get('uid'),
            'email': request.firebase_user.get('email')
        })
    
    # ==========================================
    # Error Handlers
    # ==========================================
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'error': 'Bad Request',
            'message': 'The request could not be understood by the server.',
            'code': 400
        }), 400
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'error': 'Not Found',
            'message': 'The requested resource was not found on this ship.',
            'code': 404
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'The ship has encountered rough waters. Please try again.',
            'code': 500
        }), 500
    
    return app


# ==========================================
# Run the Application
# ==========================================
if __name__ == '__main__':
    app = create_app()
    
    # Get port from environment or default to 5000
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    print("""
    ⚓ VitalPlunder Backend Server ⚓
    ================================
    "Plunder Health Risks Before They Strike"
    
    Server running on: http://localhost:{}
    Debug mode: {}
    
    Available Modules:
    - Storm Watch:      /api/storm-watch
    - Mind Compass:     /api/mind-compass
    - Captain's Orders: /api/captains-orders
    - Supply Check:     /api/supply-check
    - Night Watch:      /api/night-watch
    - Galley Log:       /api/galley-log
    - Ship Doctor:      /api/ship-doctor
    ================================
    """.format(port, debug))
    
    app.run(host='0.0.0.0', port=port, debug=debug)
