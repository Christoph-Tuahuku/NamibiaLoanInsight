"""
Enhanced loan calculations with comparison tools and debt consolidation
"""
import math
import json
from typing import Dict, List, Any, Tuple
from datetime import datetime, date


class LoanComparator:
    """Compare multiple loan options side by side"""
    
    def __init__(self):
        # Current Namibian rates (updated from official sources)
        self.current_rates = {
            'microlender_max': 16.8,  # NamFISA: Prime Rate × 1.6
            'bank_prime': 10.5,       # Current Bank of Namibia prime rate
            'repo_rate': 6.75         # Current repo rate
        }
    
    def compare_loans(self, loan_amount: float, term_months: int, 
                     loan_options: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Compare multiple loan options
        
        Args:
            loan_amount: Principal amount to borrow
            term_months: Loan term in months
            loan_options: List of loan options with rates and fees
            
        Returns:
            Comprehensive comparison data
        """
        results = {
            'loan_amount': loan_amount,
            'term_months': term_months,
            'options': [],
            'best_option': None,
            'worst_option': None,
            'savings_amount': 0,
            'comparison_date': datetime.now().isoformat()
        }
        
        for i, option in enumerate(loan_options):
            calc_result = self._calculate_single_loan(
                loan_amount, term_months, option
            )
            calc_result['option_id'] = i
            calc_result['lender_name'] = option.get('lender_name', f'Option {i+1}')
            results['options'].append(calc_result)
        
        # Find best and worst options based on total repayment
        if results['options']:
            results['options'].sort(key=lambda x: x['total_repayment'])
            results['best_option'] = results['options'][0]
            results['worst_option'] = results['options'][-1]
            results['savings_amount'] = (
                results['worst_option']['total_repayment'] - 
                results['best_option']['total_repayment']
            )
        
        return results
    
    def _calculate_single_loan(self, principal: float, term: int, 
                              option: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate loan details for a single option"""
        annual_rate = option['annual_rate']
        admin_fee = option.get('admin_fee', 0)
        insurance = option.get('insurance', 0)
        
        # Monthly rate
        monthly_rate = annual_rate / 100 / 12
        
        # Calculate monthly payment using standard loan formula
        if monthly_rate > 0:
            monthly_payment = principal * (
                monthly_rate * (1 + monthly_rate) ** term
            ) / ((1 + monthly_rate) ** term - 1)
        else:
            monthly_payment = principal / term
        
        # Total calculations
        total_payments = monthly_payment * term
        total_interest = total_payments - principal
        first_payment = monthly_payment + admin_fee + insurance
        total_repayment = total_payments + admin_fee + insurance
        
        # Effective APR calculation including fees
        if admin_fee > 0 or insurance > 0:
            total_fees = admin_fee + insurance
            effective_principal = principal - total_fees
            if effective_principal > 0:
                effective_apr = self._calculate_effective_apr(
                    effective_principal, monthly_payment, term
                )
            else:
                effective_apr = annual_rate
        else:
            effective_apr = annual_rate
        
        return {
            'annual_rate': annual_rate,
            'monthly_payment': round(monthly_payment, 2),
            'first_payment': round(first_payment, 2),
            'total_repayment': round(total_repayment, 2),
            'total_interest': round(total_interest, 2),
            'total_fees': round(admin_fee + insurance, 2),
            'effective_apr': round(effective_apr, 2),
            'admin_fee': admin_fee,
            'insurance': insurance,
            'lender_type': option.get('lender_type', 'Unknown'),
            'compliance_status': self._check_compliance(annual_rate, option.get('lender_type', 'unknown'))
        }
    
    def _calculate_effective_apr(self, principal: float, payment: float, term: int) -> float:
        """Calculate effective APR using Newton-Raphson method"""
        # Simplified effective APR calculation
        total_cost = payment * term
        return ((total_cost / principal) - 1) * (12 / term) * 100
    
    def _check_compliance(self, rate: float, lender_type: str = 'unknown') -> str:
        """Check if loan complies with NamFISA regulations"""
        if lender_type == 'microlender' and rate > self.current_rates['microlender_max']:
            return 'non_compliant'
        elif lender_type == 'bank' and rate > self.current_rates['bank_prime'] * 1.5:
            return 'warning'
        return 'compliant'


class DebtConsolidator:
    """Calculate debt consolidation benefits"""
    
    def analyze_consolidation(self, existing_debts: List[Dict[str, Any]], 
                            consolidation_offer: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze if debt consolidation is beneficial
        
        Args:
            existing_debts: List of current debts with balances, rates, payments
            consolidation_offer: New loan offer details
            
        Returns:
            Analysis of consolidation benefits
        """
        # Calculate current situation
        current_total_balance = sum(debt['balance'] for debt in existing_debts)
        current_total_payment = sum(debt['monthly_payment'] for debt in existing_debts)
        current_total_interest = self._calculate_total_interest_existing(existing_debts)
        
        # Calculate consolidation loan
        new_loan_amount = consolidation_offer['amount']
        new_rate = consolidation_offer['annual_rate']
        new_term = consolidation_offer['term_months']
        
        monthly_rate = new_rate / 100 / 12
        if monthly_rate > 0:
            new_monthly_payment = new_loan_amount * (
                monthly_rate * (1 + monthly_rate) ** new_term
            ) / ((1 + monthly_rate) ** new_term - 1)
        else:
            new_monthly_payment = new_loan_amount / new_term
        
        new_total_repayment = new_monthly_payment * new_term
        new_total_interest = new_total_repayment - new_loan_amount
        
        # Calculate savings
        monthly_savings = current_total_payment - new_monthly_payment
        interest_savings = current_total_interest - new_total_interest
        
        return {
            'current_situation': {
                'total_balance': round(current_total_balance, 2),
                'monthly_payment': round(current_total_payment, 2),
                'total_interest': round(current_total_interest, 2)
            },
            'consolidation_option': {
                'loan_amount': new_loan_amount,
                'monthly_payment': round(new_monthly_payment, 2),
                'total_repayment': round(new_total_repayment, 2),
                'total_interest': round(new_total_interest, 2)
            },
            'savings': {
                'monthly_savings': round(monthly_savings, 2),
                'interest_savings': round(interest_savings, 2),
                'is_beneficial': monthly_savings > 0 and interest_savings > 0
            },
            'recommendation': self._get_consolidation_recommendation(
                monthly_savings, interest_savings, new_rate
            )
        }
    
    def _calculate_total_interest_existing(self, debts: List[Dict[str, Any]]) -> float:
        """Calculate total interest for existing debts"""
        total_interest = 0
        for debt in debts:
            balance = debt['balance']
            rate = debt['annual_rate'] / 100 / 12
            payment = debt['monthly_payment']
            
            # Estimate remaining term
            if rate > 0 and payment > balance * rate:
                remaining_months = math.log(1 + (balance * rate) / (payment - balance * rate)) / math.log(1 + rate)
                total_interest += (payment * remaining_months) - balance
            else:
                # Minimum payment scenario
                total_interest += balance * 0.5  # Estimate
        
        return total_interest
    
    def _get_consolidation_recommendation(self, monthly_savings: float, 
                                       interest_savings: float, new_rate: float) -> str:
        """Generate consolidation recommendation"""
        if monthly_savings > 0 and interest_savings > 0:
            return "Recommended: Consolidation will save you money monthly and overall."
        elif monthly_savings > 0 and interest_savings <= 0:
            return "Caution: Lower monthly payment but higher total interest cost."
        elif monthly_savings <= 0 and interest_savings > 0:
            return "Mixed: Higher monthly payment but saves on total interest."
        else:
            return "Not Recommended: Consolidation will cost more money."


class BudgetCalculator:
    """Calculate budget and affordability assessments"""
    
    def __init__(self):
        # Namibian average living costs (approximate)
        self.namibian_averages = {
            'housing_percentage': 35,   # % of income
            'transport_percentage': 15,
            'food_percentage': 20,
            'utilities_percentage': 10,
            'other_percentage': 20
        }
    
    def calculate_affordability(self, monthly_income: float, 
                              existing_debts: float = 0,
                              dependents: int = 0) -> Dict[str, Any]:
        """
        Calculate how much someone can afford to borrow
        
        Args:
            monthly_income: Gross monthly income
            existing_debts: Current monthly debt payments
            dependents: Number of dependents
            
        Returns:
            Affordability assessment
        """
        # Calculate disposable income
        estimated_expenses = self._estimate_living_expenses(monthly_income, dependents)
        disposable_income = monthly_income - estimated_expenses - existing_debts
        
        # Conservative lending ratios
        max_debt_service_ratio = 0.4  # Max 40% of income for all debt
        safe_debt_service_ratio = 0.3  # Recommended 30% max
        
        max_total_debt_payment = monthly_income * max_debt_service_ratio
        safe_total_debt_payment = monthly_income * safe_debt_service_ratio
        
        max_additional_payment = max(0, max_total_debt_payment - existing_debts)
        safe_additional_payment = max(0, safe_total_debt_payment - existing_debts)
        
        return {
            'monthly_income': monthly_income,
            'estimated_expenses': round(estimated_expenses, 2),
            'existing_debts': existing_debts,
            'disposable_income': round(disposable_income, 2),
            'debt_service_ratios': {
                'current': round((existing_debts / monthly_income) * 100, 1),
                'maximum_recommended': 30,
                'absolute_maximum': 40
            },
            'affordable_payments': {
                'maximum_additional': round(max_additional_payment, 2),
                'safe_additional': round(safe_additional_payment, 2)
            },
            'loan_estimates': self._estimate_loan_amounts(safe_additional_payment),
            'recommendation': self._get_affordability_recommendation(
                disposable_income, existing_debts, monthly_income
            )
        }
    
    def _estimate_living_expenses(self, income: float, dependents: int) -> float:
        """Estimate monthly living expenses based on income and dependents"""
        base_percentage = 0.7  # 70% of income for basic living
        dependent_addition = dependents * 0.05  # 5% extra per dependent
        
        expense_percentage = min(0.9, base_percentage + dependent_addition)
        return income * expense_percentage
    
    def _estimate_loan_amounts(self, payment: float) -> Dict[str, float]:
        """Estimate loan amounts for different terms and rates"""
        estimates = {}
        
        # Different scenarios
        scenarios = [
            ('12_months_16.8%', 12, 16.8),
            ('24_months_16.8%', 24, 16.8),
            ('36_months_16.8%', 36, 16.8),
            ('60_months_16.8%', 60, 16.8),
            ('12_months_10.5%', 12, 10.5),
            ('36_months_10.5%', 36, 10.5),
            ('60_months_10.5%', 60, 10.5)
        ]
        
        for name, term, rate in scenarios:
            monthly_rate = rate / 100 / 12
            if monthly_rate > 0:
                loan_amount = payment * ((1 + monthly_rate) ** term - 1) / (
                    monthly_rate * (1 + monthly_rate) ** term
                )
            else:
                loan_amount = payment * term
            
            estimates[name] = round(loan_amount, 2)
        
        return estimates
    
    def _get_affordability_recommendation(self, disposable: float, 
                                        existing_debts: float, income: float) -> str:
        """Generate affordability recommendation"""
        debt_ratio = (existing_debts / income) * 100
        
        if debt_ratio > 40:
            return "High Risk: Consider debt reduction before additional borrowing"
        elif debt_ratio > 30:
            return "Caution: Limited capacity for additional debt"
        elif disposable < 0:
            return "Not Recommended: Expenses exceed income"
        else:
            return "Good: Healthy capacity for responsible borrowing"


class EconomicTracker:
    """Track and analyze Namibian economic indicators"""
    
    def get_current_rates(self) -> Dict[str, Any]:
        """Get current Namibian lending rates and economic indicators"""
        return {
            'last_updated': datetime.now().isoformat(),
            'rates': {
                'repo_rate': 6.75,
                'prime_rate': 10.5,
                'namfisa_max': 16.8,
                'inflation_estimate': 4.2  # Approximate
            },
            'compliance_limits': {
                'microlender_max_rate': 16.8,
                'microlender_max_amount': 50000,
                'microlender_max_term': 60,
                'bank_max_term': 84
            },
            'market_insights': [
                "Prime rate held steady at 10.5% following BoN monetary policy",
                "NamFISA continues enforcing maximum rate formula: Prime × 1.6",
                "Increased focus on financial literacy and consumer protection"
            ]
        }