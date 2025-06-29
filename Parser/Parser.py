from Scanner.SourcePos import *
from Scanner.Token import *
from Scanner.SourcePos import *
from Scanner.Scanner import *
from Parser.SyntaxError import *
from ErrorReporter import *

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

class Parser:
    #
    # NOTE:
    #
    # This is a dummy parser implementation that is only used when the
    # course participant wishes to use the provided parser class file.
    # The dummy implementation makes the MiniC framework compileable.
    # After compiling, the class-file of the dummy parser is replaced
    # by the provided parser's class file.
    #
    # Students who wish to use their own parser should replace this file with
    # their own parser from Assignment 1.
    def __init__(self, lexer, reporter):
        print("ERROR: empty parser implementation used!")
        print("Provide your own Parser.py or use the provided pyc files!")
        print("See the Assignment specification on how to use the provided pre-compiled python files.")
        exit(1)
    
    def parse(self):
        ProgramAST = None
        return ProgramAST
