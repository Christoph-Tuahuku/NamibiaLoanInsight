from flask import render_template, request, flash, redirect, url_for, jsonify
from app import app, db
from calculations import LoanCalculator, RiskAnalyzer
from enhanced_calculations import LoanComparator, DebtConsolidator, BudgetCalculator, EconomicTracker
from models import (RegisteredLender, LenderReview, FraudAlert, FinancialTip, 
                   ComparisonHistory, BudgetEntry, LoanApplication)
import json
import logging
from datetime import datetime

@app.route('/')
def index():
    """Home page with introduction and regulatory information"""
    return render_template('index.html')

@app.route('/loan-calculator', methods=['GET', 'POST'])
def loan_calculator():
    """Loan calculator page with NamFISA/BoN compliance"""
    if request.method == 'POST':
        try:
            # Get form data
            loan_amount = float(request.form.get('loan_amount', 0))
            loan_term = int(request.form.get('loan_term', 0))
            loan_type = request.form.get('loan_type', '')
            admin_fee = float(request.form.get('admin_fee', 0))
            insurance = float(request.form.get('insurance', 0))
            
            # Validate inputs
            if loan_amount <= 0:
                flash('Please enter a valid loan amount', 'error')
                return render_template('loan_calculator.html')
            
            if loan_term <= 0:
                flash('Please enter a valid loan term', 'error')
                return render_template('loan_calculator.html')
            
            if loan_type not in ['cash_loan', 'bank_loan']:
                flash('Please select a valid loan type', 'error')
                return render_template('loan_calculator.html')
            
            # Calculate loan details
            calculator = LoanCalculator()
            result = calculator.calculate_loan(
                loan_amount=loan_amount,
                loan_term=loan_term,
                loan_type=loan_type,
                admin_fee=admin_fee,
                insurance=insurance
            )
            
            return render_template('loan_calculator.html', result=result)
            
        except ValueError as e:
            flash('Please enter valid numeric values', 'error')
            logging.error(f"Loan calculation error: {e}")
            return render_template('loan_calculator.html')
        except Exception as e:
            flash('An error occurred during calculation. Please try again.', 'error')
            logging.error(f"Unexpected error in loan calculation: {e}")
            return render_template('loan_calculator.html')
    
    return render_template('loan_calculator.html')

@app.route('/risk-analyzer', methods=['GET', 'POST'])
def risk_analyzer():
    """Risk analysis page for loan assessment"""
    if request.method == 'POST':
        try:
            # Get form data
            age = int(request.form.get('age', 0))
            monthly_income = float(request.form.get('monthly_income', 0))
            credit_score = int(request.form.get('credit_score', 0))
            previous_defaults = int(request.form.get('previous_defaults', 0))
            loan_amount = float(request.form.get('loan_amount', 0))
            
            # Validate inputs
            if age < 18 or age > 100:
                flash('Please enter a valid age (18-100)', 'error')
                return render_template('risk_analyzer.html')
            
            if monthly_income <= 0:
                flash('Please enter a valid monthly income', 'error')
                return render_template('risk_analyzer.html')
            
            if credit_score < 1 or credit_score > 10:
                flash('Please enter a credit score between 1 and 10', 'error')
                return render_template('risk_analyzer.html')
            
            if loan_amount <= 0:
                flash('Please enter a valid loan amount', 'error')
                return render_template('risk_analyzer.html')
            
            # Perform risk analysis
            analyzer = RiskAnalyzer()
            result = analyzer.analyze_risk(
                age=age,
                monthly_income=monthly_income,
                credit_score=credit_score,
                previous_defaults=previous_defaults,
                loan_amount=loan_amount
            )
            
            return render_template('risk_analyzer.html', result=result)
            
        except ValueError as e:
            flash('Please enter valid numeric values', 'error')
            logging.error(f"Risk analysis error: {e}")
            return render_template('risk_analyzer.html')
        except Exception as e:
            flash('An error occurred during analysis. Please try again.', 'error')
            logging.error(f"Unexpected error in risk analysis: {e}")
            return render_template('risk_analyzer.html')
    
    return render_template('risk_analyzer.html')

@app.route('/about')
def about():
    """About us page"""
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact form page"""
    if request.method == 'POST':
        try:
            name = request.form.get('name', '').strip()
            email = request.form.get('email', '').strip()
            message = request.form.get('message', '').strip()
            
            # Basic validation
            if not name:
                flash('Please enter your name', 'error')
                return render_template('contact.html')
            
            if not email or '@' not in email:
                flash('Please enter a valid email address', 'error')
                return render_template('contact.html')
            
            if not message:
                flash('Please enter a message', 'error')
                return render_template('contact.html')
            
            # In a real application, you would send the email here
            # For now, we'll just log it and show a success message
            logging.info(f"Contact form submission - Name: {name}, Email: {email}, Message: {message}")
            flash('Thank you for your message! We will get back to you soon.', 'success')
            return redirect(url_for('contact'))
            
        except Exception as e:
            flash('An error occurred. Please try again.', 'error')
            logging.error(f"Contact form error: {e}")
            return render_template('contact.html')
    
    return render_template('contact.html')


@app.route('/loan-comparison', methods=['GET', 'POST'])
def loan_comparison():
    """Compare multiple loan options side by side"""
    if request.method == 'POST':
        try:
            loan_amount = float(request.form.get('loan_amount', 0))
            loan_term = int(request.form.get('loan_term', 0))
            
            # Collect loan options
            loan_options = []
            for i in range(3):  # Support up to 3 options
                lender_name = request.form.get(f'lender_name_{i}', '').strip()
                lender_type = request.form.get(f'lender_type_{i}', '')
                annual_rate = request.form.get(f'annual_rate_{i}', '')
                admin_fee = request.form.get(f'admin_fee_{i}', '0')
                insurance = request.form.get(f'insurance_{i}', '0')
                
                if lender_name and annual_rate:
                    loan_options.append({
                        'lender_name': lender_name,
                        'lender_type': lender_type,
                        'annual_rate': float(annual_rate),
                        'admin_fee': float(admin_fee),
                        'insurance': float(insurance)
                    })
            
            if len(loan_options) < 2:
                flash('Please enter at least 2 loan options to compare', 'error')
                return render_template('loan_comparison.html')
            
            # Perform comparison
            comparator = LoanComparator()
            comparison_result = comparator.compare_loans(loan_amount, loan_term, loan_options)
            
            # Save comparison history
            comparison_data = json.dumps(comparison_result, default=str)
            history = ComparisonHistory()
            history.comparison_data = comparison_data
            history.loan_amount = loan_amount
            history.loan_term = loan_term
            history.best_option = comparison_result['best_option']['lender_name']
            history.potential_savings = comparison_result['savings_amount']
            db.session.add(history)
            db.session.commit()
            
            return render_template('loan_comparison.html', comparison_result=comparison_result)
            
        except ValueError as e:
            flash('Please enter valid numeric values', 'error')
            return render_template('loan_comparison.html')
        except Exception as e:
            flash('An error occurred during comparison. Please try again.', 'error')
            logging.error(f"Loan comparison error: {e}")
            return render_template('loan_comparison.html')
    
    return render_template('loan_comparison.html')


@app.route('/budget-planner', methods=['GET', 'POST'])
def budget_planner():
    """Budget planning and affordability calculator"""
    if request.method == 'POST':
        try:
            monthly_income = float(request.form.get('monthly_income', 0))
            dependents = int(request.form.get('dependents', 0))
            existing_debt_payments = float(request.form.get('existing_debt_payments', 0))
            credit_cards = float(request.form.get('credit_cards', 0))
            
            # Optional detailed expenses
            housing = float(request.form.get('housing', 0))
            transport = float(request.form.get('transport', 0))
            food_groceries = float(request.form.get('food_groceries', 0))
            utilities = float(request.form.get('utilities', 0))
            medical = float(request.form.get('medical', 0))
            other_expenses = float(request.form.get('other_expenses', 0))
            
            total_existing_debts = existing_debt_payments + credit_cards
            
            # Calculate affordability
            budget_calc = BudgetCalculator()
            budget_result = budget_calc.calculate_affordability(
                monthly_income=monthly_income,
                existing_debts=total_existing_debts,
                dependents=dependents
            )
            
            return render_template('budget_planner.html', budget_result=budget_result)
            
        except ValueError as e:
            flash('Please enter valid numeric values', 'error')
            return render_template('budget_planner.html')
        except Exception as e:
            flash('An error occurred during budget calculation. Please try again.', 'error')
            logging.error(f"Budget planning error: {e}")
            return render_template('budget_planner.html')
    
    return render_template('budget_planner.html')


@app.route('/debt-consolidation', methods=['GET', 'POST'])
def debt_consolidation():
    """Debt consolidation analysis"""
    if request.method == 'POST':
        try:
            # Collect existing debts
            existing_debts = []
            i = 0
            while True:
                debt_name = request.form.get(f'debt_name_{i}', '').strip()
                debt_balance = request.form.get(f'debt_balance_{i}', '')
                debt_rate = request.form.get(f'debt_rate_{i}', '')
                debt_payment = request.form.get(f'debt_payment_{i}', '')
                
                if not debt_name and not debt_balance:
                    break
                
                if debt_balance and debt_rate and debt_payment:
                    existing_debts.append({
                        'name': debt_name,
                        'balance': float(debt_balance),
                        'annual_rate': float(debt_rate),
                        'monthly_payment': float(debt_payment)
                    })
                i += 1
            
            # Consolidation loan details
            consolidation_amount = float(request.form.get('consolidation_amount', 0))
            consolidation_rate = float(request.form.get('consolidation_rate', 0))
            consolidation_term = int(request.form.get('consolidation_term', 0))
            consolidation_fees = float(request.form.get('consolidation_fees', 0))
            
            if not existing_debts:
                flash('Please enter at least one existing debt', 'error')
                return render_template('debt_consolidation.html')
            
            consolidation_offer = {
                'amount': consolidation_amount,
                'annual_rate': consolidation_rate,
                'term_months': consolidation_term,
                'fees': consolidation_fees
            }
            
            # Analyze consolidation
            consolidator = DebtConsolidator()
            consolidation_result = consolidator.analyze_consolidation(existing_debts, consolidation_offer)
            
            return render_template('debt_consolidation.html', consolidation_result=consolidation_result)
            
        except ValueError as e:
            flash('Please enter valid numeric values', 'error')
            return render_template('debt_consolidation.html')
        except Exception as e:
            flash('An error occurred during consolidation analysis. Please try again.', 'error')
            logging.error(f"Debt consolidation error: {e}")
            return render_template('debt_consolidation.html')
    
    return render_template('debt_consolidation.html')


@app.route('/lender-directory')
def lender_directory():
    """Directory of NamFISA registered lenders"""
    search = request.args.get('search', '')
    lender_type = request.args.get('lender_type', '')
    location = request.args.get('location', '')
    
    # Build query
    query = RegisteredLender.query.filter(RegisteredLender.is_active == True)
    
    if search:
        query = query.filter(
            (RegisteredLender.name.contains(search)) |
            (RegisteredLender.license_number.contains(search))
        )
    
    if lender_type:
        query = query.filter(RegisteredLender.lender_type == lender_type)
    
    lenders = query.all()
    
    return render_template('lender_directory.html', lenders=lenders)


@app.route('/financial-literacy')
def financial_literacy():
    """Financial literacy and education hub"""
    # Get featured tips
    featured_tips = FinancialTip.query.filter(FinancialTip.is_featured == True).limit(5).all()
    
    # Get fraud alerts
    active_alerts = FraudAlert.query.filter(
        FraudAlert.is_active == True,
        (FraudAlert.expires_at.is_(None)) | (FraudAlert.expires_at > datetime.utcnow())
    ).order_by(FraudAlert.severity.desc()).limit(3).all()
    
    return render_template('financial_literacy.html', 
                         featured_tips=featured_tips, 
                         fraud_alerts=active_alerts)


@app.route('/fraud-protection')
def fraud_protection():
    """Fraud protection and awareness center"""
    # Get active fraud alerts
    active_alerts = FraudAlert.query.filter(
        FraudAlert.is_active == True,
        (FraudAlert.expires_at.is_(None)) | (FraudAlert.expires_at > datetime.utcnow())
    ).order_by(FraudAlert.created_at.desc()).limit(10).all()
    
    return render_template('fraud_protection.html', fraud_alerts=active_alerts)


@app.route('/api/economic-indicators')
def api_economic_indicators():
    """API endpoint for current economic indicators"""
    tracker = EconomicTracker()
    indicators = tracker.get_current_rates()
    return jsonify(indicators)


# Seed some sample data for demonstration
@app.route('/seed-data')
def seed_data():
    """Seed the database with sample lenders and content (development only)"""
    try:
        # Sample lenders
        lenders_data = [
            {
                'name': 'First National Bank Namibia',
                'license_number': 'BK001',
                'lender_type': 'bank',
                'contact_phone': '+264 61 299 2222',
                'contact_email': 'info@fnbnamibia.com.na',
                'website': 'https://www.fnbnamibia.com.na',
                'current_rates_min': 8.5,
                'current_rates_max': 15.5,
                'max_loan_amount': 500000,
                'max_term_months': 84
            },
            {
                'name': 'Capricorn Investment Holdings',
                'license_number': 'BK002',
                'lender_type': 'bank',
                'contact_phone': '+264 61 299 1200',
                'contact_email': 'info@capricorn.com.na',
                'website': 'https://www.capricorn.com.na',
                'current_rates_min': 9.0,
                'current_rates_max': 16.0,
                'max_loan_amount': 400000,
                'max_term_months': 72
            },
            {
                'name': 'African Finance Corporation',
                'license_number': 'ML001',
                'lender_type': 'microlender',
                'contact_phone': '+264 61 123 4567',
                'contact_email': 'loans@afc.com.na',
                'current_rates_min': 14.0,
                'current_rates_max': 16.8,
                'max_loan_amount': 50000,
                'max_term_months': 60
            }
        ]
        
        for lender_data in lenders_data:
            existing = RegisteredLender.query.filter_by(license_number=lender_data['license_number']).first()
            if not existing:
                lender = RegisteredLender(**lender_data)
                db.session.add(lender)
        
        # Sample fraud alerts
        fraud_alerts = [
            {
                'alert_type': 'scam_warning',
                'title': 'WhatsApp Loan Scam Alert',
                'description': 'Fraudsters using WhatsApp to offer instant loans requiring upfront payments. Never pay before loan approval.',
                'severity': 'high'
            },
            {
                'alert_type': 'fake_lender',
                'title': 'Fake NamFISA Documents',
                'description': 'Be aware of fake NamFISA registration certificates. Always verify license numbers on the official website.',
                'severity': 'medium'
            }
        ]
        
        for alert_data in fraud_alerts:
            existing = FraudAlert.query.filter_by(title=alert_data['title']).first()
            if not existing:
                alert = FraudAlert(**alert_data)
                db.session.add(alert)
        
        # Sample financial tips
        financial_tips = [
            {
                'category': 'budgeting',
                'title': 'The 50/30/20 Rule',
                'content': 'Allocate 50% of income to needs, 30% to wants, and 20% to savings and debt repayment.',
                'is_featured': True
            },
            {
                'category': 'saving',
                'title': 'Emergency Fund Basics',
                'content': 'Build an emergency fund covering 3-6 months of expenses before taking on additional debt.',
                'is_featured': True
            }
        ]
        
        for tip_data in financial_tips:
            existing = FinancialTip.query.filter_by(title=tip_data['title']).first()
            if not existing:
                tip = FinancialTip(**tip_data)
                db.session.add(tip)
        
        db.session.commit()
        flash('Sample data seeded successfully!', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error seeding data: {str(e)}', 'error')
        logging.error(f"Database seeding error: {e}")
    
    return redirect(url_for('index'))
