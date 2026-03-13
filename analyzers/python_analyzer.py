import ast
import re
from .base import BaseAnalyzer, Issue


class PythonAnalyzer(BaseAnalyzer):
    def get_language_name(self) -> str:
        return "Python"
    
    def validate_syntax(self) -> bool:
        try:
            ast.parse(self.code)
            self.result.syntax_valid = True
            return True
        except SyntaxError as e:
            self.result.syntax_valid = False
            self.result.syntax_error = f"Syntax error at line {e.lineno}: {e.msg}"
            self.result.add_issue(Issue(
                Issue.CRITICAL,
                e.lineno or 0,
                f"Syntax error: {e.msg}",
                "Fix the syntax error before running the code"
            ))
            return False
    
    def check_imports(self):
        has_selenium = False
        has_webdriver = False
        has_wait = False
        
        for i, line in enumerate(self.lines, 1):
            line_stripped = line.strip()
            
            if 'from selenium' in line_stripped or 'import selenium' in line_stripped:
                has_selenium = True
            
            if 'webdriver' in line_stripped.lower():
                has_webdriver = True
            
            if 'WebDriverWait' in line_stripped or 'expected_conditions' in line_stripped:
                has_wait = True
        
        if not has_selenium:
            self.result.add_issue(Issue(
                Issue.CRITICAL,
                1,
                "Missing Selenium import",
                "Add: from selenium import webdriver"
            ))
        
        if not has_webdriver and has_selenium:
            self.result.add_issue(Issue(
                Issue.WARNING,
                1,
                "WebDriver not imported",
                "Consider importing: from selenium.webdriver"
            ))
    
    def check_selenium_patterns(self):
        driver_initialized = False
        driver_quit = False
        has_try_except = False
        has_selenium_patterns = False
        
        for i, line in enumerate(self.lines, 1):
            line_stripped = line.strip()
            
            if 'webdriver.' in line_stripped.lower() and '=' in line_stripped:
                driver_initialized = True
                has_selenium_patterns = True
            
            if 'driver.quit()' in line_stripped or 'driver.close()' in line_stripped:
                driver_quit = True
            
            if 'try:' in line_stripped or 'except' in line_stripped:
                has_try_except = True
            
            if 'time.sleep' in line_stripped or 'sleep(' in line_stripped:
                self.result.add_issue(Issue(
                    Issue.WARNING,
                    i,
                    "Using time.sleep() instead of explicit waits",
                    "Use WebDriverWait with expected_conditions instead"
                ))
            
            if '.find_element_by_' in line_stripped:
                self.result.add_issue(Issue(
                    Issue.WARNING,
                    i,
                    "Deprecated locator method used",
                    "Use find_element(By.ID, 'element_id') instead"
                ))
            
            if '///' in line_stripped or 'xpath' in line_stripped.lower():
                if '//' in line_stripped and '[' in line_stripped:
                    self.result.add_issue(Issue(
                        Issue.INFO,
                        i,
                        "Complex XPath detected - may be fragile",
                        "Consider using CSS selectors or simpler XPath"
                    ))
            
            if 'find_element' in line_stripped.lower() or 'get(' in line_stripped:
                has_selenium_patterns = True
        
        self.result.has_selenium_patterns = has_selenium_patterns or driver_initialized
        
        if driver_initialized and not driver_quit:
            self.result.add_issue(Issue(
                Issue.WARNING,
                len(self.lines),
                "WebDriver not properly closed (missing driver.quit())",
                "Recommended: Add driver.quit() in a finally block to prevent resource leaks"
            ))
        
        if driver_initialized and not has_try_except:
            self.result.add_issue(Issue(
                Issue.WARNING,
                1,
                "No exception handling around WebDriver operations",
                "Wrap driver operations in try-except blocks"
            ))
    
    def check_best_practices(self):
        has_implicit_wait = False
        has_explicit_wait = False
        
        for i, line in enumerate(self.lines, 1):
            line_stripped = line.strip()
            
            if 'implicitly_wait' in line_stripped:
                has_implicit_wait = True
                self.result.add_issue(Issue(
                    Issue.WARNING,
                    i,
                    "Implicit wait detected",
                    "Prefer explicit waits (WebDriverWait) for better control"
                ))
            
            if 'WebDriverWait' in line_stripped:
                has_explicit_wait = True
        
        if not has_explicit_wait and not has_implicit_wait:
            self.result.add_issue(Issue(
                Issue.INFO,
                1,
                "No wait strategy detected",
                "Consider using WebDriverWait for reliable element interactions"
            ))
