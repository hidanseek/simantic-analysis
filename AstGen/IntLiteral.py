from Scanner.SourcePos import *
from AstGen.Terminal import *

class IntLiteral(Terminal):
    def __init__(self, Lexeme, pos):
        super().__init__(pos)
        self.Lexeme = Lexeme
        self.value = int(Lexeme)
    
    def GetValue(self):
        return self.value
    
    def accept(self, v):
        v.visit(self)
