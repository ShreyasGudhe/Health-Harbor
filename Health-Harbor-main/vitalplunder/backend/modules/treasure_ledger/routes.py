"""
Treasure Ledger - API Routes
=============================
Personal Finance Management endpoints.

Endpoints:
- POST /api/treasure-ledger/transaction - Add transaction
- GET /api/treasure-ledger/transactions - List transactions
- GET /api/treasure-ledger/summary - Monthly summary
- GET /api/treasure-ledger/alerts - Spending alerts

Author: VitalPlunder Team
"""

from flask import Blueprint, request, jsonify
from .finance_manager import get_finance_manager, FinanceManager

treasure_ledger_bp = Blueprint('treasure_ledger', __name__, url_prefix='/api/treasure-ledger')


@treasure_ledger_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'module': 'Treasure Ledger',
        'message': 'Count your doubloons! 💰'
    })


@treasure_ledger_bp.route('/transaction', methods=['POST'])
def add_transaction():
    """
    Add a new financial transaction
    
    Request body:
    {
        "type": "income" | "expense",
        "amount": 100.00,
        "category": "food",
        "description": "Lunch",
        "date": "2026-01-16"  // optional
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate required fields
        if 'type' not in data:
            return jsonify({'error': 'Transaction type is required'}), 400
        if 'amount' not in data:
            return jsonify({'error': 'Amount is required'}), 400
        if 'category' not in data:
            return jsonify({'error': 'Category is required'}), 400
        
        manager = get_finance_manager()
        transaction = manager.add_transaction(
            trans_type=data['type'],
            amount=float(data['amount']),
            category=data['category'],
            description=data.get('description', ''),
            date=data.get('date')
        )
        
        return jsonify({
            'success': True,
            'transaction': transaction,
            'message': 'Transaction logged to the treasure ledger! 💰'
        }), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@treasure_ledger_bp.route('/transactions', methods=['GET'])
def get_transactions():
    """
    Get list of transactions with optional filters
    
    Query params:
    - start_date: Filter from date (YYYY-MM-DD)
    - end_date: Filter until date (YYYY-MM-DD)
    - type: Filter by 'income' or 'expense'
    """
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        trans_type = request.args.get('type')
        
        manager = get_finance_manager()
        transactions = manager.get_transactions(
            start_date=start_date,
            end_date=end_date,
            trans_type=trans_type
        )
        
        return jsonify({
            'success': True,
            'count': len(transactions),
            'transactions': transactions
        })
        
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@treasure_ledger_bp.route('/summary', methods=['GET'])
def get_summary():
    """
    Get monthly financial summary
    
    Query params:
    - year: Year (defaults to current)
    - month: Month (defaults to current)
    """
    try:
        year = request.args.get('year', type=int)
        month = request.args.get('month', type=int)
        
        manager = get_finance_manager()
        summary = manager.get_monthly_summary(year=year, month=month)
        
        return jsonify({
            'success': True,
            'summary': summary
        })
        
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@treasure_ledger_bp.route('/alerts', methods=['GET'])
def get_alerts():
    """
    Get spending alerts
    
    Query params:
    - budget: Monthly budget limit (optional)
    """
    try:
        budget = request.args.get('budget', type=float)
        
        manager = get_finance_manager()
        alerts = manager.get_spending_alerts(budget=budget)
        
        return jsonify({
            'success': True,
            'alerts': alerts
        })
        
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@treasure_ledger_bp.route('/categories', methods=['GET'])
def get_categories():
    """Get available transaction categories"""
    return jsonify({
        'success': True,
        'expense_categories': FinanceManager.EXPENSE_CATEGORIES,
        'income_categories': FinanceManager.INCOME_CATEGORIES
    })
