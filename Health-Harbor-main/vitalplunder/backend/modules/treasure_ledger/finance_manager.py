"""
Treasure Ledger - Finance Manager
=================================
Handles personal finance tracking with income/expense management.

Author: VitalPlunder Team
"""

import os
import csv
import json
from datetime import datetime, timedelta
from collections import defaultdict

class FinanceManager:
    """
    Manages personal finance transactions.
    Uses CSV storage for simplicity (hackathon-ready).
    """
    
    # Expense categories
    EXPENSE_CATEGORIES = [
        'food', 'transport', 'utilities', 'entertainment', 
        'health', 'shopping', 'education', 'other'
    ]
    
    # Income categories
    INCOME_CATEGORIES = [
        'salary', 'freelance', 'investment', 'gift', 'refund', 'other'
    ]
    
    def __init__(self):
        self.data_dir = os.path.dirname(os.path.abspath(__file__))
        self.csv_file = os.path.join(self.data_dir, 'transactions.csv')
        self._ensure_csv_exists()
    
    def _ensure_csv_exists(self):
        """Create CSV file with headers if it doesn't exist"""
        if not os.path.exists(self.csv_file):
            with open(self.csv_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['id', 'type', 'amount', 'category', 'description', 'date', 'created_at'])
    
    def _read_transactions(self):
        """Read all transactions from CSV"""
        transactions = []
        try:
            with open(self.csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    row['amount'] = float(row['amount'])
                    transactions.append(row)
        except FileNotFoundError:
            self._ensure_csv_exists()
        return transactions
    
    def _write_transaction(self, transaction):
        """Append a transaction to CSV"""
        with open(self.csv_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                transaction['id'],
                transaction['type'],
                transaction['amount'],
                transaction['category'],
                transaction['description'],
                transaction['date'],
                transaction['created_at']
            ])
    
    def add_transaction(self, trans_type, amount, category, description='', date=None):
        """
        Add a new transaction (income or expense)
        
        Args:
            trans_type: 'income' or 'expense'
            amount: Transaction amount (positive number)
            category: Category of transaction
            description: Optional description
            date: Transaction date (defaults to today)
            
        Returns:
            dict: Created transaction
        """
        if trans_type not in ['income', 'expense']:
            raise ValueError("Type must be 'income' or 'expense'")
        
        if amount <= 0:
            raise ValueError("Amount must be positive")
        
        # Validate category
        valid_categories = self.INCOME_CATEGORIES if trans_type == 'income' else self.EXPENSE_CATEGORIES
        if category not in valid_categories:
            category = 'other'
        
        transaction = {
            'id': datetime.now().strftime('%Y%m%d%H%M%S%f'),
            'type': trans_type,
            'amount': float(amount),
            'category': category,
            'description': description or '',
            'date': date or datetime.now().strftime('%Y-%m-%d'),
            'created_at': datetime.now().isoformat()
        }
        
        self._write_transaction(transaction)
        return transaction
    
    def get_transactions(self, start_date=None, end_date=None, trans_type=None):
        """
        Get transactions with optional filters
        
        Args:
            start_date: Filter from this date
            end_date: Filter until this date
            trans_type: Filter by 'income' or 'expense'
            
        Returns:
            list: Filtered transactions
        """
        transactions = self._read_transactions()
        
        if trans_type:
            transactions = [t for t in transactions if t['type'] == trans_type]
        
        if start_date:
            transactions = [t for t in transactions if t['date'] >= start_date]
        
        if end_date:
            transactions = [t for t in transactions if t['date'] <= end_date]
        
        return sorted(transactions, key=lambda x: x['date'], reverse=True)
    
    def get_monthly_summary(self, year=None, month=None):
        """
        Get financial summary for a specific month
        
        Args:
            year: Year (defaults to current)
            month: Month (defaults to current)
            
        Returns:
            dict: Monthly summary with totals and breakdown
        """
        now = datetime.now()
        year = year or now.year
        month = month or now.month
        
        # Calculate date range
        start_date = f"{year}-{month:02d}-01"
        if month == 12:
            end_date = f"{year + 1}-01-01"
        else:
            end_date = f"{year}-{month + 1:02d}-01"
        
        transactions = self._read_transactions()
        monthly = [t for t in transactions if start_date <= t['date'] < end_date]
        
        # Calculate totals
        total_income = sum(t['amount'] for t in monthly if t['type'] == 'income')
        total_expense = sum(t['amount'] for t in monthly if t['type'] == 'expense')
        
        # Category breakdown
        expense_by_category = defaultdict(float)
        income_by_category = defaultdict(float)
        
        for t in monthly:
            if t['type'] == 'expense':
                expense_by_category[t['category']] += t['amount']
            else:
                income_by_category[t['category']] += t['amount']
        
        # TODO: Add ML-based spending prediction
        # TODO: Add anomaly detection for unusual expenses
        
        return {
            'year': year,
            'month': month,
            'total_income': total_income,
            'total_expense': total_expense,
            'balance': total_income - total_expense,
            'savings_rate': (total_income - total_expense) / total_income * 100 if total_income > 0 else 0,
            'expense_breakdown': dict(expense_by_category),
            'income_breakdown': dict(income_by_category),
            'transaction_count': len(monthly)
        }
    
    def get_spending_alerts(self, budget=None):
        """
        Check for spending alerts based on thresholds
        
        Args:
            budget: Optional monthly budget limit
            
        Returns:
            list: Alert messages
        """
        summary = self.get_monthly_summary()
        alerts = []
        
        # Budget alert
        if budget and summary['total_expense'] > budget:
            alerts.append({
                'type': 'over_budget',
                'severity': 'high',
                'message': f"⚠️ You've exceeded your budget! Spent ${summary['total_expense']:.2f} of ${budget:.2f}"
            })
        elif budget and summary['total_expense'] > budget * 0.8:
            alerts.append({
                'type': 'near_budget',
                'severity': 'medium',
                'message': f"⚡ You're at {summary['total_expense']/budget*100:.0f}% of your budget"
            })
        
        # Category alerts (if any category exceeds 40% of total)
        for category, amount in summary['expense_breakdown'].items():
            if summary['total_expense'] > 0:
                percentage = amount / summary['total_expense'] * 100
                if percentage > 40:
                    alerts.append({
                        'type': 'category_high',
                        'severity': 'medium',
                        'message': f"📊 {category.title()} spending is {percentage:.0f}% of total expenses"
                    })
        
        # TODO: Add ML-based anomaly detection alerts
        
        return alerts


# Singleton instance
_finance_manager = None

def get_finance_manager():
    global _finance_manager
    if _finance_manager is None:
        _finance_manager = FinanceManager()
    return _finance_manager
