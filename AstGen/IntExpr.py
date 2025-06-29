from Scanner.SourcePos import *
from AstGen.Expr import *

class IntExpr(Expr):
    def __init__(self, astIL, pos):
        super().__init__(pos)
        assert astIL != None
        self.astIL = astIL
    
    def GetValue(self):
        return self.astIL.GetValue()

    def accept(self, v):
        v.visit(self)
