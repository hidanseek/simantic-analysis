from Scanner.SourcePos import *
from AstGen.Type import *
from AstGen.ErrorType import *
from AstGen.IntExpr import IntExpr

class ArrayType(Type):
    def __init__(self, astType, astExpr, pos):
        super().__init__(pos)
        self.astType = astType
        self.astExpr = astExpr
    
    def accept(self, v):
        v.visit(self)

    def Tequal(self, t):
        if t != None and isinstance(t, ErrorType):
            return True
        else:
            return False

    def AssignableTo(self, t):
        assert t != None
        if isinstance(t, ArrayType):
            # Arrays we consider "assignable" if they have the same
            # element type and the same size
            arrT = t
            eTypeSame = self.astType.Tequal(arrT.astType)
            return eTypeSame and (arrT.GetRange() == self.GetRange())
    
    def GetRange(self):
        assert isinstance(self.astExpr, IntExpr)
        return self.astExpr.GetValue()