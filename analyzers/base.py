from abc import ABC, abstractmethod
from typing import List, Dict, Any


class Issue:
    CRITICAL = "critical"
    WARNING = "warning"
    INFO = "info"
    
    def __init__(self, severity: str, line: int, message: str, suggestion: str = ""):
        self.severity = severity
        self.line = line
        self.message = message
        self.suggestion = suggestion
    
    def __repr__(self):
        return f"Issue({self.severity}, line {self.line}: {self.message})"


class AnalysisResult:
    def __init__(self, language: str):
        self.language = language
        self.issues: List[Issue] = []
        self.score = 100
        self.syntax_valid = True
        self.syntax_error = None
        self.has_selenium_imports = False
        self.has_selenium_patterns = False
    
    def add_issue(self, issue: Issue):
        self.issues.append(issue)
        if issue.severity == Issue.CRITICAL:
            self.score -= 10
        elif issue.severity == Issue.WARNING:
            self.score -= 5
        elif issue.severity == Issue.INFO:
            self.score -= 2
        self.score = max(0, self.score)
    
    def finalize_score(self):
        """Apply final scoring adjustments based on Selenium patterns"""
        # Lenient scoring: syntax errors don't immediately drop to 0
        # Give partial credit for attempting to write Selenium code
        
        if not self.syntax_valid:
            # Deduct 30 points for syntax issues but don't drop to 0
            self.score = max(0, self.score - 30)
        
        # Less strict penalties for missing imports/patterns
        if not self.has_selenium_imports:
            self.score = max(0, self.score - 15)
        
        if not self.has_selenium_patterns:
            self.score = max(0, self.score - 15)
    
    def get_issues_by_severity(self, severity: str) -> List[Issue]:
        return [i for i in self.issues if i.severity == severity]
    
    def get_summary(self) -> Dict[str, Any]:
        return {
            'language': self.language,
            'score': self.score,
            'syntax_valid': self.syntax_valid,
            'syntax_error': self.syntax_error,
            'total_issues': len(self.issues),
            'critical': len(self.get_issues_by_severity(Issue.CRITICAL)),
            'warnings': len(self.get_issues_by_severity(Issue.WARNING)),
            'info': len(self.get_issues_by_severity(Issue.INFO))
        }


class BaseAnalyzer(ABC):
    def __init__(self, code: str):
        self.code = code
        self.lines = code.split('\n')
        self.result = AnalysisResult(self.get_language_name())
    
    @abstractmethod
    def get_language_name(self) -> str:
        pass
    
    @abstractmethod
    def validate_syntax(self) -> bool:
        pass
    
    @abstractmethod
    def check_imports(self):
        pass
    
    @abstractmethod
    def check_selenium_patterns(self):
        pass
    
    def check_best_practices(self):
        pass
    
    def analyze(self) -> AnalysisResult:
        if not self.validate_syntax():
            self.result.finalize_score()
            return self.result
        
        self.check_imports()
        self.check_selenium_patterns()
        self.check_best_practices()
        
        self.result.finalize_score()
        return self.result
