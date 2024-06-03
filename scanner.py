import pdb
from enum import Enum
from typing import Callable,List,Tuple,Optional
import re

class ScannerException(Exception):
    
    # this time, the scanner exception takes a line number
    def __init__(self, lineno:int) -> None:
        message = "Scanner error on line: " + str(lineno)
        super().__init__(message)

class Token(Enum):
    LPAR   = "("
    RPAR   = ")"
    ID     = "ID"
    NUM    = "NUM"
    IGNORE = "IGNORE"
    MUL    = "MUL"
    PLUS   = "PLUS"
    MINUS  = "MINUS"
    DIV    = "DIV"
    EQ     = "EQ"
    LT     = "LT"
    LBRACE = "LBRACE"
    RBRACE = "RBRACE"
    SEMI   = "SEMI"
    ASSIGN = "ASSIGN"
    AMP    = "AMP"
    COMMA  = "COMMA"
    IF     = "IF"
    ELSE   = "ELSE"
    FOR    = "FOR"
    INT    = "INT"
    FLOAT  = "FLOAT"
    VOID   = "VOID"

class Lexeme:
    def __init__(self, token:Token, value:str) -> None:
        self.token = token
        self.value = value

    def __str__(self) -> str:
        return "(" + str(self.token) + "," + "\"" + self.value + "\"" + ")"    


class Scanner:
    def __init__(self) -> None:
        self.lineno = 1

    def set_tokens(self, tokens: List[Tuple[Token,str,Callable[[Lexeme],Lexeme]]]) -> None:
        self.tokens = tokens

    def input_string(self, input_string:str) -> None:
        self.istring = input_string

    # Get the scanner line number, needed for the parser exception
    def get_lineno(self)->int:
        return self.lineno


    def token(self) -> Optional[Lexeme]:
    
        # Loop until we find a token we can
        # return (or until the string is empty)
        while True:
            if len(self.istring) == 0:
                return None

            # For each substring
            for l in range(len(self.istring),0,-1):
                matches = []

                # Check each token
                for t in self.tokens:
                    # Create a tuple for each token:
                    # * first element is the token name
                    # * second is the possible match
                    # * third is the token action
                    matches.append((t[0],
                                    re.fullmatch(t[1],self.istring[:l]),
                                    t[2]))

                matches = [m for m in matches if m[1] is not None]
                if len(matches) > 0:
                    break
    
            if len(matches) == 0:
                raise ScannerException(self.lineno);
              
            longest = matches[0]

            # apply the token action
            lexeme = longest[2](Lexeme(longest[0],longest[1][0]))

            # figure how much we need to chop from our input string
            chop = len(lexeme.value)
            self.istring = self.istring[chop:]

            # if we did not match an IGNORE token, then we can
            # return the lexeme
            if lexeme.token != Token.IGNORE:
                return lexeme


keywords = [(Token.IF, "if"), (Token.ELSE, "else"), (Token.FOR, "for"), (Token.INT, "int"), (Token.FLOAT, "float"), (Token.VOID, "void")]

def find_keywords(l) -> Lexeme:
    values = [k[1] for k in keywords]
    if l.value in values:
        i = values.index(l.value)
        return Lexeme(keywords[i][0],keywords[i][1])
    return l

def idy(l:Lexeme) -> Lexeme:
    return l

tokens = [(Token.MUL,    "\*", idy),
          (Token.PLUS,   "\+", idy),
          (Token.MINUS,  "\-", idy),
          (Token.DIV,    "/",  idy),
          (Token.EQ,     "==", idy),
          (Token.LT,     "<",  idy),
          (Token.LBRACE, "{",  idy),
          (Token.RBRACE, "}",  idy),
          (Token.LPAR,   "\(", idy),
          (Token.RPAR,   "\)", idy),
          (Token.SEMI,   ";",  idy),
          (Token.ASSIGN, "=",  idy),
          (Token.AMP,    "&",  idy),
          (Token.COMMA,  ",",  idy),
          (Token.NUM,    "([0-9]+(\.[0-9]+)?)|(\.[0-9]+)", idy),
          (Token.ID,     "[a-zA-Z]+[a-zA-Z0-9]*", find_keywords)]
