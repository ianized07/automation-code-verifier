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

1. Start the Streamlit application:
```bash
streamlit run app.py
```

2. Open your browser (should open automatically at `http://localhost:8501`)

3. Select your programming language from the dropdown

4. Paste your Selenium automation code or click "Load Example" to see a sample

5. Click "Analyze Code" to run the analysis

6. Review the results:
   - Overall score (0-100)
   - Issue count by severity
   - Detailed line-by-line feedback
   - Suggestions for improvement

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

```
✅ Overall Score: 78/100

🔴 CRITICAL ISSUES (2)
  Line 15: Missing driver.quit() - Resource leak detected
  Line 8: No exception handling around WebDriver operations

⚠️  WARNINGS (3)
  Line 12: Using Thread.sleep() instead of WebDriverWait
  Line 25: Fragile XPath locator - consider using CSS or ID
  Line 30: Implicit wait set - prefer explicit waits

ℹ️  SUGGESTIONS (2)
  Consider implementing Page Object Model pattern
  Add meaningful comments for complex locator strategies
```

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
