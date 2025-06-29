from Scanner.SourcePos import *
from AstGen.Type import *
from AstGen.ErrorType import *

class BoolType(Type):
    def __init__(self, pos):
        super().__init__(pos)
    
    def accept(self, v):
        v.visit(self)

    def Tequal(self, t):
        if t != None and isinstance(t, ErrorType):
            return True
        else:
            return t != None and isinstance(t, BoolType)
    
    def AssignableTo(self, t):
        #BoolType assignable to t ?
        if t != None and isinstance(t, ErrorType):
            return True
        else:
            return t != None and isinstance(t, BoolType)