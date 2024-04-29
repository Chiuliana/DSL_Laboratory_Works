import re
from enum import Enum
from anytree import Node, RenderTree


class TokenType(Enum):
    INTEGER = 2
    FLOAT = 3
    PLUS = 4
    MINUS = 5
    MULTIPLY = 6
    DIVIDE = 7
    LPAREN = 8
    RPAREN = 9
    WHITESPACE = 10


token_patterns = [
    (TokenType.FLOAT, r'\d+\.\d+'),
    (TokenType.INTEGER, r'\d+'),
    (TokenType.PLUS, r'\+'),
    (TokenType.MINUS, r'\-'),
    (TokenType.MULTIPLY, r'\*'),
    (TokenType.DIVIDE, r'\/'),
    (TokenType.LPAREN, r'\('),
    (TokenType.RPAREN, r'\)'),
    (TokenType.WHITESPACE, r'\s')
]


class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return f"Token({self.type}, {self.value})"

    def __repr__(self):
        return self.__str__()


def lexer(text):
    pos = 0
    tokens = []
    while pos < len(text):
        for token_type, pattern in token_patterns:
            regex = re.compile(pattern)
            match = regex.match(text, pos)
            if match:
                value = match.group(0)
                pos = match.end()
                if token_type != TokenType.WHITESPACE:
                    yield Token(token_type, value)
                break
        else:
            raise Exception("Invalid character")


def parser(tokens):
    root = Node("expression")
    current_node = root
    brackets_stack = []
    flag = False
    for token in tokens:
        if token.type == TokenType.LPAREN:
            current_node = Node("sub_expression", parent=current_node)
            brackets_stack.append(current_node)

        elif token.type == TokenType.RPAREN:
            current_node = current_node.parent
            last_node = current_node
            brackets_stack.pop()

        elif token.type == TokenType.MULTIPLY:
            last_node = current_node.children[-1]
            last_node.parent = None
            current_node = Node("multiply", parent=current_node)
            last_node.parent = current_node
            flag = True

        elif token.type == TokenType.DIVIDE:
            last_node = current_node.children[-1]
            last_node.parent = None
            current_node = Node("divide", parent=current_node)
            last_node.parent = current_node
            flag = True

        else:
            Node(token.value, parent=current_node)

            if flag:
                current_node = current_node.parent
                flag = False

    if brackets_stack:
        raise Exception("Invalid syntax")

    return root


def print_tree(node):
    for pre, fill, node in RenderTree(node):
        print("%s%s" % (pre, node.name))

def main():
    file = open("test.txt", "r")
    text = file.read()
    file.close()
    tokens = list(lexer(text))
    root = parser(tokens)
    print_tree(root)


if __name__ == '__main__':
    main()