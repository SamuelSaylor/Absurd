DIGITS = "0123456789" # Constants

# ERRORS #################################################

class Error: # Errors in case stuff goes down
    def __init__(self, error_name, details):
        self.error_name = error_name
        self.details = details
        
    def as_string(self):
        result = f'{self.error_name}: {self.details}'
        return result

class IllegalCharError (Error): # When lexer finds error it dont support
    def __init__(self, details):
        super().__init__("There is an issue with your computer, I am pondering the possibilities and believe it might just be an illusive \"IllegalCharError\" which basically has some very simple implications! I am led to believe it is because... uhhhhh... i forgot. Google is free though! Here's some lame details: ", details)
#################################################
    

TT_INT = "INT"
TT_FLOAT = "FLOAT"
TT_PLUS = "PLUS"
TT_MINUS = "MINUS"
TT_MUL = "MUL"
TT_DIV = "DIV"
TT_LPAREN = "LPAREN" # left parenthesis
TT_RPAREN = "RPAREN" # you guessed it

class Token: # stores keywords, operators, etc
    def __init_(self,type_, value =None):
        self.type = type_
        self.value = value
    
    def __repr__(self): # Represents token as a string
        if self.value:
            return f'{self.type}:{self.value}'
        return f'{self.type}'

########################

class Lexer: #breaks down code into tokens
    def __init__(self, text):
        self.text = text
        self.pos = -1 # Think of it as like typing on the terminal (but instead for text) and each time you type the position goes up by 1
        self.current_char = None
        self.advance() # increments
        
    def advance(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None
    
    def make_tokens(self):
        tokens = []
        
        while self.current_char != None:
            if self.current_char in ' \t': #checks for enter
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char == "+":
                tokens.append(Token(TT_PLUS))
                self.advance()
            elif self.current_char == "-":
                tokens.append(Token(TT_MINUS))
                self.advance()  
            elif self.current_char == "*":
                tokens.append(Token(TT_MUL))
                self.advance()
            elif self.current_char == "/":
                tokens.append(Token(TT_DIV))
                self.advance()
            elif self.current_char == "(":
                tokens.append(Token(TT_LPAREN))
                self.advance()
            elif self.current_char == ")":
                tokens.append(Token(TT_RPAREN))
                self.advance()
            else:
                char = self.current_char
                self.advance()
                return [], IllegalCharError("'"+char + "'") # Returns no tokens
            
        return tokens, None # None for error
    
    def make_number(self):
        num_str = '' # Number for display
        decimal_count = 0 # Checks for decimals aka floats
        
        while self.current_char != None and self.current_char in DIGITS + ".":
            if self.current_char == ".": # Creating floats
                if decimal_count == 1: break # Ensures you cant have multiple decimals
                decimal_count += 1
                num_str += "."
            else:
                num_str += self.current_char
            self.advance()
            
        if decimal_count == 0: # Differentiates between int and float
            # int
            return Token(TT_INT, int(num_str))
        else:
            # float
            return Token(TT_FLOAT, float(num_str))
        
def run(text): # Run stuff
    lexer = Lexer(text)
    tokens, error = lexer.make_tokens()
    
    return tokens, error
