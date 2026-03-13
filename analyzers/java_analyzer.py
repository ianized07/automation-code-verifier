import re
from .base import BaseAnalyzer, Issue


class JavaAnalyzer(BaseAnalyzer):
    def get_language_name(self) -> str:
        return "Java"
    
    def validate_syntax(self) -> bool:
        try:
            import javalang
            javalang.parse.parse(self.code)
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
            
            if 'import org.openqa.selenium' in line_stripped:
                has_selenium = True
            
            if 'WebDriver' in line_stripped and 'import' in line_stripped:
                has_webdriver = True
        
        if not has_selenium:
            self.result.add_issue(Issue(
                Issue.CRITICAL,
                1,
                "Missing Selenium import",
                "Add: import org.openqa.selenium.WebDriver;"
            ))
    
    def check_selenium_patterns(self):
        driver_initialized = False
        driver_quit = False
        has_try_catch = False
        
        for i, line in enumerate(self.lines, 1):
            line_stripped = line.strip()
            
            if 'WebDriver' in line_stripped and '=' in line_stripped and 'new' in line_stripped:
                driver_initialized = True
            
            if 'driver.quit()' in line_stripped or 'driver.close()' in line_stripped:
                driver_quit = True
            
            if 'try {' in line_stripped or 'catch' in line_stripped:
                has_try_catch = True
            
            if 'Thread.sleep' in line_stripped:
                self.result.add_issue(Issue(
                    Issue.WARNING,
                    i,
                    "Using Thread.sleep() instead of explicit waits",
                    "Use WebDriverWait with ExpectedConditions instead"
                ))
            
            if '.findElement(By.' in line_stripped and 'xpath' in line_stripped.lower():
                if '//' in line_stripped:
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
    
    def check_best_practices(self):
        has_page_factory = False
        
        for i, line in enumerate(self.lines, 1):
            line_stripped = line.strip()
            
            if 'PageFactory' in line_stripped:
                has_page_factory = True
            
            if 'manage().timeouts().implicitlyWait' in line_stripped:
                self.result.add_issue(Issue(
                    Issue.WARNING,
                    i,
                    "Implicit wait detected",
                    "Prefer explicit waits (WebDriverWait) for better control"
                ))
