# Namibia Loan Insight

## Overview

Namibia Loan Insight is a Flask-based web application designed to help Namibians make informed financial decisions by providing loan calculation tools and risk assessment features. The application ensures compliance with NamFISA (Namibia Financial Institutions Supervisory Authority) and Bank of Namibia regulations.

## User Preferences

Preferred communication style: Simple, everyday language.
UI Theme: White background theme (updated from dark theme)
Contact Information: Christoph Tuahuku, Lumina TechEdge (Pty) Ltd
- LinkedIn: https://www.linkedin.com/in/christoph-tuahuku-78477b196/
- GitHub: https://github.com/Christoph-Tuahuku
- Email: tjimbanae@gmail.com
- WhatsApp: +264817356870

## System Architecture

### Frontend Architecture
- **Framework**: HTML templates using Jinja2 templating engine
- **Styling**: Bootstrap 5 for responsive design with custom dark theme CSS
- **Icons**: Font Awesome for UI icons
- **JavaScript**: Vanilla JavaScript for client-side validation and real-time calculations
- **Theme**: Custom dark theme inspired by Namibian flag colors (blue, red, green, yellow)

### Backend Architecture
- **Framework**: Flask (Python web framework)
- **Structure**: Modular design with separate files for routes, calculations, and business logic
- **Session Management**: Flask sessions with configurable secret key
- **Logging**: Python's built-in logging module for debugging and monitoring

### Application Structure
- `app.py`: Main Flask application initialization
- `routes.py`: URL routing and view logic
- `calculations.py`: Core business logic for loan calculations and risk analysis
- `templates/`: HTML templates with Jinja2 templating
- `static/`: CSS and JavaScript assets

## Key Components

### Loan Calculator (`LoanCalculator` class)
- **Purpose**: Calculates loan payments with regulatory compliance
- **Features**:
  - Cash loan calculations (max 30% APR, 1-6 months term)
  - Bank loan calculations (16.8% APR, 1-64 months term)
  - Administration fees and insurance cost inclusion
  - Real-time compliance validation

### Risk Analyzer (`RiskAnalyzer` class)
- **Purpose**: Assesses borrower risk profiles
- **Factors**: Age, income, credit score, loan history, debt-to-income ratio
- **Output**: Risk categorization and personalized recommendations

### Web Interface
- **Pages**: Home, loan calculator, risk analyzer, about, contact
- **Navigation**: Fixed top navigation with responsive design
- **Forms**: Input validation and real-time feedback
- **Results**: Detailed calculation breakdowns with compliance warnings

## Data Flow

1. **User Input**: Forms collect loan parameters and personal financial data
2. **Validation**: Client-side JavaScript provides immediate feedback
3. **Processing**: Flask routes handle form submissions
4. **Calculation**: Business logic classes perform calculations with regulatory checks
5. **Response**: Results displayed with compliance status and warnings
6. **Feedback**: Flash messages for errors and validation issues

## External Dependencies

### Frontend Dependencies
- **Bootstrap 5**: CSS framework for responsive design
- **Font Awesome 6**: Icon library for UI elements
- **CDN Delivery**: External resources loaded via CDN

### Python Dependencies
- **Flask**: Web framework
- **Standard Library**: `os`, `logging`, `math`, `typing` modules

### Regulatory Compliance
- **NamFISA**: Maximum APR = Prime Rate × 1.6 (currently 16.8%), 60-month term limit, N$50,000 max amount
- **Bank of Namibia**: Prime rate 10.5%, 84-month term limit for bank loans
- **Built-in Validation**: Automatic compliance checking with official formulas and current rates
- **Official Sources**: Rates verified from NamFISA.com.na and Bank of Namibia websites

## Deployment Strategy

### Development Configuration
- **Host**: 0.0.0.0 (all interfaces)
- **Port**: 5000
- **Debug Mode**: Enabled for development
- **Secret Key**: Environment variable with fallback

### Production Considerations
- **Environment Variables**: `SESSION_SECRET` for secure session management
- **Logging**: Configurable logging levels
- **Error Handling**: Flash messages for user-friendly error reporting

### File Structure
```
/
├── app.py              # Flask app initialization
├── main.py             # Application entry point
├── routes.py           # URL routing and views
├── calculations.py     # Business logic (incomplete)
├── templates/          # HTML templates
│   ├── base.html       # Base template
│   ├── index.html      # Home page
│   ├── loan_calculator.html
│   ├── risk_analyzer.html
│   ├── about.html
│   └── contact.html
└── static/
    ├── css/style.css   # Custom dark theme
    └── js/
        ├── calculator.js
        └── risk_analyzer.js
```

### Current Implementation Status
- **Complete**: Flask app structure, routing, templates, frontend styling, calculations.py with official regulatory rates
- **Updated**: Official NamFISA rates (Prime Rate × 1.6 formula), current prime rates, proper term and amount limits
- **Verified**: Regulatory compliance with official sources from NamFISA and Bank of Namibia websites
- **Ready**: Full loan calculator and risk analyzer functionality with real-time validation
- **NEW (2025-07-24)**: Comprehensive feature expansion completed including:
  - Loan comparison tool with side-by-side analysis
  - Budget planner with affordability calculator
  - Debt consolidation analyzer
  - NamFISA registered lender directory
  - Financial literacy education hub
  - Fraud protection center with real-time alerts
  - PostgreSQL database integration with complete data models
  - Enhanced calculations engine with advanced algorithms
  - Professional navigation with dropdown menus
  - Interactive charts and visual analytics

### Recent Changes (July 24, 2025)
- Implemented comprehensive database models (RegisteredLender, FraudAlert, FinancialTip, etc.)
- Added advanced calculation engines (LoanComparator, DebtConsolidator, BudgetCalculator)
- Created all major feature templates with responsive design
- Integrated Chart.js for visual data representation
- Added sample data seeding functionality
- Updated navigation structure with organized dropdown menus
- Enhanced user experience with interactive forms and real-time calculations

The application now represents a complete financial platform for Namibians with all requested advanced features fully implemented and working.
