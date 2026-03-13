import re
from .base import BaseAnalyzer, Issue


class JavaAnalyzer(BaseAnalyzer):
    def get_language_name(self) -> str:
        return "Java"
    
    def validate_syntax(self) -> bool:
        # Check for language mismatch first
        python_indicators = ['def ', 'import selenium', 'from selenium', 'if __name__']
        csharp_indicators = ['using OpenQA', 'IWebDriver', 'namespace ']
        js_indicators = ['const {', 'require(', 'async function', '=>']
        
        if any(indicator in self.code for indicator in python_indicators):
            self.result.add_issue(Issue(
                Issue.CRITICAL,
                1,
                "Wrong language selected - this appears to be Python code",
                "Select 'Python' from the language dropdown and re-analyze"
            ))
            self.result.score = 0
            return False
        
        if any(indicator in self.code for indicator in csharp_indicators):
            self.result.add_issue(Issue(
                Issue.CRITICAL,
                1,
                "Wrong language selected - this appears to be C# code",
                "Select 'C#' from the language dropdown and re-analyze"
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
        
        # Lenient syntax check - don't fail on minor issues
        try:
            import javalang
            javalang.parse.parse(self.code)
            self.result.syntax_valid = True
        except Exception as e:
            # Mark as syntax issue but continue analysis
            self.result.syntax_valid = False
            self.result.syntax_error = f"Syntax error: {str(e)}"
            self.result.add_issue(Issue(
                Issue.WARNING,
                1,
                f"Syntax error detected: {str(e)}",
                "Review and fix syntax issues for code to compile"
            ))
        # Always continue with pattern analysis
        return True
    
    def check_imports(self):
        has_selenium = False
        has_webdriver = False
        
        for i, line in enumerate(self.lines, 1):
            line_stripped = line.strip()
            
            if 'import org.openqa.selenium' in line_stripped:
                has_selenium = True
            
            if 'WebDriver' in line_stripped and 'import' in line_stripped:
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
            
            if 'WebDriver' in line_stripped and '=' in line_stripped and 'new' in line_stripped:
                driver_initialized = True
                has_selenium_patterns = True
            
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
            
            # Check for findElement methods (deprecated and current)
            if '.findElement' in line_stripped:
                has_selenium_patterns = True
                
                # Accept deprecated methods with info-level feedback
                if 'findElementById' in line_stripped or 'findElementByID' in line_stripped:
                    self.result.add_issue(Issue(
                        Issue.INFO,
                        i,
                        "Using deprecated findElementById() method",
                        "Modern syntax: findElement(By.id(\"element_id\"))"
                    ))
                elif 'findElementByXpath' in line_stripped or 'findElementByXPath' in line_stripped:
                    self.result.add_issue(Issue(
                        Issue.INFO,
                        i,
                        "Using deprecated findElementByXpath() method",
                        "Modern syntax: findElement(By.xpath(\"//xpath\"))"
                    ))
                elif 'findElementByName' in line_stripped:
                    self.result.add_issue(Issue(
                        Issue.INFO,
                        i,
                        "Using deprecated findElementByName() method",
                        "Modern syntax: findElement(By.name(\"name\"))"
                    ))
                elif 'findElementByText' in line_stripped or 'findElementByLinkText' in line_stripped:
                    self.result.add_issue(Issue(
                        Issue.INFO,
                        i,
                        "Using deprecated findElementByLinkText() method",
                        "Modern syntax: findElement(By.linkText(\"text\"))"
                    ))
                
                # Check for XPath in modern syntax
                if '.findElement(By.' in line_stripped and 'xpath' in line_stripped.lower() and '//' in line_stripped:
                    self.result.add_issue(Issue(
                        Issue.INFO,
                        i,
                        "XPath locator detected - may be fragile",
                        "Consider using CSS selectors or ID locators for better maintainability"
                    ))
        
        self.result.has_selenium_patterns = has_selenium_patterns or driver_initialized
        
        if driver_initialized and not driver_quit:
            self.result.add_issue(Issue(
                Issue.WARNING,
                len(self.lines),
                "WebDriver not properly closed (missing driver.quit())",
                "Recommended: Add driver.quit() in a finally block to prevent resource leaks"
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
