from Scanner.SourcePos import *

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

from AstGen.TypeDecl import TypeDecl
from AstGen.Type import Type
from AstGen.FunDecl import FunDecl

from AstGen.Visitor import *

class StdEnvironment():
    # The pre-defined language environment for MiniC:
    
    # ASTs representing the MiniC standard type declarations: (TypeDecl)
    intTypeDecl = None
    boolTypeDecl = None
    floatTypeDecl = None
    stringTypeDecl = None
    voidTypeDecl = None
    errorTypeDecl = None

    # ASTs representing the MiniC standard types: (Type)
    intType = None
    boolType = None
    floatType = None
    stringType = None
    voidType = None
    errorType = None

    # ASTs representing the declarations of our pre-defined MiniC functions: (FunDecl)
    getInt = None
    putInt = None
    getBool = None
    putBool = None
    getFloat = None
    putFloat = None
    getString = None
    putString = None
    putLn = None

    AST = None  # Program()

    dummyPos = SourcePos() # SourcePos()

    def __init__(self):
        D = None
        pDecl = None
        pSeq = None
        '''
            Generate the declarations for the StdEnvironment,
            generate an AST, so that it can be traversed and printed:
        '''
        StdEnvironment.intType = IntType(StdEnvironment.dummyPos)
        StdEnvironment.boolType = BoolType(StdEnvironment.dummyPos)
        StdEnvironment.floatType = FloatType(StdEnvironment.dummyPos)
        StdEnvironment.stringType = StringType(StdEnvironment.dummyPos)
        StdEnvironment.voidType = VoidType(StdEnvironment.dummyPos)
        StdEnvironment.errorType = ErrorType(StdEnvironment.dummyPos)

        StdEnvironment.putLn = FunDecl(StdEnvironment.voidType,
                        ID("putLn", StdEnvironment.dummyPos),
                        EmptyFormalParamDecl(StdEnvironment.dummyPos),
                        EmptyCompoundStmt(StdEnvironment.dummyPos),
                        StdEnvironment.dummyPos)
        D = DeclSequence(StdEnvironment.putLn, EmptyDecl(StdEnvironment.dummyPos), StdEnvironment.dummyPos)

        pDecl = FormalParamDecl(StdEnvironment.stringType, ID("s", StdEnvironment.dummyPos), StdEnvironment.dummyPos)
        pSeq = FormalParamDeclSequence(pDecl, EmptyFormalParamDecl(StdEnvironment.dummyPos), StdEnvironment.dummyPos)
        StdEnvironment.putString = FunDecl(StdEnvironment.voidType,
                            ID("putString", StdEnvironment.dummyPos),
                            pSeq,
                            EmptyCompoundStmt(StdEnvironment.dummyPos),
                            StdEnvironment.dummyPos)
        D = DeclSequence(StdEnvironment.putString, D, StdEnvironment.dummyPos)

        StdEnvironment.getString = FunDecl(StdEnvironment.stringType,
                            ID("getString", StdEnvironment.dummyPos),
                            EmptyFormalParamDecl(StdEnvironment.dummyPos),
                            EmptyCompoundStmt(StdEnvironment.dummyPos),
                            StdEnvironment.dummyPos)
        D = DeclSequence(StdEnvironment.getString, D, StdEnvironment.dummyPos)

        pDecl = FormalParamDecl(StdEnvironment.floatType, 
                                ID("f", StdEnvironment.dummyPos),
                                StdEnvironment.dummyPos)
        pSeq = FormalParamDeclSequence(pDecl,
                                       EmptyFormalParamDecl(StdEnvironment.dummyPos),
                                       StdEnvironment.dummyPos)
        StdEnvironment.putFloat = FunDecl(StdEnvironment.voidType,
                           ID("putFloat", StdEnvironment.dummyPos),
                           pSeq,
                           EmptyCompoundStmt(StdEnvironment.dummyPos),
                           StdEnvironment.dummyPos)
        D = DeclSequence(StdEnvironment.putFloat, D, StdEnvironment.dummyPos)

        StdEnvironment.getFloat = FunDecl(StdEnvironment.floatType,
                           ID("getFloat", StdEnvironment.dummyPos),
                           EmptyFormalParamDecl(StdEnvironment.dummyPos),
                           EmptyCompoundStmt(StdEnvironment.dummyPos),
                           StdEnvironment.dummyPos)
        D = DeclSequence(StdEnvironment.getFloat, D, StdEnvironment.dummyPos)

        pDecl = FormalParamDecl(StdEnvironment.boolType, 
                                ID("b", StdEnvironment.dummyPos),
                                StdEnvironment.dummyPos)
        pSeq = FormalParamDeclSequence(pDecl,
                                       EmptyFormalParamDecl(StdEnvironment.dummyPos),
                                       StdEnvironment.dummyPos)
        StdEnvironment.putBool = FunDecl(StdEnvironment.voidType,
                          ID("putBool", StdEnvironment.dummyPos),
                          pSeq,
                          EmptyCompoundStmt(StdEnvironment.dummyPos),
                          StdEnvironment.dummyPos)
        D = DeclSequence(StdEnvironment.putBool, D, StdEnvironment.dummyPos)

        StdEnvironment.getBool = FunDecl(StdEnvironment.boolType,
                          ID("getBool", StdEnvironment.dummyPos),
                          EmptyFormalParamDecl(StdEnvironment.dummyPos),
                          EmptyCompoundStmt(StdEnvironment.dummyPos),
                          StdEnvironment.dummyPos)
        D = DeclSequence(StdEnvironment.getBool, D, StdEnvironment.dummyPos)

        pDecl = FormalParamDecl(StdEnvironment.intType,
                                ID("i", StdEnvironment.dummyPos),
                                StdEnvironment.dummyPos)
        pSeq = FormalParamDeclSequence(pDecl,
                                       EmptyFormalParamDecl(StdEnvironment.dummyPos),
                                       StdEnvironment.dummyPos)
        StdEnvironment.putInt = FunDecl(StdEnvironment.voidType,
                         ID("putInt", StdEnvironment.dummyPos),
                         pSeq,
                         EmptyCompoundStmt(StdEnvironment.dummyPos),
                         StdEnvironment.dummyPos)
        D = DeclSequence(StdEnvironment.putInt, D, StdEnvironment.dummyPos)

        StdEnvironment.getInt = FunDecl(StdEnvironment.intType,
                         ID("getInt", StdEnvironment.dummyPos),
                         EmptyFormalParamDecl(StdEnvironment.dummyPos),
                         EmptyCompoundStmt(StdEnvironment.dummyPos),
                         StdEnvironment.dummyPos)
        D = DeclSequence(StdEnvironment.getInt, D, StdEnvironment.dummyPos)

        StdEnvironment.errorTypeDecl = TypeDecl(StdEnvironment.errorType, StdEnvironment.dummyPos)
        D = DeclSequence(StdEnvironment.errorTypeDecl, D, StdEnvironment.dummyPos)
        
        StdEnvironment.voidTypeDecl = TypeDecl(StdEnvironment.voidType, StdEnvironment.dummyPos)
        D = DeclSequence(StdEnvironment.voidTypeDecl, D, StdEnvironment.dummyPos)

        StdEnvironment.stringTypeDecl = TypeDecl(StdEnvironment.stringType, StdEnvironment.dummyPos)
        D = DeclSequence(StdEnvironment.stringTypeDecl, D, StdEnvironment.dummyPos)

        StdEnvironment.floatTypeDecl = TypeDecl(StdEnvironment.floatType, StdEnvironment.dummyPos)
        D = DeclSequence(StdEnvironment.floatTypeDecl, D, StdEnvironment.dummyPos)

        StdEnvironment.boolTypeDecl = TypeDecl(StdEnvironment.boolType, StdEnvironment.dummyPos)
        D = DeclSequence(StdEnvironment.boolTypeDecl, D, StdEnvironment.dummyPos)

        StdEnvironment.intTypeDecl = TypeDecl(StdEnvironment.intType, StdEnvironment.dummyPos)
        D = DeclSequence(StdEnvironment.intTypeDecl, D, StdEnvironment.dummyPos)

        StdEnvironment.AST = Program(D, StdEnvironment.dummyPos)
