from datetime import datetime
from app import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    """User model for loan application tracking and preferences"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    loan_applications = db.relationship('LoanApplication', backref='applicant', lazy=True)
    budget_entries = db.relationship('BudgetEntry', backref='user', lazy=True)
    lender_reviews = db.relationship('LenderReview', backref='reviewer', lazy=True)


class LoanApplication(db.Model):
    """Track user loan applications across different lenders"""
    __tablename__ = 'loan_applications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    lender_name = db.Column(db.String(100), nullable=False)
    loan_amount = db.Column(db.Float, nullable=False)
    loan_type = db.Column(db.String(50), nullable=False)  # 'cash_loan', 'bank_loan', 'vehicle', 'home'
    status = db.Column(db.String(30), default='pending')  # 'pending', 'approved', 'rejected', 'withdrawn'
    interest_rate = db.Column(db.Float)
    term_months = db.Column(db.Integer)
    monthly_payment = db.Column(db.Float)
    application_date = db.Column(db.DateTime, default=datetime.utcnow)
    decision_date = db.Column(db.DateTime)
    notes = db.Column(db.Text)


class RegisteredLender(db.Model):
    """NamFISA registered lenders directory"""
    __tablename__ = 'registered_lenders'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    license_number = db.Column(db.String(50), unique=True, nullable=False)
    lender_type = db.Column(db.String(30), nullable=False)  # 'microlender', 'bank', 'credit_provider'
    contact_phone = db.Column(db.String(20))
    contact_email = db.Column(db.String(120))
    physical_address = db.Column(db.Text)
    website = db.Column(db.String(200))
    current_rates_min = db.Column(db.Float)  # Minimum rate offered
    current_rates_max = db.Column(db.Float)  # Maximum rate offered
    max_loan_amount = db.Column(db.Float)
    max_term_months = db.Column(db.Integer)
    is_active = db.Column(db.Boolean, default=True)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    reviews = db.relationship('LenderReview', backref='lender', lazy=True)


class LenderReview(db.Model):
    """User reviews and ratings for lenders"""
    __tablename__ = 'lender_reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    lender_id = db.Column(db.Integer, db.ForeignKey('registered_lenders.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
    review_text = db.Column(db.Text)
    loan_experience = db.Column(db.String(30))  # 'approved', 'rejected', 'processing'
    processing_time_days = db.Column(db.Integer)
    customer_service_rating = db.Column(db.Integer)  # 1-5 stars
    transparency_rating = db.Column(db.Integer)  # 1-5 stars
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_verified = db.Column(db.Boolean, default=False)


class BudgetEntry(db.Model):
    """User budget tracking entries"""
    __tablename__ = 'budget_entries'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # 'income', 'housing', 'transport', 'food', etc.
    subcategory = db.Column(db.String(50))
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200))
    date = db.Column(db.Date, nullable=False)
    is_recurring = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class EconomicIndicator(db.Model):
    """Track Namibian economic indicators"""
    __tablename__ = 'economic_indicators'
    
    id = db.Column(db.Integer, primary_key=True)
    indicator_name = db.Column(db.String(50), nullable=False)  # 'repo_rate', 'prime_rate', 'inflation', etc.
    value = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)
    source = db.Column(db.String(100))  # 'Bank of Namibia', 'NamFISA', etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class FraudAlert(db.Model):
    """Fraud alerts and warnings"""
    __tablename__ = 'fraud_alerts'
    
    id = db.Column(db.Integer, primary_key=True)
    alert_type = db.Column(db.String(30), nullable=False)  # 'scam_warning', 'fake_lender', 'phishing'
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    severity = db.Column(db.String(20), default='medium')  # 'low', 'medium', 'high', 'critical'
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime)


class FinancialTip(db.Model):
    """Financial literacy tips and educational content"""
    __tablename__ = 'financial_tips'
    
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)  # 'budgeting', 'saving', 'borrowing', 'investing'
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    difficulty_level = db.Column(db.String(20), default='beginner')  # 'beginner', 'intermediate', 'advanced'
    language = db.Column(db.String(10), default='en')  # 'en', 'af', 'oshiwambo', etc.
    is_featured = db.Column(db.Boolean, default=False)
    views = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class ComparisonHistory(db.Model):
    """Save loan comparison results for users"""
    __tablename__ = 'comparison_history'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # Nullable for anonymous users
    comparison_data = db.Column(db.Text)  # JSON string of comparison results
    loan_amount = db.Column(db.Float, nullable=False)
    loan_term = db.Column(db.Integer, nullable=False)
    best_option = db.Column(db.String(100))  # Name of recommended lender/option
    potential_savings = db.Column(db.Float)  # Amount saved vs worst option
    created_at = db.Column(db.DateTime, default=datetime.utcnow)