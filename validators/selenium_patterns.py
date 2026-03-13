import re


class SeleniumPatternValidator:
    COMMON_PATTERNS = {
        'webdriver_init': [
            r'webdriver\.\w+\(',
            r'new\s+\w+Driver',
            r'new Builder\(\)',
            r'IWebDriver.*=.*new'
        ],
        'element_locators': [
            r'find_element',
            r'findElement',
            r'FindElement'
        ],
        'waits': [
            r'WebDriverWait',
            r'implicitly_wait',
            r'until\.',
            r'ExpectedConditions'
        ],
        'actions': [
            r'\.click\(\)',
            r'\.send_keys\(',
            r'\.submit\(\)',
            r'\.clear\(\)'
        ]
    }
    
    ANTI_PATTERNS = {
        'hardcoded_sleep': [
            r'time\.sleep\(',
            r'Thread\.sleep\(',
            r'setTimeout\('
        ],
        'deprecated_locators': [
            r'find_element_by_id',
            r'find_element_by_xpath',
            r'find_element_by_class_name'
        ],
        'fragile_xpath': [
            r'//\*\[',
            r'//div\[\d+\]',
            r'//table//tr//td'
        ]
    }
    
    @staticmethod
    def has_pattern(code: str, pattern_list: list) -> bool:
        for pattern in pattern_list:
            if re.search(pattern, code, re.IGNORECASE):
                return True
        return False
    
    @staticmethod
    def find_pattern_lines(code: str, pattern_list: list) -> list:
        lines = code.split('\n')
        matches = []
        for i, line in enumerate(lines, 1):
            for pattern in pattern_list:
                if re.search(pattern, line, re.IGNORECASE):
                    matches.append((i, line.strip()))
        return matches
