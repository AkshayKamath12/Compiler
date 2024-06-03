from parser import Parser
from typing import Callable,List,Tuple,Optional

# simple high level class that uses the parser to generate
# a list of 3 address instructions. The compiler then
# wraps that code in a C++ function that can be compiled
# and executed.
class IRCompiler():
    # takes in a parser
    def __init__(self, p: Parser) ->None:
        self.parser = p

    def print_program(self,program: List[str]) ->str:
        # Get the args for the function header
        args = ["%s &%s" % (a[1], a[0]) for a in self.parser.function_args]
        arg_string = ",".join(reversed(args))
        
        # get all the program variables and virtual registers
        vrs = self.parser.vra.declare_variables()
        vrs_str = "\n".join(vrs)
        new_names = "\n".join(["virtual_reg %s;" % n for n in self.parser.nng.new_names])

        # Get the 3 address instructions
        program_str = "\n".join(program)

        # print the function
        return """
#include "../../classir.h"
void %s(%s){
%s
%s
%s
return;
}
        """ % (self.parser.function_name, arg_string, vrs_str, new_names, program_str)
        

    def compile2ir(self, s: str) -> None:
        # Get the 3 address instructions
        program = self.parser.parse(s)

        # Wrap them in a C++ function
        self.ir_program = self.print_program(program)
