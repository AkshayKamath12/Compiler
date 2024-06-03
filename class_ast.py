from enum import Enum
from typing import Callable,List,Tuple,Optional


# enum for data types in ClassIeR
class Type(Enum):
    INT = 1
    FLOAT = 2

# base class for an AST node. Each node
# has a type and a VR
class ASTNode():
    def __init__(self) -> None:
        self.node_type = None
        self.vr = None

class ASTLeafNode(ASTNode):
    def __init__(self, value: str) -> None:
        self.value = value
        self.node_type = None
        super().__init__()
        
    def set_node_type(self, nodeType: str) -> None:
        self.node_type = nodeType 
        
    def linearize(self) -> List[str]:
        if self.node_type == Type.INT:
            return ["%s = int2vr(%s);" % (self.vr, self.value)]
        elif self.node_type == Type.FLOAT:
            return ["%s = float2vr(%s);" % (self.vr, self.value)]
            
    def varLinearize(self) -> List[str]:
        return ["%s = %s;" % (self.vr, self.value)]

    def getVal(self) -> str:
        return self.value


class ASTNumNode(ASTLeafNode):
    def __init__(self, value: str) -> None:        
        super().__init__(value)
        self.setType()
    
    def setType(self) -> None:
        if '.' in super().getVal():
            self.node_type = Type.FLOAT
        else:
            self.node_type = Type.INT
    
    def linearize(self) -> List[str]:
        super().set_node_type(self.node_type)
        return super().linearize()


class ASTVarIDNode(ASTLeafNode):
    def __init__(self, value: str, value_type) -> None:
        super().__init__(value)
        self.node_type = value_type
    
    def linearize(self) -> List[str]:
        super().set_node_type(self.node_type)
        return super().varLinearize()

class ASTIOIDNode(ASTLeafNode):
    def __init__(self, value: str, value_type) -> None:
        super().__init__(value)
        self.node_type = value_type
        
    def linearize(self) -> List[str]:
        super().set_node_type(self.node_type)
        return super().linearize()


class ASTBinOpNode(ASTNode):
    def __init__(self, l_child, r_child) -> None:
        self.l_child = l_child
        self.r_child = r_child
        self.node_type = None
        self.operator = ""
        super().__init__()
        
    def setOperator(self, op: str) -> None:
        self.operator = op
        
    def set_node_type(self, nodeType: str) -> None:
        self.node_type = nodeType  
        
    def getOp(self) -> str:
        if self.node_type == Type.INT:
            return self.operator + "i"
        else:
            return self.operator + "f"
            
    def threeAddressCode(self) -> str:
        return "%s = %s(%s, %s);" % (self.vr, self.getOp(), self.l_child.vr, self.r_child.vr)

class ASTPlusNode(ASTBinOpNode):
    def __init__(self, l_child, r_child) -> None:
        super().__init__(l_child,r_child)
        self.node_type = None
           
    def threeAddressCode(self) -> str:
        super().set_node_type(self.node_type)
        super().setOperator("add")
        return super().threeAddressCode()
        
    def linearize(self) -> List[str]:
        return self.l_child.linearize() + self.r_child.linearize() + [self.threeAddressCode()]

class ASTMultNode(ASTBinOpNode):
    def __init__(self, l_child, r_child) -> None:
        super().__init__(l_child,r_child)
        self.node_type = None
        
    def threeAddressCode(self) -> str:
        super().set_node_type(self.node_type)
        super().setOperator("mult")
        return super().threeAddressCode()
        
    def linearize(self) -> List[str]:
        return self.l_child.linearize() + self.r_child.linearize() + [self.threeAddressCode()]

class ASTMinusNode(ASTBinOpNode):
    def __init__(self, l_child, r_child) -> None:
        super().__init__(l_child,r_child)
        self.node_type = None
        
    def threeAddressCode(self) -> str:
        super().set_node_type(self.node_type)
        super().setOperator("sub")
        return super().threeAddressCode()
        
    def linearize(self) -> List[str]:
        return self.l_child.linearize() + self.r_child.linearize() + [self.threeAddressCode()]

class ASTDivNode(ASTBinOpNode):
    def __init__(self, l_child, r_child) ->None:
        super().__init__(l_child,r_child)
        self.node_type = None
        
    def threeAddressCode(self) -> str:
        super().set_node_type(self.node_type)
        super().setOperator("div")
        return super().threeAddressCode()
        
    def linearize(self) -> List[str]:
        return self.l_child.linearize() + self.r_child.linearize() + [self.threeAddressCode()]


class ASTEqNode(ASTBinOpNode):
    def __init__(self, l_child, r_child) ->None:
        self.node_type = Type.INT
        super().__init__(l_child,r_child)
        
    def threeAddressCode(self) -> str:
        super().set_node_type(self.node_type)
        super().setOperator("eq")
        return super().threeAddressCode()
        
    def linearize(self) -> List[str]:
        return self.l_child.linearize() + self.r_child.linearize() + [self.threeAddressCode()]

class ASTLtNode(ASTBinOpNode):
    def __init__(self, l_child, r_child: ASTNode) -> None:
        self.node_type = Type.INT
        super().__init__(l_child,r_child)
        
    def threeAddressCode(self) -> str:
        super().set_node_type(self.node_type)
        super().setOperator("lt")
        return super().threeAddressCode()

    def linearize(self) -> List[str]:
        return self.l_child.linearize() + self.r_child.linearize() + [self.threeAddressCode()]

class ASTUnOpNode(ASTNode):
    def __init__(self, child) -> None:
        self.child = child
        super().__init__()
        
class ASTIntToFloatNode(ASTUnOpNode):
    def __init__(self, child) -> None:
        super().__init__(child)
        self.node_type = Type.FLOAT
        
    def linearize(self) -> List[str]:
        return self.child.linearize() + ["%s = vr_int2float(%s);" % (self.vr, self.child.vr)]

class ASTFloatToIntNode(ASTUnOpNode):
    def __init__(self, child) -> None:
        super().__init__(child)
        self.node_type = Type.INT
        
    def linearize(self) -> List[str]:
        return self.child.linearize() + ["%s = vr_float2int(%s);" % (self.vr, self.child.vr)]
