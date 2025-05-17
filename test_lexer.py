"""
Test module for the lexer functionality
"""

import pytest
from lexer.core import Lexer, Token, TokenType

def test_basic_tokenization():
    """Test basic tokenization of simple code"""
    lexer = Lexer()
    code = "def hello(): return 42"
    tokens = lexer.tokenize(code)
    
    assert len(tokens) == 5
    assert tokens[0].type == TokenType.KEYWORD
    assert tokens[0].value == "def"
    assert tokens[1].type == TokenType.IDENTIFIER
    assert tokens[1].value == "hello"
    assert tokens[2].type == TokenType.DELIMITER
    assert tokens[2].value == "("
    assert tokens[3].type == TokenType.DELIMITER
    assert tokens[3].value == ")"
    assert tokens[4].type == TokenType.INTEGER
    assert tokens[4].value == "42"

def test_string_tokenization():
    """Test tokenization of string literals"""
    lexer = Lexer()
    code = 'x = "hello world"'
    tokens = lexer.tokenize(code)
    
    assert len(tokens) == 3
    assert tokens[0].type == TokenType.IDENTIFIER
    assert tokens[0].value == "x"
    assert tokens[1].type == TokenType.OPERATOR
    assert tokens[1].value == "="
    assert tokens[2].type == TokenType.STRING
    assert tokens[2].value == '"hello world"'

def test_error_detection():
    """Test detection of invalid tokens"""
    lexer = Lexer()
    code = "x = @invalid"
    tokens = lexer.tokenize(code)
    errors = lexer.get_errors()
    
    assert len(errors) == 1
    assert errors[0][0] == "Unrecognized token: @"
    assert errors[0][1] == 1  # line number
    assert errors[0][2] == 5  # column number

def test_whitespace_handling():
    """Test proper handling of whitespace"""
    lexer = Lexer()
    code = "x  =  42\n  y=  'test'"
    tokens = lexer.tokenize(code)
    
    assert len(tokens) == 6
    assert tokens[0].type == TokenType.IDENTIFIER
    assert tokens[0].value == "x"
    assert tokens[1].type == TokenType.OPERATOR
    assert tokens[1].value == "="
    assert tokens[2].type == TokenType.INTEGER
    assert tokens[2].value == "42"
    assert tokens[3].type == TokenType.IDENTIFIER
    assert tokens[3].value == "y"
    assert tokens[4].type == TokenType.OPERATOR
    assert tokens[4].value == "="
    assert tokens[5].type == TokenType.STRING
    assert tokens[5].value == "'test'"

def test_comment_handling():
    """Test proper handling of comments"""
    lexer = Lexer()
    code = "x = 42 # This is a comment"
    tokens = lexer.tokenize(code)
    
    assert len(tokens) == 3
    assert tokens[0].type == TokenType.IDENTIFIER
    assert tokens[0].value == "x"
    assert tokens[1].type == TokenType.OPERATOR
    assert tokens[1].value == "="
    assert tokens[2].type == TokenType.INTEGER
    assert tokens[2].value == "42" 