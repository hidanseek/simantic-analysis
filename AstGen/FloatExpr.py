from Scanner.SourcePos import *
from AstGen.Expr import *

class FloatExpr(Expr):
    def __init__(self, astFL, pos):
        super().__init__(pos)
        self.astFL = astFL
    
    def accept(self, v):
        v.visit(self)