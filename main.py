import argparse
from scanner import Scanner, tokens, Lexeme, Token
from parser import Parser
from ir_compiler import IRCompiler

if __name__ == "__main__":

    # this is the command line parser, not the C-simple parser
    parser = argparse.ArgumentParser()
    parser.add_argument('file_name', type=str)
    args = parser.parse_args()

    # get the program string
    f = open(args.file_name)    
    f_contents = f.read()
    f.close()

    # create the scanner and make a token action for
    # tracking the line number
    s = Scanner()
    def track_lineno(l:Lexeme) -> Lexeme:
        if l.value == "\n":
            s.lineno += 1
        return l
    tokens = tokens + [(Token.IGNORE, " |\n|\t", track_lineno)]
    s.set_tokens(tokens)

    # create the parser with the scanner
    p = Parser(s)

    # create the IRCompiler with the parser
    compiler = IRCompiler(p)

    # compile the program into IR
    compiler.compile2ir(f_contents)

    # print the IR
    print(compiler.ir_program)
