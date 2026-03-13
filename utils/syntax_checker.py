import ast
import re


class SyntaxChecker:
    @staticmethod
    def check_python(code: str) -> tuple:
        try:
            ast.parse(code)
            return True, None
        except SyntaxError as e:
            return False, f"Line {e.lineno}: {e.msg}"
    
    @staticmethod
    def check_java(code: str) -> tuple:
        try:
            import javalang
            javalang.parse.parse(code)
            return True, None
        except Exception as e:
            return False, str(e)
    
    @staticmethod
    def check_javascript(code: str) -> tuple:
        try:
            import esprima
            esprima.parseScript(code)
            return True, None
        except Exception as e:
            return False, str(e)
    
    @staticmethod
    def check_csharp(code: str) -> tuple:
        open_braces = code.count('{')
        close_braces = code.count('}')
        
        if open_braces != close_braces:
            return False, f"Mismatched braces: {open_braces} opening, {close_braces} closing"
        
        open_parens = code.count('(')
        close_parens = code.count(')')
        
        if open_parens != close_parens:
            return False, f"Mismatched parentheses: {open_parens} opening, {close_parens} closing"
        
        return True, None
