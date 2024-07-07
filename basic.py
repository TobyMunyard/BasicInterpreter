
TOKEN_TYPE_INT = 'INT'
TOKEN_TYPE_FLOAT = 'FLOAT'
TOKEN_TYPE_PLUS = 'PLUS'
TOKEN_TYPE_MINUS = 'MINUS'
TOKEN_TYPE_MUL = 'MUL'
TOKEN_TYPE_DIV = 'DIV'
TOKEN_TYPE_LPAREN = 'LPAREN'
TOKEN_TYPE_RPAREN = 'RPAREN'

DIGITS = '0123456789'

class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'
    
class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = -1
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def make_tokens(self):
        tokens = []

        while self.current_char != None:
            if self.current_char in ' \t':
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char == '+':
                tokens.append(Token(TOKEN_TYPE_PLUS))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(TOKEN_TYPE_MINUS))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(TOKEN_TYPE_MUL))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(TOKEN_TYPE_DIV))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(TOKEN_TYPE_LPAREN))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TOKEN_TYPE_RPAREN))
                self.advance()
            else:
                char = self.current_char
                self.advance()
                return [], IllegalCharError("'" + char + "'")
                
        return tokens, None
    
    def make_number(self):
        num_str = ''
        dot_count = 0
        
        while self.current_char != None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_count == 1: break
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.current_char
            self.advance()
            
        if dot_count == 0:
            return Token(TOKEN_TYPE_INT, int(num_str))
        else:
            return Token(TOKEN_TYPE_FLOAT, float(num_str))
        
        
class Error:
    def __init__(self, error_name, details):
        self.error_name = error_name
        self.details = details
        
    def as_string(self):
        result = f'{self.error_name}: {self.details}'
        return result
    
class IllegalCharError(Error):
    def __init__(self, details):
        super().__init__('Illegal Character', details)
        
def run(text):
    lexer = Lexer(text)
    tokens, error = lexer.make_tokens()
    
    return tokens, error