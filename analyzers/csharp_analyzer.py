import re
from .base import BaseAnalyzer, Issue


class CSharpAnalyzer(BaseAnalyzer):
    def get_language_name(self) -> str:
        return "C#"
    
    def validate_syntax(self) -> bool:
        # Check for language mismatch first
        python_indicators = ['def ', 'import selenium', 'from selenium', 'if __name__']
        java_indicators = ['public class', 'import org.openqa', 'new ChromeDriver()']
        js_indicators = ['const {', 'require(', 'async function', '=>', 'await driver']
        
        if any(indicator in self.code for indicator in python_indicators):
            self.result.add_issue(Issue(
                Issue.CRITICAL,
                1,
                "Wrong language selected - this appears to be Python code",
                "Select 'Python' from the language dropdown and re-analyze"
            ))
            self.result.score = 0
            return False
        
        if any(indicator in self.code for indicator in java_indicators):
            self.result.add_issue(Issue(
                Issue.CRITICAL,
                1,
                "Wrong language selected - this appears to be Java code",
                "Select 'Java' from the language dropdown and re-analyze"
            ))
            self.result.score = 0
            return False
        
        if any(indicator in self.code for indicator in js_indicators):
            self.result.add_issue(Issue(
                Issue.CRITICAL,
                1,
                "Wrong language selected - this appears to be JavaScript code",
                "Select 'JavaScript' from the language dropdown and re-analyze"
            ))
            self.result.score = 0
            return False
        
        basic_checks = [
            (r'\bclass\s+\w+', "No class definition found"),
            (r'[{}\(\)]', "Missing braces or parentheses"),
        ]
        
        open_braces = self.code.count('{')
        close_braces = self.code.count('}')
        
        if open_braces != close_braces:
            self.result.syntax_valid = False
            self.result.syntax_error = f"Mismatched braces: {open_braces} opening, {close_braces} closing"
            self.result.add_issue(Issue(
                Issue.WARNING,
                1,
                "Mismatched braces in code",
                "Ensure all opening braces have corresponding closing braces"
            ))
            return True
        
        try:
            self.result.syntax_valid = True
            return True
        except Exception as e:
            self.result.syntax_valid = False
            self.result.syntax_error = f"Syntax error: {str(e)}"
            self.result.add_issue(Issue(
                Issue.WARNING,
                1,
                f"Syntax error detected: {str(e)}",
                "Review and fix syntax issues for code to compile"
            ))
            return True
    
    def check_imports(self):
        has_selenium = False
        has_webdriver = False
        
        for i, line in enumerate(self.lines, 1):
            line_stripped = line.strip()
            
            if 'using OpenQA.Selenium' in line_stripped:
                has_selenium = True
            
            if 'IWebDriver' in line_stripped or 'WebDriver' in line_stripped:
                has_webdriver = True
        
        self.result.has_selenium_imports = has_selenium
        
        # User preference: ignore missing imports
        # Just track for pattern detection
        pass
    
    def check_selenium_patterns(self):
        driver_initialized = False
        driver_quit = False
        has_try_catch = False
        has_selenium_patterns = False
        
        for i, line in enumerate(self.lines, 1):
            line_stripped = line.strip()
            
            if 'IWebDriver' in line_stripped and '=' in line_stripped and 'new' in line_stripped:
                driver_initialized = True
                has_selenium_patterns = True
            
            if 'driver.Quit()' in line_stripped or 'driver.Close()' in line_stripped:
                driver_quit = True
            
            if 'try' in line_stripped or 'catch' in line_stripped:
                has_try_catch = True
            
            if 'Thread.Sleep' in line_stripped:
                self.result.add_issue(Issue(
                    Issue.WARNING,
                    i,
                    "Using Thread.Sleep instead of explicit waits",
                    "Use WebDriverWait with ExpectedConditions instead"
                ))
            
            if '.FindElement(' in line_stripped:
                has_selenium_patterns = True
                if 'XPath' in line_stripped and '//' in line_stripped:
                    self.result.add_issue(Issue(
                        Issue.INFO,
                        i,
                        "XPath locator detected - may be fragile",
                        "Consider using CSS selectors or ID locators"
                    ))
        
        self.result.has_selenium_patterns = has_selenium_patterns or driver_initialized
        
        if driver_initialized and not driver_quit:
            self.result.add_issue(Issue(
                Issue.WARNING,
                len(self.lines),
                "WebDriver not properly closed (missing driver.Quit())",
                "Recommended: Add driver.Quit() in a finally block to prevent resource leaks"
            ))
        
        if driver_initialized and not has_try_catch:
            self.result.add_issue(Issue(
                Issue.WARNING,
                1,
                "No exception handling around WebDriver operations",
                "Wrap driver operations in try-catch blocks"
            ))
    
    def check_best_practices(self):
        for i, line in enumerate(self.lines, 1):
            line_stripped = line.strip()
            
            if '.Manage().Timeouts().ImplicitWait' in line_stripped:
                self.result.add_issue(Issue(
                    Issue.WARNING,
                    i,
                    "Implicit wait detected",
                    "Prefer explicit waits (WebDriverWait) for better control"
                ))
