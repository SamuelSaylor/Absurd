DIGITS = "0123456789" # Constants

# ERRORS #################################################

class Error: # Errors in case stuff goes down
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details
        
    def as_string(self):
        result = f'{self.error_name}: {self.details}'
        result += f'File {self.pos_start.fn}, line {self.pos_start.ln + 1}'
        return result

class IllegalCharError (Error): # When lexer finds error it dont support
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, "There is an issue with your computer, I am pondering the possibilities and believe it might just be an illusive \"IllegalCharError\" which basically has some very simple implications! I am led to believe it is because... uhhhhh... i forgot. Google is free though! Here's some lame details: ", details)
#################################################

class Position: # Pinpoints position in code where stuff happens
    def __init__(self, index, ln, col, fn, ftxt): # ln = linenumbber, col = column number, fn = filename, ftxt = file text
        self.index = index
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt
    
    def advance(self, current_char):
        self.index += 1
        self.col += 1

        if current_char == '\n':
            self.ln += 1
            self.col = 0

        return self

    def copy(self):
        return Position(self.index, self.ln, self.col, self.fn, self.ftxt)


TT_INT		= 'INT'
TT_FLOAT    = 'FLOAT'
TT_PLUS     = 'PLUS'
TT_MINUS    = 'MINUS'
TT_MUL      = 'MUL'
TT_DIV      = 'DIV'
TT_LPAREN   = "LPAREN" # left parenthesis
TT_RPAREN   = "RPAREN" # you guessed it

class Token: # stores keywords, operators, etc
    def __init__(self,types, value =None):
        self.type = types
        self.value = value
    
    def __repr__(self): # Represents token as a string
        if self.value: 
            return f'{self.type}:{self.value}'
        return f'{self.type}'

########################

class Lexer: #breaks down code into tokens
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Position(-1,0,-1, fn, text) # Think of it as like typing on the terminal (but instead for text) and each time you type the position goes up by 1
        self.current_char = None
        self.advance() # increments
        
    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.index] if self.pos.index < len(self.text) else None
    
    def make_tokens(self):
        tokens = [ ]
        
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
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos,"'"+char + "'") # Returns no tokens
            
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
        
def run(fn, text): # Run stuff
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    
    return tokens, error
