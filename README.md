# 🔍 Automation Code Verifier

A web-based tool to analyze and verify Selenium automation code across multiple programming languages (Python, Java, JavaScript, C#) through static analysis and validation.

## Features

- **Multi-Language Support:** Analyze Python, Java, JavaScript, and C# Selenium code
- **Static Analysis:** Parse and validate code without executing it
- **Comprehensive Checks:**
  - Syntax validation
  - Import/package verification
  - Selenium-specific patterns
  - Best practices validation
  - Anti-pattern detection
  - Resource management
  - Exception handling
  - Locator strategy analysis
- **Detailed Reports:** Get line-by-line feedback with severity levels and improvement suggestions
- **Code Quality Scoring:** 0-100 score based on issues found
- **User-Friendly Interface:** Clean Streamlit UI with syntax highlighting
- **Two-Mode System:**
  - **Candidate Mode:** Simple code editor for writing automation tests
  - **Assessor Mode:** Full analysis and scoring features (password protected)

## Two-Mode System

### Candidate Mode
A clean, distraction-free code editor for candidates taking practical automation tests:
- Language selection (Python, Java, JavaScript, C#)
- Code editor with syntax highlighting
- Download button to save code as text file
- No analysis or scoring visible
- Simple, focused interface

**Use Case:** Give candidates a portable IDE to write their Selenium automation code without seeing assessment results.

### Assessor Mode
Full-featured analysis interface for reviewing candidate submissions:
- All features from Candidate Mode
- Code analysis with detailed scoring
- Issue detection and categorization
- Best practice recommendations
- Line-by-line feedback with suggestions
- Password protected to prevent unauthorized access

**Use Case:** Assessors can paste candidate code and receive objective scoring and detailed feedback for evaluation.

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. Clone or navigate to the project directory:
```bash
cd automation-code-verifier
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Starting the Application

1. Start the Streamlit application:
```bash
streamlit run app.py
```

2. Open your browser (should open automatically at `http://localhost:8501`)

### For Candidates (Candidate Mode - Default)

1. The app opens in **Candidate Mode** by default
2. Select your programming language from the dropdown
3. Write your Selenium automation code in the editor
4. Click **"Download Code"** when finished
5. Submit the downloaded `.txt` file to your assessor

**Note:** Analysis features are hidden in Candidate Mode to provide a clean coding environment.

### For Assessors (Assessor Mode)

1. Switch to **"Assessor Mode"** in the sidebar
2. Enter the assessor password when prompted
3. Select the programming language
4. Paste the candidate's code or click "Load Example"
5. Click **"Analyze Code"** to run the analysis
6. Review the results:
   - Overall score (0-100)
   - Issue count by severity
   - Detailed line-by-line feedback
   - Suggestions for improvement

**Tip:** You can lock/unlock Assessor Mode at any time using the button in the sidebar.

## Scoring System

The tool provides a **0-100 score** based on code quality, with strict penalties for invalid or incomplete Selenium code:

### Score Ranges
- **90-100:** Excellent - Production-ready code with best practices
- **75-89:** Good - Minor improvements needed
- **60-74:** Acceptable - Has issues but functional
- **40-59:** Poor - Multiple problems, needs significant work
- **20-39:** Very Poor - Critical issues, missing basics
- **0-19:** Invalid - Syntax errors, not Selenium code, or gibberish

### Scoring Rules
- **Syntax errors:** Score drops to 0 immediately
- **Missing Selenium imports:** Score capped at 20 maximum
- **No Selenium patterns detected:** Score capped at 30 maximum
- **Missing imports + patterns:** Score capped at 10 maximum
- **Critical issues:** -15 points each
- **Warnings:** -8 points each
- **Info/Suggestions:** -3 points each

This strict scoring prevents random or invalid code from scoring high and ensures only legitimate Selenium automation receives passing grades.

## What It Checks

### Critical Issues (🔴)
- Syntax errors
- Missing required imports
- WebDriver not properly closed (resource leaks)
- Mismatched braces/parentheses

### Warnings (⚠️)
- Using hardcoded waits (`Thread.sleep`, `time.sleep`) instead of explicit waits
- Missing exception handling
- Deprecated locator methods
- Implicit waits (prefer explicit waits)

### Informational (ℹ️)
- Complex/fragile XPath locators
- Missing wait strategies
- Code organization suggestions
- Best practice recommendations

## Supported Languages

### Python
- AST-based syntax validation
- Checks for: `selenium`, `webdriver`, `WebDriverWait`, `expected_conditions`
- Detects deprecated methods like `find_element_by_*`

### Java
- javalang parser for syntax checking
- Checks for: `org.openqa.selenium`, `WebDriver`, `WebDriverWait`
- Validates exception handling with try-catch-finally

### JavaScript
- esprima parser for AST analysis
- Checks for: `selenium-webdriver`, `Builder`, `async/await`
- Validates promise handling and asynchronous patterns

### C#
- Pattern-based syntax validation
- Checks for: `OpenQA.Selenium`, `IWebDriver`, `WebDriverWait`
- Validates resource disposal patterns

## Project Structure

```
automation-code-verifier/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── analyzers/
│   ├── __init__.py
│   ├── base.py              # Base analyzer class
│   ├── python_analyzer.py   # Python code analysis
│   ├── java_analyzer.py     # Java code analysis
│   ├── javascript_analyzer.py  # JavaScript analysis
│   └── csharp_analyzer.py   # C# code analysis
├── validators/
│   ├── __init__.py
│   ├── selenium_patterns.py # Common Selenium patterns
│   ├── best_practices.py    # Best practice checks
│   └── security_checks.py   # Security validation
└── utils/
    ├── __init__.py
    ├── syntax_checker.py    # Syntax validation
    └── report_generator.py  # Format analysis results
```

## Example Analysis Output

### Good Code (Score: 78/100)
```
✅ Overall Score: 78/100

🔴 CRITICAL ISSUES (1)
  Line 15: Missing driver.quit() - Resource leak detected

⚠️  WARNINGS (2)
  Line 12: Using Thread.sleep() instead of WebDriverWait
  Line 25: Fragile XPath locator - consider using CSS or ID

ℹ️  SUGGESTIONS (1)
  Consider implementing Page Object Model pattern
```

### Invalid Code (Score: 0/100)
```
❌ Overall Score: 0/100

🔴 SYNTAX ERROR
  Line 1: invalid syntax

Fix syntax errors before proceeding with analysis.
```

### Non-Selenium Code (Score: 10/100)
```
⚠️ Overall Score: 10/100

🔴 CRITICAL ISSUES (2)
  Line 1: Missing Selenium import
  Line 1: No Selenium patterns detected - this doesn't appear to be automation code
```

## Candidate Assessment Workflow

This tool is designed to streamline the automation candidate evaluation process:

### Setup
1. Deploy the application (locally or on Streamlit Cloud)
2. Share the URL with candidates

### Candidate Test
1. Candidate opens the app (automatically in Candidate Mode)
2. Receives test scenario/requirements separately
3. Writes Selenium automation code
4. Downloads their code as a text file
5. Submits the file

### Assessment Review
1. Assessor switches to Assessor Mode (password protected)
2. Pastes candidate's code into the analyzer
3. Reviews automated scoring and feedback:
   - **Score 80+:** Strong candidate with solid fundamentals
   - **Score 60-79:** Acceptable with areas for improvement
   - **Score <60:** Significant issues or gaps in knowledge
4. Uses detailed feedback for interview discussion points
5. Makes hiring decision based on objective metrics + code review

### Benefits
- **Objective Scoring:** Consistent evaluation criteria across all candidates
- **Time Savings:** Automated first-pass analysis before manual review
- **Detailed Feedback:** Specific issues and improvement suggestions
- **Prevents Cheating:** Candidates can't see scoring or analysis
- **Portable Testing:** Web-based, no installation required for candidates

## Dependencies

- `streamlit>=1.30.0` - Web UI framework
- `pygments>=2.17.0` - Syntax highlighting
- `javalang>=0.13.0` - Java parsing
- `esprima>=4.0.1` - JavaScript parsing
- `pylint>=3.0.0` - Python linting
- `flake8>=7.0.0` - Python style checking

## Future Enhancements

- Save/load code snippets
- Export analysis reports as PDF
- Integration with GitHub repositories
- Multi-file project analysis
- Automated fix suggestions
- Code formatting tools
- Performance analysis
- Browser compatibility checks

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

MIT License - feel free to use this project for personal or commercial purposes.

## Author

Created by **Cliff Ian Murillo** - QA Engineer 1

---

**Note:** This tool performs static analysis only and does not execute the submitted code, ensuring safety and security.
