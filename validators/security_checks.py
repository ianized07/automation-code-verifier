import re


class SecurityValidator:
    SECURITY_PATTERNS = {
        'hardcoded_credentials': [
            r'password\s*=\s*["\'][\w!@#$%^&*]+["\']',
            r'username\s*=\s*["\'][\w]+["\']',
            r'api_key\s*=\s*["\'][\w-]+["\']',
            r'token\s*=\s*["\'][\w-]+["\']'
        ],
        'dangerous_functions': [
            r'\beval\(',
            r'\bexec\(',
            r'__import__\('
        ],
        'sql_injection_risk': [
            r'execute\(["\'].*\+.*["\']',
            r'query\(["\'].*\+.*["\']'
        ]
    }
    
    @staticmethod
    def check_hardcoded_secrets(code: str) -> list:
        issues = []
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            for pattern in SecurityValidator.SECURITY_PATTERNS['hardcoded_credentials']:
                if re.search(pattern, line, re.IGNORECASE):
                    issues.append({
                        'line': i,
                        'type': 'hardcoded_credential',
                        'message': 'Possible hardcoded credential detected'
                    })
        
        return issues
    
    @staticmethod
    def check_dangerous_functions(code: str) -> list:
        issues = []
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            for pattern in SecurityValidator.SECURITY_PATTERNS['dangerous_functions']:
                if re.search(pattern, line):
                    issues.append({
                        'line': i,
                        'type': 'dangerous_function',
                        'message': 'Dangerous function detected (eval/exec)'
                    })
        
        return issues
