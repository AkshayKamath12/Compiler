# change types to type ~ change IDtypes to IDtype
import pdb
import class_ast as class_ast
from class_ast import *
from typing import Callable,List,Tuple,Optional
from scanner import Lexeme,Token,Scanner

# Extra classes:

# Keeps track of the type of an ID,
# i.e. whether it is a program variable
# or an IO variable
class IDType(Enum):
    IO = 1
    VAR = 2

# The data to be stored for each ID in the symbol table
class SymbolTableData:
    def __init__(self, id_type: IDType, data_type: Type, new_name: str) -> None:
        self.id_type = id_type      # if the variable is input/output
                                    # or variable
                                    
        self.data_type = data_type  # if the variable is an int or
                                    # float
                                    
        self.new_name = new_name    # a new name to resolve collisions
                                    # in scoping

    # Getters for each of the elements
    def get_id_type(self) -> IDType:
        return self.id_type

    def get_data_type(self) -> Type:
        return self.data_type

    def get_new_name(self) -> str:
        return self.new_name

# Symbol Table exception, requires a line number and ID
class SymbolTableException(Exception):
    def __init__(self, lineno: int, ID: str) -> None:
        message = "Symbol table error on line: " + str(lineno) + "\nUndeclared ID: " + str(ID)
        super().__init__(message)

# Generates a new label when needed
class NewLabelGenerator():
    def __init__(self) -> None:
        self.counter = 0
        
    def mk_new_label(self) -> str:
        new_label = "label" + str(self.counter)
        self.counter += 1
        return new_label

# Generates a new name (e.g. for program variables)
# when needed
class NewNameGenerator():
    def __init__(self) -> None:
        self.counter = 0
        self.new_names = []

    # You may want to make a better renaming scheme
    def mk_new_name(self) -> str:
        new_name = "_new_name" + str(self.counter)
        self.counter += 1
        self.new_names.append(new_name)
        return new_name
    
# Allocates virtual registers
class VRAllocator():
    def __init__(self) -> None:
        self.counter = 0
        
    def mk_new_vr(self) -> str:
        vr = "vr" + str(self.counter)
        self.counter += 1
        return vr

    # get variable declarations (needed for the C++ wrapper)
    def declare_variables(self) -> List[str]:
        ret = []
        for i in range(self.counter):
            ret.append("virtual_reg vr%d;" % i)

        return ret

# Symbol table class
class SymbolTable:
    def __init__(self) -> None:
        # stack of hashtables
        self.ht_stack = [dict()]
        self.nng = NewNameGenerator()

    def insert(self, ID: str, id_type: IDType, data_type: Type) -> None:
        
        # Create the data to store for the ID
        info = SymbolTableData(id_type, data_type, ID)
        self.ht_stack[-1][ID] = info        

    # Lookup the symbol. If it is there, return the
    # info, otherwise return None
    def lookup(self, ID: str) -> Optional:
        for ht in reversed(self.ht_stack):
            if ID in ht:
                return ht[ID]
        return None

    def push_scope(self) -> None:
        self.ht_stack.append(dict())

    def pop_scope(self) -> None:
        self.ht_stack.pop()

# Parser Exception
class ParserException(Exception):
    
    # Pass a line number, current lexeme, and what tokens are expected
    def __init__(self, lineno: int, lexeme: Lexeme, tokens: List[Token]) -> None:
        message = "Parser error on line: " + str(lineno) + "\nExpected one of: " + str(tokens) + "\nGot: " + str(lexeme)
        super().__init__(message)

# Parser class
class Parser:

    # Creating the parser requires a scanner
    def __init__(self, scanner: Scanner) -> None:
        
        self.scanner = scanner

        # Create a symbol table
        self.symbol_table = SymbolTable()

        # objects to create virtual registers,
        # labels, and new names
        self.vra = VRAllocator()
        self.nlg = NewLabelGenerator()
        self.nng = NewNameGenerator()

        # needed to create the C++ wrapper
        # You do not need to modify these for the
        # homework
        self.function_name = None
        self.function_args = []


    
    # HOMEWORK: top level function:
    # This needs to return a list of 3 address instructions
    def parse(self, s: str) -> List[str]:

        # Set the scanner and get the first token
        self.scanner.input_string(s)
        self.to_match = self.scanner.token()

        # start parsing. In your solution, p must contain a list of
        # three address instructions
        p = self.parse_function()
        self.eat(None)
        
        return p

    # Helper fuction: get the token ID
    def get_token_id(self, l: Lexeme) ->Token:
        if l is None:
            return None
        return l.token

    # Helper fuction: eat a token ID and advance
    # to the next token
    def eat(self, check: Token) -> None:
        token_id = self.get_token_id(self.to_match)
        if token_id != check:
            raise ParserException(self.scanner.get_lineno(),
                                  self.to_match,
                                  [check])      
        self.to_match = self.scanner.token()
    
    def allocateRegisters(self, node) -> None:
        if is_binop_node(node):
            self.allocateRegisters(node.l_child)
            self.allocateRegisters(node.r_child)
        elif is_unop_node(node):
            self.allocateRegisters(node.child)
        node.vr = self.vra.mk_new_vr()
            
    def label_code(self, label: str) -> str:
        return label + ":"
        
    # The top level parse_function
    def parse_function(self) -> List[str]:

        # I am parsing the function header for you
        # You do not need to do anything with this.
        self.parse_function_header()    
        self.eat(Token.LBRACE)

        # your solution should have p containing a list
        # of three address instructions
        p = self.parse_statement_list()        
        self.eat(Token.RBRACE)
        return p


    def parse_function_header(self) -> None:
        self.eat(Token.VOID)
        function_name = self.to_match.value
        self.eat(Token.ID)        
        self.eat(Token.LPAR)
        self.function_name = function_name
        args = self.parse_arg_list()
        self.function_args = args
        self.eat(Token.RPAR)


    def parse_arg_list(self) -> List[Tuple[str, str]]:
        token_id = self.get_token_id(self.to_match)
        if token_id == Token.RPAR:
            return
        arg = self.parse_arg()
        token_id = self.get_token_id(self.to_match)
        if token_id == Token.RPAR:
            return [arg]
        self.eat(Token.COMMA)
        arg_l = self.parse_arg_list()
        return arg_l + [arg]


    def parse_arg(self) -> Tuple[str, str]:
        token_id = self.get_token_id(self.to_match)
        if token_id == Token.FLOAT:
            self.eat(Token.FLOAT)
            data_type = Type.FLOAT
            data_type_str = "float"            
        elif token_id == Token.INT:
            self.eat(Token.INT)
            data_type = Type.INT
            data_type_str = "int"
        else:
            raise ParserException(self.scanner.get_lineno(),
                              self.to_match,            
                              [Token.INT, Token.FLOAT])
        self.eat(Token.AMP)
	# change strings and indexing token.names .value .token
        id_name = self.to_match.value
        self.eat(Token.ID)

        # storing an IO variable to the symbol table
        self.symbol_table.insert(id_name, IDType.IO, data_type)
        return (id_name, data_type_str)

    def parse_statement_list(self) -> List[str]:
        token_id = self.get_token_id(self.to_match)
        if token_id in [Token.INT, Token.FLOAT, Token.ID, Token.IF, Token.LBRACE, Token.FOR]:
            value1 = self.parse_statement()
            value2 = self.parse_statement_list()
            if value2 is not []:
                return value1 + value2
            else:
                return value1
        if token_id in [Token.RBRACE]:
            return []
        
    def parse_statement(self) -> List[str]:
        token_id = self.get_token_id(self.to_match)
        if token_id in [Token.INT, Token.FLOAT]:
            return self.parse_declaration_statement()
        elif token_id in [Token.ID]:
            return self.parse_assignment_statement()
        elif token_id in [Token.IF]:
            return self.parse_if_else_statement()
        elif token_id in [Token.LBRACE]:
            return self.parse_block_statement()
        elif token_id in [Token.FOR]:
            return self.parse_for_statement()
        else:
            raise ParserException(self.scanner.get_lineno(),
                              self.to_match,            
                              [Token.FOR, Token.IF, Token.LBRACE, Token.INT, Token.FLOAT, Token.ID])


    def parse_declaration_statement(self) -> List[str]:
        token_id = self.get_token_id(self.to_match)
        if token_id in [Token.INT]:
            self.eat(Token.INT)
            id_name = self.to_match.value
            self.symbol_table.insert(id_name, IDType.VAR, Type.INT)
            id_data = self.symbol_table.lookup(id_name)
            new_name = self.nng.mk_new_name()
            id_data.new_name = new_name
            self.eat(Token.ID)
            self.eat(Token.SEMI)
            return []
        if token_id in [Token.FLOAT]:
            self.eat(Token.FLOAT)
            id_name = self.to_match.value
            self.symbol_table.insert(id_name, IDType.VAR, Type.FLOAT)
            id_data = self.symbol_table.lookup(id_name)
            new_name = self.nng.mk_new_name()
            id_data.new_name = new_name
            self.eat(Token.ID)
            self.eat(Token.SEMI)
            return []
        
        raise ParserException(self.scanner.get_lineno(),
                              self.to_match,            
                              [Token.INT, Token.FLOAT])

    def parse_assignment_statement(self) -> List[str]:
        value = self.parse_assignment_statement_base()
        self.eat(Token.SEMI)
        return value

    def parse_assignment_statement_base(self) -> List[str]:
        id_name = self.to_match.value
        id_data = self.symbol_table.lookup(id_name)
        id_data_type = id_data.get_data_type()
        if id_data == None:
            raise SymbolTableException(self.scanner.get_lineno(), id_name)
        self.eat(Token.ID)
        self.eat(Token.ASSIGN)
        node = self.parse_expr()
        type_inference(node)
        if id_data_type == Type.INT and node.node_type == Type.FLOAT:
            ast = ASTFloatToIntNode(node)
            node = ast
        elif id_data_type == Type.FLOAT and node.node_type == Type.INT:
            ast = ASTIntToFloatNode(node)
            node = ast
        self.allocateRegisters(node)
        program = node.linearize()
        if id_data.get_id_type() == IDType.VAR:
            if id_data_type == Type.INT:
                return program + ["%s = %s;" % (id_data.get_new_name(), node.vr)]
            else:
                return program + ["%s = %s;" % (id_data.get_new_name(), node.vr)]
        else:
            if id_data_type == Type.INT:
                return program + ["%s = vr2int(%s);" % (id_name, node.vr)]
            else:
                return program + ["%s = vr2float(%s);" % (id_name, node.vr)]

    def parse_if_else_statement(self) -> List[str]:
        self.eat(Token.IF)
        self.eat(Token.LPAR)
        node = self.parse_expr()
        type_inference(node)
        self.allocateRegisters(node)
        program0 = node.linearize()
        self.eat(Token.RPAR)
        program1 = self.parse_statement()
        self.eat(Token.ELSE)
        program2 = self.parse_statement()
        vrx = self.vra.mk_new_vr()
        else_label = self.nlg.mk_new_label()
        end_label = self.nlg.mk_new_label()     
        ins0 = "%s = int2vr(0);" % (vrx)
        ins1 = "beq(%s, %s, %s);" %(node.vr, vrx, else_label)
        ins2 = "branch(%s);" %(end_label)
        return program0 + [ins0, ins1] + program1 + [ins2, self.label_code(else_label)] + program2 + [self.label_code(end_label)]

    def parse_block_statement(self) -> List[str]:
        self.eat(Token.LBRACE)
        self.symbol_table.push_scope()
        result = self.parse_statement_list()
        self.symbol_table.pop_scope()
        self.eat(Token.RBRACE)
        return result

    def parse_for_statement(self) -> List[str]:
        self.eat(Token.FOR)
        self.eat(Token.LPAR)
        asign0 = self.parse_assignment_statement()
        node = self.parse_expr()
        type_inference(node)
        self.allocateRegisters(node)
        evalExpr = node.linearize()
        self.eat(Token.SEMI)
        asign1 = self.parse_assignment_statement_base()
        self.eat(Token.RPAR)
        program = self.parse_statement()
        start_label = self.nlg.mk_new_label()
        end_label = self.nlg.mk_new_label()
        vrx = self.vra.mk_new_vr()
        ins0 = "%s = int2vr(0);" % (vrx)
        ins1 = "beq(%s, %s, %s);" % (node.vr, vrx, end_label)
        ins2 = "branch(%s);" % (start_label) 
        return asign0 + [self.label_code(start_label)] + evalExpr + [ins0, ins1] + program + asign1 + [ins2, self.label_code(end_label)]

    def parse_expr(self) -> ASTNode:        
        node = self.parse_comp()
        return self.parse_expr2(node)

    def parse_expr2(self, lhs_node) -> ASTNode:
        token_id = self.get_token_id(self.to_match)
        if token_id in [Token.EQ]:
            self.eat(Token.EQ)
            rhs_node = self.parse_comp()
            node = ASTEqNode(lhs_node, rhs_node)
            return self.parse_expr2(node)
        if token_id in [Token.SEMI, Token.RPAR]:
            return lhs_node
        
        raise ParserException(self.scanner.get_lineno(),
                              self.to_match,            
                              [Token.EQ, Token.SEMI, Token.RPAR])
    
    def parse_comp(self) -> ASTNode:
        node = self.parse_factor()
        return self.parse_comp2(node)

    def parse_comp2(self, lhs_node) -> ASTNode:
        token_id = self.get_token_id(self.to_match)
        if token_id in [Token.LT]:
            self.eat(Token.LT)
            rhs_node = self.parse_factor()
            node = ASTLtNode(lhs_node, rhs_node)
            return self.parse_comp2(node)
        if token_id in [Token.SEMI, Token.RPAR, Token.EQ]:
            return lhs_node
        
        raise ParserException(self.scanner.get_lineno(),
                              self.to_match,            
                              [Token.EQ, Token.SEMI, Token.RPAR, Token.LT])

    def parse_factor(self) -> ASTNode:
        node = self.parse_term()
        return self.parse_factor2(node)

    def parse_factor2(self, lhs_node) -> ASTNode:
        token_id = self.get_token_id(self.to_match)
        if token_id in [Token.PLUS]:
            self.eat(Token.PLUS)
            rhs_node = self.parse_term()    
            node = ASTPlusNode(lhs_node, rhs_node)        
            return self.parse_factor2(node)
        if token_id in [Token.MINUS]:
            self.eat(Token.MINUS)
            rhs_node = self.parse_term()
            node = ASTMinusNode(lhs_node, rhs_node)
            return self.parse_factor2(node)
        if token_id in [Token.EQ, Token.SEMI, Token.RPAR, Token.LT]:
            return lhs_node

        raise ParserException(self.scanner.get_lineno(),
                              self.to_match,            
                              [Token.EQ, Token.SEMI, Token.RPAR, Token.LT, Token.PLUS, Token.MINUS])
    
    def parse_term(self) -> ASTNode:
        node = self.parse_unit()
        return self.parse_term2(node)

    def parse_term2(self, lhs_node) -> ASTNode:
        token_id = self.get_token_id(self.to_match)
        if token_id in [Token.DIV]:
            self.eat(Token.DIV)
            rhs_node = self.parse_unit()
            node = ASTDivNode(lhs_node, rhs_node)
            return self.parse_term2(node)
        if token_id in [Token.MUL]:
            self.eat(Token.MUL)
            rhs_node = self.parse_unit()
            node = ASTMultNode(lhs_node, rhs_node)
            return self.parse_term2(node)
        if token_id in [Token.EQ, Token.SEMI, Token.RPAR, Token.LT, Token.PLUS, Token.MINUS]:
            return lhs_node

        raise ParserException(self.scanner.get_lineno(),
                              self.to_match,            
                              [Token.EQ, Token.SEMI, Token.RPAR, Token.LT, Token.PLUS, Token.MINUS, Token.MUL, Token.DIV])

    def parse_unit(self) -> ASTNode:
        token_id = self.get_token_id(self.to_match)
        if token_id in [Token.NUM]:
            value = self.to_match.value
            self.eat(Token.NUM)  
            node = ASTNumNode(value)          
            return node
        if token_id in [Token.ID]:
            id_name = self.to_match.value
            id_data = self.symbol_table.lookup(id_name)
            if id_data == None:
                raise SymbolTableException(self.scanner.get_lineno(), id_name)
            self.eat(Token.ID)
            id_type = id_data.id_type
            data_type = id_data.get_data_type()
            if id_type == IDType.IO:
                node = ASTIOIDNode(id_name, data_type)
                return node
            else:
                node = ASTVarIDNode(id_data.get_new_name(), data_type)
                return node
        if token_id in [Token.LPAR]:
            self.eat(Token.LPAR)
            node = self.parse_expr()
            self.eat(Token.RPAR)
            return node
            
        raise ParserException(self.scanner.get_lineno(),
                              self.to_match,            
                              [Token.NUM, Token.ID, Token.LPAR])    

# Type inference start
def is_leaf_node(node) -> bool:
    return issubclass(type(node), ASTLeafNode)
    
def is_unop_node(node) -> bool:
    return issubclass(type(node), ASTUnOpNode)

def is_binop_node(node) -> bool:
    return issubclass(type(node), ASTBinOpNode)

def type_conversion(node) -> None:
    if node.node_type == Type.INT:
        if node.l_child.node_type == Type.FLOAT:
            conv = ASTFloatToIntNode(node.l_child)
            node.l_child = conv
        if node.r_child.node_type == Type.FLOAT:
            conv = ASTFloatToIntNode(node.r_child)
            node.r_child = conv
    else:
        if node.l_child.node_type == Type.INT:
            conv = ASTIntToFloatNode(node.l_child)
            node.l_child = conv
        if node.r_child.node_type == Type.INT:
            conv = ASTIntToFloatNode(node.r_child)
            node.r_child = conv

# Type inference top level
def type_inference(node) -> Type:
    
    if is_leaf_node(node):
        return node.node_type
    
    if is_binop_node(node):
        leftType = type_inference(node.l_child)
        rightType = type_inference(node.r_child)
        if leftType == Type.FLOAT or rightType == Type.FLOAT:
            node.node_type = Type.FLOAT
        else:
            node.node_type = Type.INT
        type_conversion(node)
        if type(node) == ASTEqNode or type(node) == ASTLtNode:
            node.node_type = Type.INT
        return node.node_type
            


