import re

# CONSTANTS
DIGITS = '0123456789'
KEYWORDS = {'if', 'while', 'return'}

# ERRORS
class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start  # Start position of the error
        self.pos_end = pos_end  # End position of the error
        self.error_name = error_name
        self.details = details

    def as_string(self):
        result = f'{self.error_name}: {self.details}\n'  # Formatting error message
        result += f'File {self.pos_start.fn}, line {self.pos_start.ln + 1}'  # Adding file and line information
        return result


class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Illegal Character', details)

# POSITION
class Position:
    def __init__(self, idx, ln, col, fn, ftxt):
        self.idx = idx
        self.ln = ln  # Line number
        self.col = col
        self.fn = fn  # File name
        self.ftxt = ftxt  # Full text of the file

    def advance(self, current_char):
        self.idx += 1  # Moving to next character
        self.col += 1  # Moving to next column

        if current_char == '\n':
            self.ln += 1  # Moving to next line
            self.col = 0  # Reset column number

        return self

    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)  # Creating a copy of the current position
# TOKENS
class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'  # Returning token type and value if available
        return f'{self.type}'


# Token types
TT_INT = 'INT'
TT_FLOAT = 'FLOAT'
TT_PLUS = 'PLUS'
TT_MINUS = 'MINUS'
TT_MUL = 'MUL'
TT_DIV = 'DIV'
TT_LPAREN = 'LPAREN'
TT_RPAREN = 'RPAREN'
TT_IDENTIFIER = 'IDENTIFIER'
TT_STRING = 'STRING'
TT_COMMA = 'COMMA'
TT_ASSIGN = 'ASSIGN'
TT_EQUAL = 'EQUAL'
TT_LESS = 'LESS'
TT_GREATER = 'GREATER'
TT_LESS_EQUAL = 'LESS_EQUAL'
TT_GREATER_EQUAL = 'GREATER_EQUAL'
TT_CHAR = 'CHAR'
TT_EOF = 'EOF'
TT_SPACE = 'SPACE'
TT_NEWLINE = 'NEWLINE'
TT_COLON = 'COLON'
TT_KEYWORD = 'KEYWORD'
TT_SEMICOLON = 'SEMICOLON'
TT_LBRACE = 'LEFT_BRACE'
TT_RBRACE = 'RIGHT_BRACE'

# LEXER
class Lexer:
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text  # Input text
        self.pos = Position(-1, 0, -1, fn, text)  # Starting position
        self.current_char = None
        self.advance()  # Move to the first character

    def advance(self):
        self.pos.advance(self.current_char)  # Move to the next position
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(
            self.text) else None  # Update current character

    def skip_comment(self):
        if self.current_char == '/':
            self.advance()
            if self.current_char == '/':
                # Single-line comment, skip until the end of line
                while self.current_char and self.current_char != '\n':
                    self.advance()
            elif self.current_char == '*':
                # Multi-line comment, skip until '*/'
                depth = 1
                while depth > 0:
                    self.advance()
                    if self.current_char == '/' and self.peek() == '*':
                        depth += 1
                    elif self.current_char == '*' and self.peek() == '/':
                        depth -= 1
                        self.advance()
                        self.advance()
                    elif not self.current_char:
                        # If end of file is reached before closing '*/'
                        raise Exception("Unterminated multi-line comment")
                self.advance()  # Skip closing '*/'
    # Converts input text into tokens.
    def make_tokens(self):
        tokens = []
        errors = []

        while self.current_char is not None:
            # Ignore whitespace characters
            if self.current_char in ' \t':
                self.advance()
            # Numeric tokens
            elif re.match(r'\d', self.current_char):
                tokens.append(self.make_number())
            # Operator tokens
            elif self.current_char == '+':
                tokens.append(Token(TT_PLUS))
                self.advance()
            # Other cases...
            # Parentheses and punctuation tokens...
            elif self.current_char == '(':
                tokens.append(Token(TT_LPAREN))
                self.advance()
            # Identifiers...
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                errors.append(IllegalCharError(pos_start, self.pos, "'" + char + "'"))

        tokens.append(Token(TT_EOF))  # Adding end of file token
        return tokens, errors