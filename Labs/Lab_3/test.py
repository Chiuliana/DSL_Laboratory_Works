import re  # Importing regular expression library

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

# Regular expressions for token patterns
TOKEN_REGEX = r'(?P<TOKEN>{})'
TOKEN_PATTERNS = {
    TT_INT: r'\d+',
    TT_FLOAT: r'\d+\.\d+',
    TT_PLUS: r'\+',
    TT_MINUS: r'-',
    TT_MUL: r'\*',
    TT_DIV: r'/',
    TT_LPAREN: r'\(',
    TT_RPAREN: r'\)',
    TT_IDENTIFIER: r'[a-zA-Z_][a-zA-Z0-9_]*',
    TT_STRING: r'"([^\\"]|\\")*"',
    TT_COMMA: r',',
    TT_ASSIGN: r'=',
    TT_EQUAL: r'==',
    TT_LESS: r'<',
    TT_GREATER: r'>',
    TT_LESS_EQUAL: r'<=',
    TT_GREATER_EQUAL: r'>=',
    TT_CHAR: r'char',
    TT_EOF: r'EOF',
    TT_SPACE: r'\s+',
    TT_NEWLINE: r'\n',
    TT_COLON: r':',
    TT_SEMICOLON: r';',
    TT_LBRACE: r'{',
    TT_RBRACE: r'}'
}


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
            elif self.current_char == '-':
                tokens.append(Token(TT_MINUS))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(TT_MUL))
                self.advance()
            elif self.current_char == '/':
                # Handling comments
                if self.peek() == '/':
                    self.skip_comment()
                else:
                    tokens.append(Token(TT_DIV))
                    self.advance()
            # Parentheses and punctuation tokens
            elif self.current_char == '(':
                tokens.append(Token(TT_LPAREN))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TT_RPAREN))
                self.advance()
            elif self.current_char == ',':
                tokens.append(Token(TT_COMMA))
                self.advance()
            elif self.current_char == '=':
                tokens.append(Token(TT_ASSIGN))
                self.advance()
            elif self.current_char == '<':
                self.advance()
                if self.current_char == '=':
                    tokens.append(Token(TT_LESS_EQUAL))
                    self.advance()
                else:
                    tokens.append(Token(TT_LESS))
            elif self.current_char == '>':
                self.advance()
                if self.current_char == '=':
                    tokens.append(Token(TT_GREATER_EQUAL))
                    self.advance()
                else:
                    tokens.append(Token(TT_GREATER))
            elif self.current_char == '"':
                tokens.append(self.make_string())
            elif self.current_char == 'c':
                tokens.append(self.make_char(errors))
            # Newline and punctuation tokens
            elif self.current_char == '\n':
                tokens.append(Token(TT_NEWLINE))
                self.advance()
            elif self.current_char == ':':
                tokens.append(Token(TT_COLON))
                self.advance()
            elif self.current_char == ';':
                tokens.append(Token(TT_SEMICOLON))
                self.advance()
            elif self.current_char == '{':
                tokens.append(Token(TT_LBRACE))
                self.advance()
            elif self.current_char == '}':
                tokens.append(Token(TT_RBRACE))
                self.advance()
            # Identifiers
            elif re.match(r'[a-zA-Z_]', self.current_char):
                tokens.append(self.make_identifier())
            # Handling illegal characters
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                errors.append(IllegalCharError(pos_start, self.pos, "'" + char + "'"))

        tokens.append(Token(TT_EOF))  # Adding end of file token
        return tokens, errors

    # Creates a numeric token.
    def make_number(self):
        num_str = ''

        while self.current_char is not None and re.match(r'\d|\.', self.current_char):
            num_str += self.current_char
            self.advance()

        if '.' in num_str:
            return Token(TT_FLOAT, float(num_str))
        else:
            return Token(TT_INT, int(num_str))

    # Creates a string token.
    def make_string(self):
        string = ''
        escape_character = False
        self.advance()

        escape_characters = {
            'n': '\n',
            't': '\t'
        }

        while self.current_char is not None and (self.current_char != '"' or escape_character):
            if escape_character:
                string += escape_characters.get(self.current_char, self.current_char)
                escape_character = False
            else:
                if self.current_char == '\\':
                    escape_character = True
                else:
                    string += self.current_char
            self.advance()

        self.advance()  # Closing quote
        return Token(TT_STRING, string)

    #   Creates a character token.
    def make_char(self, errors):
        char = 'c'
        self.advance()
        if self.current_char == 'h':
            char += 'h'
            self.advance()
            if self.current_char == 'a':
                char += 'a'
                self.advance()
                if self.current_char == 'r':
                    char += 'r'
                    self.advance()
                    return Token(TT_CHAR, char)

        pos_start = self.pos.copy()
        char = self.current_char
        self.advance()
        errors.append(IllegalCharError(pos_start, self.pos, "'" + char + "'"))

    # Creates an identifier token.
    def make_identifier(self):
        id_str = ''
        while self.current_char is not None and re.match(r'[a-zA-Z0-9_]', self.current_char):
            id_str += self.current_char
            self.advance()
        if id_str in KEYWORDS:
            return Token(TT_KEYWORD, id_str)
        return Token(TT_IDENTIFIER, id_str)

    # Peeks at the next character.
    def peek(self):
        peek_pos = self.pos.idx + 1
        if peek_pos < len(self.text):
            return self.text[peek_pos]
        return None


# RUN
def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, errors = lexer.make_tokens()
    return tokens, errors

