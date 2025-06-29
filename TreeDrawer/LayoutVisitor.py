from functools import singledispatchmethod

from AstGen.Visitor import Visitor
from Scanner.SourcePos import SourcePos

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
from StdEnvironment import *

from graphviz import Digraph

class LayoutVisitor(Visitor):
    visit = Visitor.visit

    def __init__(self, caption=None):
        self.graph = Digraph(format='png')
        self.counter = 0
        self.parent_stack = []
        self.graph.attr(bgcolor='#dddddd', nodesep='0.5', fixedsize='false',
                        rankdir='TB', ranksep='0.6') #ranksep='0.5', nodesep='0.8')
        self.graph.attr('node', shape='box', fontname='Arial Bold', fontsize='18', penwidth='2',
                        style='filled', fillcolor='white', fixedsize='false', margin='0.05')
        self.graph.attr('edge', arrowhead='none')

        self.caption = caption
        self.IsGlobal = True
        self.TypeInfo = True
        #if caption:
        #    self.graph.attr(label=caption, labelloc='t', fontsize='20')
    
    def _new_node(self, label):
        node_id = f"n{self.counter}"
        self.graph.node(node_id, label)
        self.counter += 1
        return node_id
    
    def _add_node(self, label):
        node_id = self._new_node(label)
        if self.parent_stack:
            self.graph.edge(self.parent_stack[-1], node_id)
        return node_id
    
    def FormatPosition(self, pos):
        if self.caption:
            return ' ' + str(pos.StartLine) + '(' + str(pos.StartCol) + ')..'\
                       + str(pos.EndLine) + '(' + str(pos.EndCol) + ')'
        else:
            return ''
    
    def TypeTag(self, t: Type):
        l = ""
        if t == None:
            l = "<?>"
        elif t.Tequal(StdEnvironment.intType):
            l = "<int>"
        elif t.Tequal(StdEnvironment.boolType):
            l = "<bool>"
        elif t.Tequal(StdEnvironment.floatType):
            l = "<float>"
        elif t.Tequal(StdEnvironment.stringType):
            l = "<string>"
        elif t.Tequal(StdEnvironment.voidType):
            l = "<void>"
        elif isinstance(t, ArrayType):
            l = "<array>"
        elif isinstance(t, ErrorType):  # .Tequal(StdEnvironment.errorType)
            l = "<error>"
        else:
            assert False
        return l
    
    @singledispatchmethod
    def visit(self, x):
        return super().visit(x)
    
    @visit.register
    def _(self, x: Program):
        node_id = self._add_node("Program")
        self.parent_stack.append(node_id)
        x.D.accept(self)
        self.parent_stack.pop()

    @visit.register
    def _(self, x: EmptyDecl):
        self._add_node("EmptyDecl")
    
    @visit.register
    def _(self, x: FunDecl):
        self.IsGlobal = False
        node_id = self._add_node("FunDecl")
        self.parent_stack.append(node_id)
        x.tAST.accept(self)
        x.idAST.accept(self)
        x.paramsAST.accept(self)
        x.stmtAST.accept(self)
        self.parent_stack.pop()
        self.IsGlobal = True
    
    @visit.register
    def _(self, x: TypeDecl):
        node_id = self._add_node("TypeDecl")
        self.parent_stack.append(node_id)
        x.tAST.accept(self)
        self.parent_stack.pop()

    @visit.register
    def _(self, x: FormalParamDecl):
        node_id = self._add_node("FormalParamDecl")
        self.parent_stack.append(node_id)        
        x.astType.accept(self)
        x.astIdent.accept(self)
        self.parent_stack.pop()
    
    @visit.register
    def _(self, x: FormalParamDeclSequence):
        node_id = self._add_node("FormalParamDeclSeq")
        self.parent_stack.append(node_id)
        x.lAST.accept(self)
        x.rAST.accept(self)
        self.parent_stack.pop()
    
    @visit.register
    def _(self, x: EmptyFormalParamDecl):
        self._add_node("EmptyFormalParamDecl")
        
    @visit.register
    def _(self, x: StmtSequence):
        node_id = self._add_node("StmtSeq")
        self.parent_stack.append(node_id)
        x.s1AST.accept(self)
        x.s2AST.accept(self)
        self.parent_stack.pop()

    @visit.register
    def _(self, x: AssignStmt):
        node_id = self._add_node("AssignStmt")
        self.parent_stack.append(node_id)
        x.lAST.accept(self)
        x.rAST.accept(self)
        self.parent_stack.pop()
    
    @visit.register
    def _(self, x: IfStmt):
        node_id = self._add_node("IfStmt")
        self.parent_stack.append(node_id)
        x.eAST.accept(self)
        x.thenAST.accept(self)
        if x.elseAST is not None:
            x.elseAST.accept(self)
        self.parent_stack.pop()
    
    @visit.register
    def _(self, x: WhileStmt):
        node_id = self._add_node("WhileStmt")
        self.parent_stack.append(node_id)
        x.eAST.accept(self)
        x.stmtAST.accept(self)
        self.parent_stack.pop()
    
    @visit.register
    def _(self, x: ForStmt):
        node_id = self._add_node("ForStmt")
        self.parent_stack.append(node_id)
        x.e1AST.accept(self)
        x.e2AST.accept(self)
        x.e3AST.accept(self)
        x.stmtAST.accept(self)
        self.parent_stack.pop()
    
    @visit.register
    def _(self, x: ReturnStmt):
        node_id = self._add_node("ReturnStmt")
        self.parent_stack.append(node_id)
        x.eAST.accept(self)
        self.parent_stack.pop()
    
    @visit.register
    def _(self, x: CompoundStmt):
        node_id = self._add_node("CompoundStmt")
        self.parent_stack.append(node_id)
        x.astDecl.accept(self)
        x.astStmt.accept(self)
        self.parent_stack.pop()
    
    @visit.register
    def _(self, x: EmptyCompoundStmt):
        self._add_node("EmptyCompoundStmt")
    
    @visit.register
    def _(self, x: EmptyStmt):
        self._add_node("EmptyStmt")
    
    @visit.register
    def _(self, x: CallStmt):
        node_id = self._add_node("CallStmt")
        self.parent_stack.append(node_id)
        x.eAST.accept(self)
        self.parent_stack.pop()
    
    @visit.register
    def _(self, x: VarDecl):
        l = "VarDecl"
        if self.IsGlobal:
            l = "G." + l
        else:
            l = "L." + l
        node_id = self._add_node(l)
        self.parent_stack.append(node_id)
        x.tAST.accept(self)
        x.idAST.accept(self)
        x.eAST.accept(self)
        self.parent_stack.pop()
    
    @visit.register
    def _(self, x: DeclSequence):
        node_id = self._add_node("DeclSeq")
        self.parent_stack.append(node_id)
        x.D1.accept(self)
        x.D2.accept(self)
        self.parent_stack.pop()
    
    @visit.register
    def _(self, x: VarExpr):
        if self.TypeInfo:
            l = self.TypeTag(x.type)
        node_id = self._add_node("VarExpr" + l)
        self.parent_stack.append(node_id)
        x.Ident.accept(self)
        self.parent_stack.pop()
    
    @visit.register
    def _(self, x: AssignExpr):
        node_id = self._add_node("AssignExpr")
        self.parent_stack.append(node_id)
        x.lAST.accept(self)
        x.rAST.accept(self)
        self.parent_stack.pop()
    
    @visit.register
    def _(self, x: IntExpr):
        if self.TypeInfo:
            l = self.TypeTag(x.type)
        node_id = self._add_node("IntExpr" + l)
        self.parent_stack.append(node_id)
        x.astIL.accept(self)
        self.parent_stack.pop()
    
    @visit.register
    def _(self, x: FloatExpr):
        if self.TypeInfo:
            l = self.TypeTag(x.type)
        node_id = self._add_node("FloatExpr" + l)
        self.parent_stack.append(node_id)
        x.astFL.accept(self)
        self.parent_stack.pop()
    
    @visit.register
    def _(self, x: BoolExpr):
        if self.TypeInfo:
            l = self.TypeTag(x.type)
        node_id = self._add_node("BoolExpr" + l)
        self.parent_stack.append(node_id)
        x.astBL.accept(self)
        self.parent_stack.pop()
    
    @visit.register
    def _(self, x: StringExpr):
        if self.TypeInfo:
            l = self.TypeTag(x.type)
        node_id = self._add_node("StringExpr" + l)
        self.parent_stack.append(node_id)
        x.astSL.accept(self)
        self.parent_stack.pop()
    
    @visit.register
    def _(self, x: ArrayExpr):
        if self.TypeInfo:
            l = self.TypeTag(x.type)
        node_id = self._add_node("ArrayExpr" + l)
        self.parent_stack.append(node_id)
        x.idAST.accept(self)
        x.indexAST.accept(self)
        self.parent_stack.pop()
    
    @visit.register
    def _(self, x: BinaryExpr):
        if self.TypeInfo:
            l = self.TypeTag(x.type)
        node_id = self._add_node("BinaryExpr" + l)
        self.parent_stack.append(node_id)
        x.lAST.accept(self)
        x.oAST.accept(self)
        x.rAST.accept(self)
        self.parent_stack.pop()
    
    @visit.register
    def _(self, x: UnaryExpr):
        if self.TypeInfo:
            l = self.TypeTag(x.type)
        node_id = self._add_node("UnaryExpr" + l)
        self.parent_stack.append(node_id)
        x.oAST.accept(self)
        x.eAST.accept(self)
        self.parent_stack.pop()
    
    @visit.register
    def _(self, x: EmptyExpr):
        self._add_node("EmptyExpr")
    
    @visit.register
    def _(self, x: ActualParam):
        if self.TypeInfo:
            l = self.TypeTag(x.type)
        node_id = self._add_node("ActualParam" + l)
        self.parent_stack.append(node_id)
        x.pAST.accept(self)
        self.parent_stack.pop()
    
    @visit.register
    def _(self, x: EmptyActualParam):
        self._add_node("EmptyActualParam")
    
    @visit.register
    def _(self, x: ActualParamSequence):
        node_id = self._add_node("ActualParamSeq")
        self.parent_stack.append(node_id)
        x.lAST.accept(self)
        x.rAST.accept(self)
        self.parent_stack.pop()
    
    @visit.register
    def _(self, x: CallExpr):
        if self.TypeInfo:
            l = self.TypeTag(x.type)
        node_id = self._add_node("CallExpr" + l)
        self.parent_stack.append(node_id)
        x.idAST.accept(self)
        x.paramAST.accept(self)
        self.parent_stack.pop()
    
    @visit.register
    def _(self, x: ExprSequence):
        node_id = self._add_node("ExprSeq")
        self.parent_stack.append(node_id)
        x.lAST.accept(self)
        x.rAST.accept(self)
        self.parent_stack.pop()
    
    @visit.register
    def _(self, x: ID):
        self._add_node(x.Lexeme)
    
    @visit.register
    def _(self, x: Operator):
        if self.TypeInfo:
            l = self.TypeTag(x.type)
        self._add_node(x.Lexeme + l)
    
    @visit.register
    def _(self, x: IntLiteral):
        self._add_node(x.Lexeme)
    
    @visit.register
    def _(self, x: FloatLiteral):
        self._add_node(x.Lexeme)
    
    @visit.register
    def _(self, x: BoolLiteral):
        self._add_node(x.Lexeme)
    
    @visit.register
    def _(self, x: StringLiteral):
        self._add_node(x.Lexeme)
    
    @visit.register
    def _(self, x: IntType):
        self._add_node("int")
    
    @visit.register
    def _(self, x: FloatType):
        self._add_node("float")
    
    @visit.register
    def _(self, x: BoolType):
        self._add_node("bool")
    
    @visit.register
    def _(self, x: StringType):
        self._add_node("string")
    
    @visit.register
    def _(self, x: VoidType):
        self._add_node("void")
    
    @visit.register
    def _(self, x: ArrayType):
        node_id = self._add_node("ArrayType")
        self.parent_stack.append(node_id)
        x.astType.accept(self)
        x.astExpr.accept(self)
        self.parent_stack.pop()
    
    @visit.register
    def _(self, x: ErrorType):
        self._add_node("Error")

    def render(self, filename='ast', view=False):
        self.graph.render(filename, view=view, cleanup=True)        
    