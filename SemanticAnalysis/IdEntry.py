from AstGen.Decl import *

class IdEntry():
    def __init__(self, id, declAST, level, previous):
        self.id = id
        self.declAST = declAST
        self.level = level
        self.previous = previous
