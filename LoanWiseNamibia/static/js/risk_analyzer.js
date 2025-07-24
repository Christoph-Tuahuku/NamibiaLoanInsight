// Namibia Loan Insight - Risk Analyzer JavaScript
document.addEventListener('DOMContentLoaded', function() {
    const riskForm = document.getElementById('riskForm');
    const ageInput = document.getElementById('age');
    const incomeInput = document.getElementById('monthly_income');
    const creditScoreSelect = document.getElementById('credit_score');
    const defaultsInput = document.getElementById('previous_defaults');
    const loanAmountInput = document.getElementById('loan_amount');
    
    // Risk assessment parameters
    const RISK_THRESHOLDS = {
        age: {
            optimal_min: 25,
            optimal_max: 55,
            min: 18,
            max: 100
        },
        income: {
            low: 5000,
            medium: 15000,
            high: 30000
        },
        credit_score: {
            poor_max: 3,
            fair_max: 6,
            good_max: 8
        },
        debt_to_income: {
            excellent_max: 20,
            good_max: 30,
            concerning_max: 40
        }
    };

    // Real-time risk assessment
    function calculateRiskPreview() {
        const age = parseInt(ageInput.value);
        const income = parseFloat(incomeInput.value);
        const creditScore = parseInt(creditScoreSelect.value);
        const defaults = parseInt(defaultsInput.value);
        const loanAmount = parseFloat(loanAmountInput.value);
        
        if (age && income && creditScore && loanAmount >= 0) {
            const riskAssessment = performRiskCalculation(age, income, creditScore, defaults || 0, loanAmount);
            updateRiskPreview(riskAssessment);
        } else {
            clearRiskPreview();
        }
    }

    // Perform risk calculation (simplified version of backend logic)
    function performRiskCalculation(age, income, creditScore, defaults, loanAmount) {
        let riskScore = 0;
        
        // Age factor
        if (age < RISK_THRESHOLDS.age.optimal_min) {
            riskScore += 15;
        } else if (age > RISK_THRESHOLDS.age.optimal_max) {
            riskScore += 10;
        } else {
            riskScore += 5;
        }
        
        // Income factor
        if (income < RISK_THRESHOLDS.income.low) {
            riskScore += 25;
        } else if (income < RISK_THRESHOLDS.income.medium) {
            riskScore += 15;
        } else {
            riskScore += 5;
        }
        
        // Credit score factor
        riskScore += (11 - creditScore) * 5;
        
        // Defaults factor
        riskScore += defaults * 15;
        
        // Debt-to-income ratio (assuming 1-year loan for DTI calculation)
        const debtToIncomeRatio = (loanAmount / 12) / income * 100;
        if (debtToIncomeRatio > 40) {
            riskScore += 20;
        } else if (debtToIncomeRatio > 30) {
            riskScore += 15;
        } else if (debtToIncomeRatio > 20) {
            riskScore += 10;
        } else {
            riskScore += 5;
        }
        
        // Determine risk level
        let riskLevel, riskColor;
        if (riskScore <= 30) {
            riskLevel = 'Low';
            riskColor = 'success';
        } else if (riskScore <= 60) {
            riskLevel = 'Medium';
            riskColor = 'warning';
        } else {
            riskLevel = 'High';
            riskColor = 'danger';
        }
        
        return {
            riskScore: Math.min(riskScore, 100),
            riskLevel,
            riskColor,
            debtToIncomeRatio: debtToIncomeRatio.toFixed(1)
        };
    }

    // Update risk preview display
    function updateRiskPreview(assessment) {
        let previewSection = document.getElementById('riskPreview');
        
        if (!previewSection) {
            previewSection = document.createElement('div');
            previewSection.id = 'riskPreview';
            riskForm.parentNode.insertBefore(previewSection, riskForm.nextSibling);
        }
        
        previewSection.innerHTML = `
            <div class="card bg-dark border-${assessment.riskColor} mt-3">
                <div class="card-header bg-${assessment.riskColor} text-white">
                    <small><i class="fas fa-eye me-1"></i>Risk Preview</small>
                </div>
                <div class="card-body">
                    <div class="row text-center">
                        <div class="col-md-4 mb-2">
                            <small class="text-muted">Risk Level</small>
                            <div class="text-${assessment.riskColor} fw-bold">${assessment.riskLevel}</div>
                        </div>
                        <div class="col-md-4 mb-2">
                            <small class="text-muted">Risk Score</small>
                            <div class="text-${assessment.riskColor} fw-bold">${assessment.riskScore}/100</div>
                        </div>
                        <div class="col-md-4 mb-2">
                            <small class="text-muted">Debt-to-Income</small>
                            <div class="text-${assessment.riskColor} fw-bold">${assessment.debtToIncomeRatio}%</div>
                        </div>
                    </div>
                    <div class="progress mt-2" style="height: 8px;">
                        <div class="progress-bar bg-${assessment.riskColor}" style="width: ${assessment.riskScore}%"></div>
                    </div>
                    <small class="text-muted d-block mt-2">
                        <i class="fas fa-info-circle me-1"></i>
                        This is a preview. Submit for detailed analysis and personalized advice.
                    </small>
                </div>
            </div>
        `;
    }

    // Clear risk preview
    function clearRiskPreview() {
        const previewSection = document.getElementById('riskPreview');
        if (previewSection) {
            previewSection.remove();
        }
    }

    // Validate form inputs
    function validateRiskForm() {
        const age = parseInt(ageInput.value);
        const income = parseFloat(incomeInput.value);
        const creditScore = parseInt(creditScoreSelect.value);
        const defaults = parseInt(defaultsInput.value);
        const loanAmount = parseFloat(loanAmountInput.value);
        
        let isValid = true;
        let messages = [];
        
        // Age validation
        if (!age || age < 18 || age > 100) {
            messages.push('Please enter a valid age between 18 and 100');
            isValid = false;
        }
        
        // Income validation
        if (!income || income <= 0) {
            messages.push('Please enter a valid monthly income');
            isValid = false;
        } else if (income < 1000) {
            messages.push('Income seems unusually low. Please verify the amount.');
        } else if (income > 100000) {
            messages.push('Income seems unusually high. Please verify the amount.');
        }
        
        // Credit score validation
        if (!creditScore || creditScore < 1 || creditScore > 10) {
            messages.push('Please select a credit score between 1 and 10');
            isValid = false;
        }
        
        // Defaults validation
        if (defaults === null || defaults < 0) {
            messages.push('Please enter the number of previous defaults (0 if none)');
            isValid = false;
        } else if (defaults > 10) {
            messages.push('Number of defaults seems unusually high. Please verify.');
        }
        
        // Loan amount validation
        if (!loanAmount || loanAmount <= 0) {
            messages.push('Please enter a valid loan amount');
            isValid = false;
        } else if (loanAmount > 1000000) {
            messages.push('Loan amount seems unusually high. Please verify.');
        }
        
        // Debt-to-income ratio check
        if (income > 0 && loanAmount > 0) {
            const dtiRatio = (loanAmount / 12) / income * 100;
            if (dtiRatio > 50) {
                messages.push('The requested loan amount results in a very high debt-to-income ratio (>' + dtiRatio.toFixed(1) + '%). Consider reducing the amount.');
            }
        }
        
        // Show validation messages
        if (messages.length > 0) {
            showValidationMessage(messages.join('<br>'), isValid ? 'warning' : 'danger');
        }
        
        return isValid;
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
        riskForm.parentNode.insertBefore(alertDiv, riskForm.nextSibling);
        
        // Auto-dismiss after 7 seconds
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 7000);
    }

    // Format inputs
    function formatNumericInput(input, decimals = 0) {
        let value = input.value.replace(/[^\d.]/g, '');
        if (decimals === 0) {
            value = value.replace(/\./g, '');
        } else if (value.includes('.')) {
            const parts = value.split('.');
            value = parts[0] + '.' + parts[1].substring(0, decimals);
        }
        input.value = value;
    }

    // Provide helpful hints based on inputs
    function provideInputHints() {
        const creditScore = parseInt(creditScoreSelect.value);
        const age = parseInt(ageInput.value);
        const income = parseFloat(incomeInput.value);
        
        let hints = [];
        
        if (creditScore && creditScore <= 3) {
            hints.push('Low credit score may affect loan approval. Consider improving credit before applying.');
        }
        
        if (age && (age < 25 || age > 55)) {
            hints.push('Age factors may impact risk assessment. Stable employment history can help.');
        }
        
        if (income && income < 5000) {
            hints.push('Lower income may require additional documentation or guarantor for loan approval.');
        }
        
        if (hints.length > 0) {
            showHints(hints);
        } else {
            clearHints();
        }
    }

    // Show helpful hints
    function showHints(hints) {
        let hintsSection = document.getElementById('inputHints');
        
        if (!hintsSection) {
            hintsSection = document.createElement('div');
            hintsSection.id = 'inputHints';
            riskForm.appendChild(hintsSection);
        }
        
        hintsSection.innerHTML = `
            <div class="alert alert-info mt-3">
                <h6 class="alert-heading"><i class="fas fa-lightbulb me-1"></i>Helpful Tips:</h6>
                <ul class="mb-0">
                    ${hints.map(hint => `<li>${hint}</li>`).join('')}
                </ul>
            </div>
        `;
    }

    // Clear hints
    function clearHints() {
        const hintsSection = document.getElementById('inputHints');
        if (hintsSection) {
            hintsSection.remove();
        }
    }

    // Event listeners
    let previewTimeout;
    [ageInput, incomeInput, creditScoreSelect, defaultsInput, loanAmountInput].forEach(input => {
        if (input) {
            input.addEventListener('input', function() {
                clearTimeout(previewTimeout);
                previewTimeout = setTimeout(() => {
                    calculateRiskPreview();
                    provideInputHints();
                }, 500);
            });
        }
    });
    
    // Format numeric inputs
    ageInput.addEventListener('input', () => formatNumericInput(ageInput));
    defaultsInput.addEventListener('input', () => formatNumericInput(defaultsInput));
    incomeInput.addEventListener('input', () => formatNumericInput(incomeInput, 2));
    loanAmountInput.addEventListener('input', () => formatNumericInput(loanAmountInput, 2));
    
    // Form validation on submit
    riskForm.addEventListener('submit', function(e) {
        if (!validateRiskForm()) {
            e.preventDefault();
            return false;
        }
        
        // Show loading state
        const submitButton = riskForm.querySelector('button[type="submit"]');
        const originalText = submitButton.innerHTML;
        submitButton.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Analyzing...';
        submitButton.disabled = true;
        
        // Re-enable button after a delay (in case of errors)
        setTimeout(() => {
            submitButton.innerHTML = originalText;
            submitButton.disabled = false;
        }, 10000);
    });
    
    // Credit score description update
    creditScoreSelect.addEventListener('change', function() {
        const score = parseInt(this.value);
        const descriptions = {
            1: 'Very Poor - Significant credit issues',
            2: 'Very Poor - Serious credit problems',
            3: 'Poor - Many credit issues',
            4: 'Fair - Some credit problems',
            5: 'Fair - Moderate credit history',
            6: 'Fair - Average credit standing',
            7: 'Good - Solid credit history',
            8: 'Good - Strong credit profile',
            9: 'Excellent - Outstanding credit',
            10: 'Excellent - Perfect credit history'
        };
        
        const description = descriptions[score];
        if (description) {
            let descElement = document.getElementById('creditScoreDesc');
            if (!descElement) {
                descElement = document.createElement('small');
                descElement.id = 'creditScoreDesc';
                descElement.className = 'form-text text-primary';
                this.parentNode.appendChild(descElement);
            }
            descElement.textContent = description;
        }
    });
    
    // Initialize tooltips if available
    if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
});

// Export utility functions
window.RiskAnalyzerUtils = {
    formatCurrency: function(amount, currency = 'NAD') {
        return new Intl.NumberFormat('en-NA', {
            style: 'currency',
            currency: currency,
            minimumFractionDigits: 2
        }).format(amount);
    },
    
    calculateDebtToIncomeRatio: function(monthlyDebt, monthlyIncome) {
        return (monthlyDebt / monthlyIncome) * 100;
    },
    
    getRiskLevelDescription: function(riskLevel) {
        const descriptions = {
            'Low': 'Excellent financial profile with minimal risk factors',
            'Medium': 'Good profile with some areas for improvement',
            'High': 'Several risk factors that may affect loan approval'
        };
        return descriptions[riskLevel] || 'Unknown risk level';
    }
};
