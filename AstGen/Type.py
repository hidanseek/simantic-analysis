from Scanner.SourcePos import *
from AstGen.AST import *

class Type(AST):
    def __init__(self, pos):
        super().__init__(pos)
    
    @abstractmethod
    def Tequal(self, t):
        pass

    @abstractmethod
    def AssignableTo(self, t):
        pass