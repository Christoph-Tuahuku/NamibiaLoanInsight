// Namibia Loan Insight - Loan Calculator JavaScript
document.addEventListener('DOMContentLoaded', function() {
    const loanForm = document.getElementById('loanForm');
    const loanTypeSelect = document.getElementById('loan_type');
    const loanTermInput = document.getElementById('loan_term');
    const loanAmountInput = document.getElementById('loan_amount');
    
    // Loan type constraints (updated with official NamFISA rates)
    const LOAN_CONSTRAINTS = {
        cash_loan: {
            maxTerm: 60,
            minTerm: 1,
            maxAPR: 16.8,  // NamFISA: Prime Rate (10.5%) × 1.6
            maxAmount: 50000,
            name: 'Microlender/Cash Loan'
        },
        bank_loan: {
            maxTerm: 84,
            minTerm: 1,
            maxAPR: 10.5,  // Current prime rate
            name: 'Bank Loan'
        }
    };

    // Update term limits based on loan type
    function updateTermLimits() {
        const selectedType = loanTypeSelect.value;
        if (selectedType && LOAN_CONSTRAINTS[selectedType]) {
            const constraints = LOAN_CONSTRAINTS[selectedType];
            loanTermInput.max = constraints.maxTerm;
            loanTermInput.min = constraints.minTerm;
            
            // Update placeholder text
            loanTermInput.placeholder = `${constraints.minTerm}-${constraints.maxTerm} months`;
            
            // Validate current value
            const currentTerm = parseInt(loanTermInput.value);
            if (currentTerm > constraints.maxTerm) {
                loanTermInput.value = constraints.maxTerm;
                showValidationMessage(`Maximum term for ${constraints.name} is ${constraints.maxTerm} months`, 'warning');
            } else if (currentTerm < constraints.minTerm && currentTerm > 0) {
                loanTermInput.value = constraints.minTerm;
                showValidationMessage(`Minimum term for ${constraints.name} is ${constraints.minTerm} month(s)`, 'warning');
            }
        }
    }

    // Show validation messages
    function showValidationMessage(message, type = 'info') {
        // Remove existing validation messages
        const existingAlerts = document.querySelectorAll('.validation-alert');
        existingAlerts.forEach(alert => alert.remove());
        
        // Create new alert
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show validation-alert mt-3`;
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        // Insert after the form
        loanForm.parentNode.insertBefore(alertDiv, loanForm.nextSibling);
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 5000);
    }

    // Validate form inputs
    function validateForm() {
        const loanAmount = parseFloat(loanAmountInput.value);
        const loanTerm = parseInt(loanTermInput.value);
        const loanType = loanTypeSelect.value;
        
        let isValid = true;
        let messages = [];
        
        // Basic validation
        if (!loanAmount || loanAmount <= 0) {
            messages.push('Please enter a valid loan amount');
            isValid = false;
        }
        
        if (!loanTerm || loanTerm <= 0) {
            messages.push('Please enter a valid loan term');
            isValid = false;
        }
        
        if (!loanType) {
            messages.push('Please select a loan type');
            isValid = false;
        }
        
        // Loan type specific validation
        if (loanType && LOAN_CONSTRAINTS[loanType]) {
            const constraints = LOAN_CONSTRAINTS[loanType];
            
            if (loanTerm > constraints.maxTerm) {
                messages.push(`${constraints.name} maximum term is ${constraints.maxTerm} months`);
                isValid = false;
            }
            
            if (loanTerm < constraints.minTerm) {
                messages.push(`${constraints.name} minimum term is ${constraints.minTerm} month(s)`);
                isValid = false;
            }
        }
        
        // Amount validation (basic checks)
        if (loanAmount > 1000000) {
            messages.push('Loan amount seems unusually high. Please verify.');
        }
        
        if (loanAmount < 100 && loanType === 'bank_loan') {
            messages.push('Bank loans typically have minimum amounts. Please check with your lender.');
        }
        
        // Show validation messages
        if (messages.length > 0) {
            const messageType = isValid ? 'warning' : 'danger';
            showValidationMessage(messages.join('<br>'), messageType);
        }
        
        return isValid;
    }

    // Real-time calculation preview (optional enhancement)
    function calculatePreview() {
        const loanAmount = parseFloat(loanAmountInput.value);
        const loanTerm = parseInt(loanTermInput.value);
        const loanType = loanTypeSelect.value;
        const adminFee = parseFloat(document.getElementById('admin_fee').value) || 0;
        const insurance = parseFloat(document.getElementById('insurance').value) || 0;
        
        if (loanAmount && loanTerm && loanType && LOAN_CONSTRAINTS[loanType]) {
            const constraints = LOAN_CONSTRAINTS[loanType];
            const annualRate = constraints.maxAPR;
            const monthlyRate = annualRate / 100 / 12;
            
            let monthlyPayment;
            if (monthlyRate > 0) {
                monthlyPayment = loanAmount * (monthlyRate * Math.pow(1 + monthlyRate, loanTerm)) / 
                               (Math.pow(1 + monthlyRate, loanTerm) - 1);
            } else {
                monthlyPayment = loanAmount / loanTerm;
            }
            
            const totalRepayment = monthlyPayment * loanTerm + adminFee + insurance;
            const totalInterest = totalRepayment - loanAmount;
            
            // Show preview (you could add a preview section to the form)
            updatePreviewDisplay({
                monthlyPayment: monthlyPayment,
                totalRepayment: totalRepayment,
                totalInterest: totalInterest
            });
        }
    }

    // Update preview display (if preview section exists)
    function updatePreviewDisplay(calculations) {
        const previewSection = document.getElementById('calculationPreview');
        if (previewSection) {
            previewSection.innerHTML = `
                <div class="card bg-dark border-info mt-3">
                    <div class="card-header bg-info text-white">
                        <small>Quick Preview</small>
                    </div>
                    <div class="card-body">
                        <div class="row text-center">
                            <div class="col-4">
                                <small class="text-muted">Monthly Payment</small>
                                <div class="text-primary">N$ ${calculations.monthlyPayment.toFixed(2)}</div>
                            </div>
                            <div class="col-4">
                                <small class="text-muted">Total Repayment</small>
                                <div class="text-primary">N$ ${calculations.totalRepayment.toFixed(2)}</div>
                            </div>
                            <div class="col-4">
                                <small class="text-muted">Total Interest</small>
                                <div class="text-primary">N$ ${calculations.totalInterest.toFixed(2)}</div>
                            </div>
                        </div>
                    </div>
                </div>
            `;
        }
    }

    // Format currency inputs
    function formatCurrencyInput(input) {
        let value = input.value.replace(/[^\d.]/g, '');
        if (value.includes('.')) {
            const parts = value.split('.');
            value = parts[0] + '.' + parts[1].substring(0, 2);
        }
        input.value = value;
    }

    // Event listeners
    loanTypeSelect.addEventListener('change', updateTermLimits);
    
    loanTermInput.addEventListener('blur', function() {
        if (loanTypeSelect.value) {
            updateTermLimits();
        }
    });
    
    // Currency formatting for amount inputs
    [loanAmountInput, document.getElementById('admin_fee'), document.getElementById('insurance')].forEach(input => {
        if (input) {
            input.addEventListener('input', () => formatCurrencyInput(input));
        }
    });
    
    // Form validation on submit
    loanForm.addEventListener('submit', function(e) {
        if (!validateForm()) {
            e.preventDefault();
            return false;
        }
        
        // Show loading state
        const submitButton = loanForm.querySelector('button[type="submit"]');
        const originalText = submitButton.innerHTML;
        submitButton.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Calculating...';
        submitButton.disabled = true;
        
        // Re-enable button after a delay (in case of errors)
        setTimeout(() => {
            submitButton.innerHTML = originalText;
            submitButton.disabled = false;
        }, 10000);
    });
    
    // Real-time preview calculation (debounced)
    let previewTimeout;
    [loanAmountInput, loanTermInput, loanTypeSelect].forEach(input => {
        if (input) {
            input.addEventListener('input', function() {
                clearTimeout(previewTimeout);
                previewTimeout = setTimeout(calculatePreview, 500);
            });
        }
    });
    
    // Initialize
    updateTermLimits();
    
    // Add helpful tooltips (if Bootstrap tooltips are available)
    if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
});

// Utility functions
function formatCurrency(amount, currency = 'NAD') {
    return new Intl.NumberFormat('en-NA', {
        style: 'currency',
        currency: currency,
        minimumFractionDigits: 2
    }).format(amount);
}

function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// Export functions for potential use in other scripts
window.LoanCalculatorUtils = {
    formatCurrency,
    validateEmail
};
