from Scanner.SourcePos import *
from AstGen.Decl import *

class TypeDecl(Decl):
    def __init__(self, tAST, pos):
        super().__init__(pos)
        self.tAST = tAST
    
    def accept(self, v):
        v.visit(self)
