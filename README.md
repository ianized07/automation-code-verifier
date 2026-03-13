# 🔍 Automation Code Verifier

A web-based tool to analyze and verify Selenium automation code across multiple programming languages (Python, Java, JavaScript, C#) through static analysis and validation.

## Features

- **Multi-Language Support:** Analyze Python, Java, JavaScript, and C# Selenium code
- **Language Mismatch Detection:** Automatically detects when code is written in the wrong language (scores 0)
- **Auto-Save Protection:** Code automatically saves every 3 seconds to prevent data loss from crashes or browser refresh
- **Static Analysis:** Parse and validate code without executing it
- **Lenient Scoring Approach:** Partial credit for minor issues, focused on practical candidate assessment
- **Comprehensive Checks:**
  - Syntax validation (continues analysis even with errors)
  - Selenium-specific patterns
  - Best practices validation
  - Anti-pattern detection
  - Deprecated method detection (with modern syntax suggestions)
  - Resource management
  - Exception handling
  - Locator strategy analysis
- **Detailed Reports:** 
  - Line-by-line feedback with severity levels
  - Detailed score breakdown showing all deductions
  - Comprehensive issue listing with suggestions
  - Transparent scoring calculation
- **Code Quality Scoring:** 0-100 score with clear breakdown
- **User-Friendly Interface:** Clean Streamlit UI with syntax highlighting
- **Two-Mode System:**
  - **Candidate Mode:** Simple code editor for writing automation tests
  - **Assessor Mode:** Full analysis and scoring features (password protected)

## Two-Mode System

### Candidate Mode
A clean, distraction-free code editor for candidates taking practical automation tests:
- Language selection (Python, Java, JavaScript, C#)
- Code editor with syntax highlighting
- **Auto-save protection** - code saves every 3 seconds and restores on refresh
- Download button to save code as text file
- No analysis or scoring visible
- Simple, focused interface

**Use Case:** Give candidates a portable IDE to write their Selenium automation code without seeing assessment results or losing work due to crashes.

### Assessor Mode
Full-featured analysis interface for reviewing candidate submissions:
- All features from Candidate Mode
- Code analysis with detailed scoring
- Issue detection and categorization
- Best practice recommendations
- Line-by-line feedback with suggestions
- Password protected to prevent unauthorized access

**Use Case:** Assessors can paste candidate code and receive objective scoring and detailed feedback for evaluation.

## Auto-Save Protection

The application includes **automatic code saving** to prevent data loss:

- **Auto-save interval:** Code saves to browser localStorage every 3 seconds
- **Auto-restore:** Code automatically restores when page refreshes or crashes
- **Before unload:** Code saves when closing tab/browser
- **Visual indicator:** Auto-save status shown in sidebar
- **No data loss:** Works even if internet connection drops temporarily

This feature is especially important for candidates taking tests, ensuring their work is never lost due to:
- Browser crashes
- Accidental page refresh
- Internet connectivity issues
- Power outages
- Tab closures

## Language Mismatch Detection

To prevent cheating or errors, the tool **automatically detects language mismatches**:

- Java code submitted to Python analyzer → **Score: 0/100**
- Python code submitted to Java analyzer → **Score: 0/100**
- All cross-language submissions detected and rejected
- Clear error message directing user to select correct language

**Detection works across all 4 languages:** Python, Java, JavaScript, C#

This prevents candidates from scoring high by selecting the wrong language to bypass strict validation.

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

The tool provides a **0-100 score** based on code quality with **lenient, partial credit** approach for practical candidate assessment:

### Score Ranges
- **85-100:** Excellent - Production-ready code with best practices
- **70-84:** Good - Minor improvements needed
- **55-69:** Acceptable - Has issues but demonstrates understanding
- **40-54:** Needs Work - Multiple problems but shows effort
- **20-39:** Poor - Significant issues or wrong language selected
- **0-19:** Invalid - Wrong language or completely non-functional

### Scoring Rules (Lenient Approach)
- **Critical issues:** -10 points each
- **Warnings:** -3 points each
- **Info/Suggestions:** -2 points each
- **Syntax errors:** -5 points (continues analysis)
- **Wrong language selected:** Score = 0 (e.g., Java code in Python analyzer)
- **Missing imports:** No penalty (ignored)
- **Missing driver.quit():** Warning only (not critical)

### Score Breakdown
Every report includes a detailed breakdown showing:
- Starting score: 100
- All deductions by severity
- Final calculated score
- Transparent, verifiable scoring

### Philosophy
This **lenient scoring approach** gives partial credit for:
- Deprecated methods (with suggestions for modern syntax)
- Minor syntax variations
- Case sensitivity issues
- Missing cleanup code

The goal is to assess practical Selenium knowledge, not penalize candidates for minor issues that modern IDEs would catch.

## What It Checks

### Critical Issues (🔴) - 10 points each
- **Wrong language selected** (Java code in Python analyzer, etc.) - Score = 0
- Code that doesn't match the selected language

### Warnings (⚠️) - 3 points each
- Syntax errors (analysis continues)
- Using hardcoded waits (`Thread.sleep`, `time.sleep`) instead of explicit waits
- Missing exception handling
- Missing `driver.quit()` cleanup
- Implicit waits (prefer explicit waits)
- Mismatched braces/parentheses

### Informational (ℹ️) - 2 points each
- Deprecated methods (e.g., `findElementById`) with modern syntax suggestions
- Complex/fragile XPath locators
- Missing wait strategies
- Code organization suggestions
- Best practice recommendations

### Not Penalized
- Missing imports (ignored)
- Case variations in method names
- Minor formatting issues

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

### Good Code with Minor Issues (Score: 85/100)
```
✅ Overall Score: 85/100

� Score Breakdown:
  Starting Score: 100
  Warnings (2 × -3): -6
  Info/Suggestions (4 × -2): -8
  Syntax Error Penalty: -5
  ─────────────────────
  Final Score: 85/100

⚠️  WARNINGS (2)
  Line 8: Syntax error detected: Expected ';' after statement
  Line 12: Missing driver.quit() - Resource leak detected

ℹ️  SUGGESTIONS (4)
  Line 3: Using deprecated findElementById() method
          Modern syntax: findElement(By.id("element_id"))
  Line 15: Using Thread.sleep() instead of explicit waits
  Line 25: XPath locator detected - may be fragile
  Line 30: Consider implementing exception handling
```

### Wrong Language Selected (Score: 0/100)
```
❌ Overall Score: 0/100

🔴 CRITICAL ISSUES (1)
  Line 1: Wrong language selected - this appears to be Java code
  💡 Select 'Java' from the language dropdown and re-analyze
```

### Code with Deprecated Methods (Score: 88/100)
```
⚠️ Overall Score: 88/100

💯 Score Breakdown:
  Starting Score: 100
  Warnings (1 × -3): -3
  Info/Suggestions (5 × -2): -10
  ─────────────────────
  Final Score: 87/100

⚠️  WARNINGS (1)
  Line 20: Missing exception handling around WebDriver operations

ℹ️  SUGGESTIONS (5)
  Line 5: Using deprecated findElementByXpath() method
  Line 8: Using deprecated findElementById() method
  Line 12: Using deprecated findElementByName() method
  Line 18: XPath locator detected - may be fragile
  Line 25: Consider adding driver.quit() in finally block
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

- Export analysis reports as PDF
- Integration with GitHub repositories
- Multi-file project analysis
- Automated fix suggestions (one-click apply)
- Code formatting tools
- Performance analysis
- Browser compatibility checks
- Historical score tracking
- Candidate comparison dashboard

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

MIT License - feel free to use this project for personal or commercial purposes.

## Author

Created by **Cliff Ian Murillo** - QA Engineer 1

---

**Note:** This tool performs static analysis only and does not execute the submitted code, ensuring safety and security.
