import math
from typing import Dict, Any

class LoanCalculator:
    """Handles loan calculations with NamFISA and Bank of Namibia compliance"""
    
    # Official NamFISA regulatory rates (Microlending Act No. 7 of 2018)
    # Maximum annual finance charge = Average Prime Rate × 1.6
    CURRENT_PRIME_RATE = 10.5  # Current prime rate as of 2024/2025
    NAMFISA_MULTIPLIER = 1.6   # Official NamFISA multiplier
    NAMFISA_MAX_APR = CURRENT_PRIME_RATE * NAMFISA_MULTIPLIER  # 16.8% for microlenders
    
    # NamFISA Microlending limits
    MICROLENDER_MAX_AMOUNT = 50000  # Maximum N$50,000 per NamFISA (updated from search)
    MICROLENDER_MAX_TERM = 60       # Maximum 60 months (5 years) per NamFISA
    MICROLENDER_MIN_TERM = 1        # Minimum 1 month
    
    # Bank lending (Bank of Namibia oversight) 
    BANK_PRIME_RATE = 10.5          # Current prime lending rate
    BANK_REPO_RATE = 6.75           # Current repo rate as of June 2025
    BANK_LOAN_MAX_TERM = 84         # Extended terms for bank loans
    BANK_LOAN_MIN_TERM = 1          # Minimum 1 month for bank loans
    
    # Legacy compatibility (keeping original structure for UI)
    CASH_LOAN_MAX_APR = NAMFISA_MAX_APR  # Use official NamFISA rate
    BANK_LOAN_APR = BANK_PRIME_RATE      # Use current prime rate for banks
    CASH_LOAN_MAX_TERM = MICROLENDER_MAX_TERM  # Updated to official limit
    CASH_LOAN_MIN_TERM = MICROLENDER_MIN_TERM
    BANK_LOAN_MAX_TERM = 84
    BANK_LOAN_MIN_TERM = 1
    
    def calculate_loan(self, loan_amount: float, loan_term: int, loan_type: str, 
                      admin_fee: float = 0, insurance: float = 0) -> Dict[str, Any]:
        """
        Calculate loan details with regulatory compliance checks
        
        Args:
            loan_amount: Principal loan amount
            loan_term: Loan term in months
            loan_type: 'cash_loan' or 'bank_loan'
            admin_fee: Optional administration fee
            insurance: Optional insurance cost
            
        Returns:
            Dictionary containing calculation results and compliance warnings
        """
        result = {
            'loan_amount': loan_amount,
            'loan_term': loan_term,
            'loan_type': loan_type,
            'admin_fee': admin_fee,
            'insurance': insurance,
            'warnings': [],
            'compliance_status': 'compliant'
        }
        
        # Validate loan type and set interest rate
        if loan_type == 'cash_loan':
            # Use official NamFISA formula: Prime Rate × 1.6
            annual_rate = self.NAMFISA_MAX_APR
            self._validate_cash_loan_term(loan_term, result)
            self._validate_cash_loan_amount(loan_amount, result)
        elif loan_type == 'bank_loan':
            # Use current prime rate for bank loans
            annual_rate = self.BANK_PRIME_RATE
            self._validate_bank_loan_term(loan_term, result)
        else:
            raise ValueError(f"Invalid loan type: {loan_type}")
        
        # Calculate monthly interest rate
        monthly_rate = annual_rate / 100 / 12
        
        # Calculate monthly payment using standard loan formula
        if monthly_rate > 0:
            monthly_payment = loan_amount * (monthly_rate * (1 + monthly_rate) ** loan_term) / \
                            ((1 + monthly_rate) ** loan_term - 1)
        else:
            monthly_payment = loan_amount / loan_term
        
        # Add admin fee and insurance to first payment if applicable
        first_payment = monthly_payment + admin_fee + insurance
        
        # Calculate totals
        total_repayment = monthly_payment * loan_term + admin_fee + insurance
        total_interest = total_repayment - loan_amount
        effective_apr = self._calculate_effective_apr(loan_amount, monthly_payment, loan_term, admin_fee, insurance)
        
        # Update result
        result.update({
            'annual_rate': annual_rate,
            'monthly_rate': monthly_rate * 100,
            'monthly_payment': round(monthly_payment, 2),
            'first_payment': round(first_payment, 2),
            'total_repayment': round(total_repayment, 2),
            'total_interest': round(total_interest, 2),
            'effective_apr': round(effective_apr, 2)
        })
        
        # Check compliance
        self._check_compliance(result, effective_apr, loan_type)
        
        return result
    
    def _validate_cash_loan_term(self, loan_term: int, result: Dict[str, Any]):
        """Validate cash loan term against NamFISA regulations"""
        if loan_term < self.MICROLENDER_MIN_TERM:
            result['warnings'].append(f"Microlending term must be at least {self.MICROLENDER_MIN_TERM} month(s)")
            result['compliance_status'] = 'non_compliant'
        elif loan_term > self.MICROLENDER_MAX_TERM:
            result['warnings'].append(f"Microlending term exceeds NamFISA maximum of {self.MICROLENDER_MAX_TERM} months")
            result['compliance_status'] = 'non_compliant'
    
    def _validate_cash_loan_amount(self, loan_amount: float, result: Dict[str, Any]):
        """Validate cash loan amount against NamFISA regulations"""
        if loan_amount > self.MICROLENDER_MAX_AMOUNT:
            result['warnings'].append(f"Loan amount exceeds NamFISA maximum of N${self.MICROLENDER_MAX_AMOUNT:,.2f} for microlending")
            result['compliance_status'] = 'non_compliant'
    
    def _validate_bank_loan_term(self, loan_term: int, result: Dict[str, Any]):
        """Validate bank loan term against regulatory limits"""
        if loan_term < self.BANK_LOAN_MIN_TERM:
            result['warnings'].append(f"Bank loan term must be at least {self.BANK_LOAN_MIN_TERM} month(s)")
            result['compliance_status'] = 'non_compliant'
        elif loan_term > self.BANK_LOAN_MAX_TERM:
            result['warnings'].append(f"Bank loan term exceeds regulatory maximum of {self.BANK_LOAN_MAX_TERM} months")
            result['compliance_status'] = 'non_compliant'
    
    def _calculate_effective_apr(self, principal: float, monthly_payment: float, 
                               term: int, admin_fee: float, insurance: float) -> float:
        """Calculate effective APR including all fees"""
        total_payments = monthly_payment * term + admin_fee + insurance
        total_cost = total_payments - principal
        
        if term == 0 or principal == 0:
            return 0
        
        # Simple APR calculation for demonstration
        # In practice, you might want to use a more sophisticated calculation
        return (total_cost / principal) * (12 / term) * 100
    
    def _check_compliance(self, result: Dict[str, Any], effective_apr: float, loan_type: str):
        """Check regulatory compliance and add warnings"""
        if loan_type == 'cash_loan':
            if effective_apr > self.NAMFISA_MAX_APR:
                result['warnings'].append(
                    f"Effective APR ({effective_apr:.2f}%) exceeds NamFISA maximum of {self.NAMFISA_MAX_APR:.2f}% "
                    f"(Prime Rate {self.CURRENT_PRIME_RATE}% × 1.6)"
                )
                result['compliance_status'] = 'non_compliant'
            else:
                result['warnings'].append(
                    f"✓ Complies with NamFISA regulations (Max: {self.NAMFISA_MAX_APR:.2f}% = Prime {self.CURRENT_PRIME_RATE}% × 1.6)"
                )
        elif loan_type == 'bank_loan':
            if effective_apr > self.BANK_PRIME_RATE * 1.5:  # Allow reasonable margin above prime
                result['warnings'].append(
                    f"Effective APR ({effective_apr:.2f}%) is significantly above prime rate ({self.BANK_PRIME_RATE}%)"
                )
                result['compliance_status'] = 'warning'
            else:
                result['warnings'].append(
                    f"✓ Reasonable rate relative to current prime rate ({self.BANK_PRIME_RATE}%)"
                )
        
        # Add regulatory contact information
        if result['compliance_status'] == 'non_compliant':
            result['warnings'].append(
                "⚠️ For regulatory questions, contact NamFISA: (061) 290-5000 or llombardt@namfisa.com.na"
            )


class RiskAnalyzer:
    """Analyzes loan risk based on borrower profile"""
    
    def analyze_risk(self, age: int, monthly_income: float, credit_score: int, 
                    previous_defaults: int, loan_amount: float) -> Dict[str, Any]:
        """
        Analyze loan risk based on borrower information
        
        Args:
            age: Borrower's age
            monthly_income: Monthly income in NAD
            credit_score: Credit score (1-10 scale)
            previous_defaults: Number of previous defaults
            loan_amount: Requested loan amount
            
        Returns:
            Dictionary containing risk assessment and advice
        """
        # Calculate debt-to-income ratio
        debt_to_income_ratio = (loan_amount / 12) / monthly_income * 100  # Assuming 1-year loan for DTI calculation
        
        # Calculate risk score (0-100, higher is riskier)
        risk_score = 0
        
        # Age factor (optimal age range 25-55)
        if age < 25:
            risk_score += 15
        elif age > 55:
            risk_score += 10
        else:
            risk_score += 5
        
        # Income factor
        if monthly_income < 5000:  # Low income
            risk_score += 25
        elif monthly_income < 15000:  # Medium income
            risk_score += 15
        else:  # High income
            risk_score += 5
        
        # Credit score factor (inverted - lower credit score = higher risk)
        risk_score += (11 - credit_score) * 5
        
        # Previous defaults factor
        risk_score += previous_defaults * 15
        
        # Debt-to-income ratio factor
        if debt_to_income_ratio > 40:
            risk_score += 20
        elif debt_to_income_ratio > 30:
            risk_score += 15
        elif debt_to_income_ratio > 20:
            risk_score += 10
        else:
            risk_score += 5
        
        # Determine risk level
        if risk_score <= 30:
            risk_level = "Low"
            risk_color = "success"
        elif risk_score <= 60:
            risk_level = "Medium"
            risk_color = "warning"
        else:
            risk_level = "High"
            risk_color = "danger"
        
        # Generate personalized advice
        advice = self._generate_advice(risk_level, debt_to_income_ratio, credit_score, monthly_income)
        
        # Generate compliance tips
        compliance_tips = self._generate_compliance_tips(risk_level, loan_amount)
        
        return {
            'age': age,
            'monthly_income': monthly_income,
            'credit_score': credit_score,
            'previous_defaults': previous_defaults,
            'loan_amount': loan_amount,
            'debt_to_income_ratio': round(debt_to_income_ratio, 2),
            'risk_score': risk_score,
            'risk_level': risk_level,
            'risk_color': risk_color,
            'advice': advice,
            'compliance_tips': compliance_tips
        }
    
    def _generate_advice(self, risk_level: str, dti_ratio: float, credit_score: int, income: float) -> list:
        """Generate personalized repayment advice"""
        advice = []
        
        if risk_level == "High":
            advice.append("Consider reducing the loan amount or extending the repayment period")
            advice.append("Build your credit score before applying for large loans")
            advice.append("Ensure you have emergency savings before taking on debt")
        
        if dti_ratio > 30:
            advice.append(f"Your debt-to-income ratio ({dti_ratio:.1f}%) is high. Consider a smaller loan amount")
        
        if credit_score < 5:
            advice.append("Work on improving your credit score by paying bills on time and reducing existing debt")
        
        if income < 10000:
            advice.append("Consider increasing your income or applying for a smaller loan amount")
        
        # General advice
        advice.append("Create a detailed budget to ensure you can meet monthly payments")
        advice.append("Compare offers from multiple NamFISA-regulated lenders")
        advice.append("Read all loan terms carefully before signing")
        
        return advice
    
    def _generate_compliance_tips(self, risk_level: str, loan_amount: float) -> list:
        """Generate compliance and regulatory tips"""
        tips = []
        
        tips.append("Ensure your lender is registered with NamFISA")
        tips.append("Check that interest rates comply with Bank of Namibia regulations")
        tips.append("Request a clear breakdown of all fees and charges")
        tips.append("Understand your rights under the Credit Agreements Act")
        
        if risk_level == "High":
            tips.append("Consider credit counseling services before proceeding")
            tips.append("Explore alternative financing options")
        
        if loan_amount > 50000:
            tips.append("For large loans, consider consulting with a financial advisor")
            tips.append("Ensure adequate insurance coverage for loan protection")
        
        return tips
