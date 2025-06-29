from AstGen.Program import Program

from AstGen.EmptyDecl import EmptyDecl
from AstGen.FunDecl import FunDecl

from AstGen.VarDecl import VarDecl
from AstGen.FormalParamDecl import FormalParamDecl
from AstGen.FormalParamDeclSequence import FormalParamDeclSequence
from AstGen.EmptyFormalParamDecl import EmptyFormalParamDecl
from AstGen.DeclSequence import DeclSequence

from AstGen.AssignStmt import AssignStmt
from AstGen.IfStmt import IfStmt
from AstGen.WhileStmt import WhileStmt
from AstGen.ForStmt import ForStmt
from AstGen.ReturnStmt import ReturnStmt
from AstGen.CompoundStmt import CompoundStmt
from AstGen.EmptyCompoundStmt import EmptyCompoundStmt
from AstGen.EmptyStmt import EmptyStmt
from AstGen.StmtSequence import StmtSequence
from AstGen.CallStmt import CallStmt

from AstGen.VarExpr import VarExpr
from AstGen.AssignExpr import AssignExpr
from AstGen.IntExpr import IntExpr
from AstGen.FloatExpr import FloatExpr
from AstGen.BoolExpr import BoolExpr
from AstGen.ArrayExpr import ArrayExpr
from AstGen.StringExpr import StringExpr
from AstGen.BinaryExpr import BinaryExpr
from AstGen.UnaryExpr import UnaryExpr
from AstGen.EmptyExpr import EmptyExpr
from AstGen.ActualParam import ActualParam
from AstGen.EmptyActualParam import EmptyActualParam
from AstGen.ActualParamSequence import ActualParamSequence
from AstGen.CallExpr import CallExpr
from AstGen.ExprSequence import ExprSequence
from AstGen.ID import ID
from AstGen.Operator import Operator
from AstGen.IntLiteral import IntLiteral
from AstGen.FloatLiteral import FloatLiteral
from AstGen.BoolLiteral import BoolLiteral
from AstGen.StringLiteral import StringLiteral
from AstGen.IntType import IntType
from AstGen.FloatType import FloatType
from AstGen.BoolType import BoolType
from AstGen.VoidType import VoidType
from AstGen.StringType import StringType
from AstGen.ArrayType import ArrayType
from AstGen.ErrorType import ErrorType

from AstGen.Visitor import *

from SemanticAnalysis.IdEntry import *

class ScopeStack():
    def __init__(self):
        self.level = 1  # MiniC's global scope is on level 1.
        self.latest = None
    
    # Opens a new level in the scope stack, 1 higher than the
    # current topmost level.

    def openScope(self):
        self.level += 1
    
    # Closes the topmost level in the scope stack, discarding
    # all entries belonging to that level.

    def closeScope(self):
        # Presumably, idTable.level > 0:
        assert self.level > 0
        entry = self.latest
        while entry.level == self.level:
            assert entry.previous != None
            entry = entry.previous

        self.level -= 1
        self.latest = entry
    
    # Makes a new entry in the scope stack for the given identifier
    # and attribute. The new entry belongs to the current level.
    # Returns false iff there is already an entry for the
    # same identifier at the current level.

    def enter(self, id, declAST):
        entry = self.latest
        searching = True

        # Check for duplicate entry ...
        while searching:
            if entry == None or entry.level < self.level:
                searching = False
            elif entry.id == id:
                # duplicate entry detected:
                return False
            else:
                entry = entry.previous

        # "id" does not exist on this scope level, add new entry for "id":...
        entry = IdEntry(id, declAST, self.level, self.latest)
        self.latest = entry
        return True
    
    # Finds an entry for the given identifier in the scope stack,
    # if any. If there are several entries for that identifier, finds the
    # entry at the highest level, in accordance with the scope rules.
    # Returns null iff no entry is found.
    # Otherwise returns the declAST field of the scope stack entry found.

    def retrieve(self, id):
        declAST = None
        searching = True

        entry = self.latest
        while searching:
            if entry == None:
                searching = False
            elif entry.id == id:
                searching = False
                declAST = entry.declAST
            else:
                entry = entry.previous
        return declAST
    