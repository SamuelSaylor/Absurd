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

class InvalidSyntaxError(Error):
    def __init__(self, pos_start, pos_end, details=""):
        super().__init__(pos_start,pos_end,"Well this is peculiar, there is an error but Id rather not discuss it with you. Think about your mistake, and try again. If that doesnt work, try again! Keep fixing mistakes, this one will keep coming in! Heres a HUGE hint for this error: Its very common and its because you messed up horribly. Either improve and stop making mistakes, or just get better.",details)
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

# NODES ###################################

class NumberNode:
    def __init__(self, token):
        self.token = token
    
    def __repr__(self):
        return f'{self.token}'

class BinOpNode: # Operations such as addition, subtraction, etc
    def __init__(self, left_node, op_tok, right_node):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node

    def __repr__(self):
        return f'({self.left_node}, {self.op_tok}, {self.right_node})'

# Parser############################

class Parser: # A parser takes data and breaks it into smaller parts. For example: 7 + 10 * 2 becomes 7 + (10 * 2)
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_index = -1
        self.advance()

    def advance(self):
        self.tok_index += 1
        if self.tok_index < len(self.tokens):
            self.current_token = self.tokens[self.tok_index]
        return self.current_token

# Parser functions#####################################

    def parse(self):
        res = self.expr()
        return res
    
    def factor(self): # In math, a number, variable, term, or longer expression that is multiplied by something else
        token = self.current_token

        if token.type in (TT_INT, TT_FLOAT):
            self.advance()
            return NumberNode(token)

    def term(self): # In math, a number variable or constant multiplied by a variable or variables
        return self.bin_op(self.factor, (TT_MUL, TT_DIV))

    def expr(self): # Expression: Combination of one or more terms that an assembler evaluates into a single value
        return self.bin_op(self.term, (TT_PLUS, TT_MINUS))

    ###########################################

    def bin_op(self, func, ops): # function it refers to, binary operation
        left = func()

        while self.current_token.type in ops:
            op_tok = self.current_token
            self.advance()
            right = func()
            left = BinOpNode(left, op_tok, right)

        return left # RETURNS LEFT FACTOR, AKA WHAT IS TO LEFT OF NUM


def run(fn, text): # Run stuff
    # Gen tokens
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    if error:
        return None, error
    
    # Gen AST
    parser = Parser(tokens)
    ast = parser.parse()
    
    return ast, None

    return tokens, error
