import re


class BestPracticeValidator:
    @staticmethod
    def check_naming_conventions(code: str, language: str) -> list:
        issues = []
        
        if language == "Python":
            if re.search(r'def [A-Z]\w+\(', code):
                issues.append("Python functions should use snake_case, not camelCase")
        
        elif language == "Java" or language == "C#":
            if re.search(r'(class|interface)\s+[a-z]\w+', code):
                issues.append("Class names should start with uppercase")
        
        return issues
    
    @staticmethod
    def check_code_organization(code: str) -> dict:
        lines = code.split('\n')
        total_lines = len(lines)
        comment_lines = sum(1 for line in lines if line.strip().startswith('#') or 
                          line.strip().startswith('//') or 
                          line.strip().startswith('/*'))
        
        return {
            'total_lines': total_lines,
            'comment_lines': comment_lines,
            'comment_ratio': comment_lines / total_lines if total_lines > 0 else 0
        }
    
    @staticmethod
    def check_resource_management(code: str, language: str) -> list:
        issues = []
        
        has_driver_init = any([
            'webdriver.' in code.lower(),
            'new Builder()' in code,
            'IWebDriver' in code
        ])
        
        has_driver_quit = any([
            'driver.quit()' in code,
            'driver.Quit()' in code,
            'driver.close()' in code
        ])
        
        if has_driver_init and not has_driver_quit:
            issues.append("WebDriver initialized but not properly closed")
        
        return issues
    
    @staticmethod
    def check_error_handling(code: str, language: str) -> dict:
        has_try = 'try' in code.lower()
        has_except = any([
            'except' in code.lower(),
            'catch' in code.lower()
        ])
        has_finally = 'finally' in code.lower()
        
        return {
            'has_error_handling': has_try and has_except,
            'has_finally': has_finally,
            'complete': has_try and has_except and has_finally
        }
