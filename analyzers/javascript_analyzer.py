import re
from .base import BaseAnalyzer, Issue


class JavaScriptAnalyzer(BaseAnalyzer):
    def get_language_name(self) -> str:
        return "JavaScript"
    
    def validate_syntax(self) -> bool:
        try:
            import esprima
            esprima.parseScript(self.code)
            self.result.syntax_valid = True
            return True
        except Exception as e:
            self.result.syntax_valid = False
            self.result.syntax_error = f"Syntax error: {str(e)}"
            self.result.add_issue(Issue(
                Issue.CRITICAL,
                1,
                f"Syntax error: {str(e)}",
                "Fix the syntax error before running the code"
            ))
            return False
    
    def check_imports(self):
        has_selenium = False
        has_webdriver = False
        
        for i, line in enumerate(self.lines, 1):
            line_stripped = line.strip()
            
            if 'require(' in line_stripped and 'selenium-webdriver' in line_stripped:
                has_selenium = True
                has_webdriver = True
            
            if 'import' in line_stripped and 'selenium-webdriver' in line_stripped:
                has_selenium = True
                has_webdriver = True
        
        if not has_selenium:
            self.result.add_issue(Issue(
                Issue.CRITICAL,
                1,
                "Missing Selenium WebDriver import",
                "Add: const {Builder, By, until} = require('selenium-webdriver');"
            ))
    
    def check_selenium_patterns(self):
        driver_initialized = False
        driver_quit = False
        has_try_catch = False
        has_async_await = False
        
        for i, line in enumerate(self.lines, 1):
            line_stripped = line.strip()
            
            if 'new Builder()' in line_stripped or '.build()' in line_stripped:
                driver_initialized = True
            
            if 'driver.quit()' in line_stripped or 'driver.close()' in line_stripped:
                driver_quit = True
            
            if 'try {' in line_stripped or 'catch' in line_stripped:
                has_try_catch = True
            
            if 'async ' in line_stripped or 'await ' in line_stripped:
                has_async_await = True
            
            if 'setTimeout' in line_stripped or 'sleep(' in line_stripped:
                self.result.add_issue(Issue(
                    Issue.WARNING,
                    i,
                    "Using setTimeout/sleep instead of explicit waits",
                    "Use driver.wait(until.elementLocated()) instead"
                ))
            
            if '.findElement(' in line_stripped and 'xpath' in line_stripped.lower():
                self.result.add_issue(Issue(
                    Issue.INFO,
                    i,
                    "XPath locator detected - may be fragile",
                    "Consider using CSS selectors or ID locators"
                ))
        
        if driver_initialized and not driver_quit:
            self.result.add_issue(Issue(
                Issue.CRITICAL,
                len(self.lines),
                "WebDriver not properly closed (missing driver.quit())",
                "Add driver.quit() in a finally block"
            ))
        
        if driver_initialized and not has_try_catch:
            self.result.add_issue(Issue(
                Issue.WARNING,
                1,
                "No exception handling around WebDriver operations",
                "Wrap driver operations in try-catch blocks"
            ))
        
        if driver_initialized and not has_async_await:
            self.result.add_issue(Issue(
                Issue.INFO,
                1,
                "No async/await detected",
                "Consider using async/await for cleaner asynchronous code"
            ))
    
    def check_best_practices(self):
        for i, line in enumerate(self.lines, 1):
            line_stripped = line.strip()
            
            if 'driver.manage().timeouts().implicitlyWait' in line_stripped:
                self.result.add_issue(Issue(
                    Issue.WARNING,
                    i,
                    "Implicit wait detected",
                    "Prefer explicit waits (driver.wait) for better control"
                ))
