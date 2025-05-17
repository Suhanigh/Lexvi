"""
Core lexer module for LexVi
Contains token definitions and the main lexer class
"""

import re
from enum import Enum
from typing import List, Tuple, Optional

class TokenType(Enum):
    """Enumeration of possible token types"""
    KEYWORD = "KEYWORD"
    IDENTIFIER = "IDENTIFIER"
    INTEGER = "INTEGER"
    FLOAT = "FLOAT"
    STRING = "STRING"
    OPERATOR = "OPERATOR"
    DELIMITER = "DELIMITER"
    COMMENT = "COMMENT"
    WHITESPACE = "WHITESPACE"
    ERROR = "ERROR"

class Token:
    """Class representing a lexical token"""
    def __init__(self, type: TokenType, value: str, line: int, column: int):
        self.type = type
        self.value = value
        self.line = line
        self.column = column

    def __str__(self):
        return f"Token({self.type}, '{self.value}', line={self.line}, column={self.column})"

class Lexer:
    """Main lexer class that tokenizes input code"""
    
    # Regular expressions for different token types
    TOKEN_PATTERNS = [
        (TokenType.KEYWORD, r'\b(if|else|while|for|return|break|continue|def|class|import|from|as|try|except|finally|raise|with|yield|async|await)\b'),
        (TokenType.IDENTIFIER, r'[a-zA-Z_][a-zA-Z0-9_]*'),
        (TokenType.INTEGER, r'\b\d+\b'),
        (TokenType.FLOAT, r'\b\d+\.\d+\b'),
        (TokenType.STRING, r'"[^"]*"|\'[^\']*\''),
        (TokenType.OPERATOR, r'[+\-*/%=<>!&|^~]+'),
        (TokenType.DELIMITER, r'[(){}\[\],;:.]'),
        (TokenType.COMMENT, r'#.*'),
        (TokenType.WHITESPACE, r'\s+'),
    ]

    def __init__(self):
        self.tokens: List[Token] = []
        self.errors: List[Tuple[str, int, int]] = []
        self.current_line = 1
        self.current_column = 1

    def tokenize(self, code: str) -> List[Token]:
        """Tokenize the input code string"""
        self.tokens = []
        self.errors = []
        self.current_line = 1
        self.current_column = 1

        while code:
            matched = False
            for token_type, pattern in self.TOKEN_PATTERNS:
                regex = re.compile(pattern)
                match = regex.match(code)
                
                if match:
                    value = match.group(0)
                    if token_type != TokenType.WHITESPACE and token_type != TokenType.COMMENT:
                        self.tokens.append(Token(token_type, value, self.current_line, self.current_column))
                    
                    # Update line and column counters
                    lines = value.count('\n')
                    if lines > 0:
                        self.current_line += lines
                        self.current_column = len(value.split('\n')[-1]) + 1
                    else:
                        self.current_column += len(value)
                    
                    code = code[len(value):]
                    matched = True
                    break

            if not matched:
                # No pattern matched, report error
                self.errors.append((f"Unrecognized token: {code[0]}", self.current_line, self.current_column))
                code = code[1:]
                self.current_column += 1

        return self.tokens

    def get_errors(self) -> List[Tuple[str, int, int]]:
        """Return list of lexing errors"""
        return self.errors 