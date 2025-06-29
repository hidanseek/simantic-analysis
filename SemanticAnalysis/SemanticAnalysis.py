from ErrorReporter import *
from StdEnvironment import *
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

from AstGen.Visitor import *

from ErrorReporter import *
from StdEnvironment import *
from Scanner.SourcePos import *

from SemanticAnalysis.ScopeStack import *

class SemanticAnalysis(Visitor):
    def __init__(self, reporter):
        self.reporter = reporter
        self.scopeStack = ScopeStack()
        self.IsFunctionBlock = None
        self.currentFunctionReturnType = None
        # Here we enter the entities from the StdEnvironment into the scope stack:
        # The scope stack is on level 1 now (initial setting).
        self.scopeStack.enter("int", StdEnvironment.intTypeDecl)
        self.scopeStack.enter("bool", StdEnvironment.boolTypeDecl)
        self.scopeStack.enter("float", StdEnvironment.floatTypeDecl)
        self.scopeStack.enter("void", StdEnvironment.voidTypeDecl)
        self.scopeStack.enter("getInt", StdEnvironment.getInt)
        self.scopeStack.enter("putInt", StdEnvironment.putInt)
        self.scopeStack.enter("getBool", StdEnvironment.getBool)
        self.scopeStack.enter("putBool", StdEnvironment.putBool)
        self.scopeStack.enter("getFloat", StdEnvironment.getFloat)
        self.scopeStack.enter("putFloat", StdEnvironment.putFloat)
        self.scopeStack.enter("getString", StdEnvironment.getString)
        self.scopeStack.enter("putString", StdEnvironment.putString)
        self.scopeStack.enter("putLn", StdEnvironment.putLn)
    
    '''
        Prints the name of a class, useful for debugging...

        def PrintClassName(t):
            print("The class of", t, "is", t.getName())
    '''

    # For FunDecl, VarDecl and FormalParamDecl, this function returns
    # the type of the declaration.
    # 1) for functions declarations, this is the return type of the function
    # 2) for variable declarations, this is the type of the variable

    def typeOfDecl(self, d):
        if d == None:
            return StdEnvironment.errorType
        assert isinstance(d, FunDecl) or isinstance(d, VarDecl) or isinstance(d, FormalParamDecl)
        if isinstance(d, FunDecl):
            T = d.tAST
        elif isinstance(d, VarDecl):
            T = d.tAST
        else:
            T = d.astType
        return T
    
    # This function returns the element type of an ArrayType AST node.
    def typeOfArrayType(self, d):
        assert d != None
        assert isinstance(d, ArrayType)
        T = d
        return T.astType
    
    # This function returns true, if an operator accepts integer or
    # floating point arguments.
    #  <int> x <int> -> <sometype>
    #  <float> x <float> -> <sometype>
    def HasIntOrFloatArgs(self, op):
        return (op.Lexeme == '+' or 
                op.Lexeme == '-' or
                op.Lexeme == '*' or
                op.Lexeme == '/' or
                op.Lexeme == '<' or
                op.Lexeme == '<=' or
                op.Lexeme == '>' or
                op.Lexeme == '>=' or
                op.Lexeme == '==' or
                op.Lexeme == '!=')
    
    # This function returns true, if an operator accepts bool arguments.
    #  <bool> x <bool> -> <sometype>
    def HasBoolArgs(self, op):
        return (op.Lexeme == '&&' or
                op.Lexeme == '||' or
                op.Lexeme == '!' or
                op.Lexeme == '!=' or
                op.Lexeme == '==')
    
    # This function returns true, if an operator returns a bool value.
    #  <sometype> x <sometype> -> bool
    def HasBoolReturnType(self, op):
        return (op.Lexeme == '&&' or
                op.Lexeme == '||' or
                op.Lexeme == '!' or
                op.Lexeme == '!=' or
                op.Lexeme == '==' or
                op.Lexeme == '<' or
                op.Lexeme == '<=' or
                op.Lexeme == '>' or
                op.Lexeme == '>=')
    
    # This function performs coercion of an integer-valued expression e.
    # It creates an i2f operator and a unary expression.
    # Expression e becomes the expression-AST of this unary expression.
    #
    #       Expr AST for e <int>
    #
    # =>
    #
    #       UnaryExpr <float>
    #         |     \
    #         |      \
    #         |       \
    #       i2f<int>  Expr AST for e <int>
    #
    def i2f(self, e):
        op = Operator('i2f', SourcePos())
        op.type = StdEnvironment.intType
        eAST = UnaryExpr(op, e, SourcePos())
        eAST.type = StdEnvironment.floatType
        return eAST
    
    # Given a function declaration FunDecl, this method returns the number
    # of formal parameters. E.g., for the following function
    #
    #    void foo (int a, bool b){}
    #
    # the return value will be 2.
    # Note: this function assumes the AST tree layout from Assignment 3.
    def GetNrOfFormalParams(self, f):
        NrArgs = 0
        D = f.paramsAST
        assert isinstance(D, EmptyFormalParamDecl) or isinstance(D, FormalParamDeclSequence)
        if isinstance(D, EmptyFormalParamDecl):
            return 0
        while isinstance(D, FormalParamDeclSequence):
            NrArgs+=1
            D = D.rAST
            assert isinstance(D, EmptyFormalParamDecl) or isinstance(D, FormalParamDeclSequence)
        return NrArgs
    
    # Given a function declaration FunDecl, this method returns the AST for 
    # the formal parameter nr (nr is the number of the parameter).
    # E.g., for the following function and nr=2,
    #
    #    void foo (int a, bool b){}
    #
    # the AST returned will be "bool b".
    # Note: this function assumes the AST tree layout from Assignment 3.
    def GetFormalParam(self, f, nr):
        fArgs = self.GetNrOfFormalParams(f)
        assert fArgs >= 0
        assert nr <= fArgs
        S = f.paramsAST
        for i in range(1, nr):
            assert isinstance(S.rAST, FormalParamDeclSequence)
            S = S.rAST
        assert isinstance(S.lAST, FormalParamDecl)
        return S.lAST
    
    # Get the number of actual parameters of a function call expression:
    # Similar to GetNrOfFormalParams above.
    # Note: this function assumes the AST tree layout from Assignment 3.
    def GetNrOfActualParams(self, f):
        NrArgs = 0
        P = f.paramAST
        assert isinstance(P, EmptyActualParam) or isinstance(P, ActualParamSequence)
        if isinstance(P, EmptyActualParam):
            return 0
        while isinstance(P, ActualParamSequence):
            NrArgs += 1
            P = P.rAST
            assert isinstance(P, EmptyActualParam) or isinstance(P, ActualParamSequence)
        return NrArgs
    
    # Given a function call expression, get the actual parameter nr
    # (nr is the number of the parameter).
    # Similar to GetFormalParam above.
    # Note: this function assumes the AST tree layout from Assignment 3.
    def GetActualParam(self, f, nr):
        aArgs = self.GetNrOfActualParams(f)
        P = f.paramAST
        assert aArgs >= 0
        assert nr <= aArgs
        for i in range(1, nr):
            assert isinstance(P, ActualParamSequence)
            P = P.rAST
        assert isinstance(P.lAST, ActualParam)
        return P.lAST
    
    # Given a type t, this function can be used to print the type.
    # Useful for debuggging, a similar mechanism is used in the
    # TreeDrawer Visitor.
    '''
        def TypeTag (self, t) {
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
            elif isinstance(t, ErrorType):
                l = "<error>"
            else:
                assert False
            return l
    '''

    # This array of strings contains the error messages that we generate
    # for errors detected during semantic analysis. These messages are
    # output using the ErrorReporter.
    # Example: reporter.reportError(errMsg[0], "", SourcePos())
    #          will print "ERROR #0: main function is missing".

    errMsg = (
        '#0: main function missing',
        "#1: return type of main must be int",

        #defining occurrences of identifiers,
        #for local, global variables and for formal parameters:
        "#2: identifier redeclared",
        "#3: identifier declared void",
        "#4: identifier declared void[]",

        #applied occurrences of identifiers:
        "#5: undeclared identifier",

        #assignment statements:
        "#6: incompatible types for =",
        "#7: invalid lvalue in assignment",

        #expression types:
        "#8: incompatible type for return statement",
        "#9: incompatible types for binary operator",
        "#10: incompatible type for unary operator",

        #scalars:
        "#11: attempt to use a function as a scalar",

        #arrays:
        "#12: attempt to use scalar/function as an array",
        "#13: wrong type for element in array initializer",
        "#14: invalid initializer: array initializer for scalar",
        "#15: invalid initializer: scalar initializer for array",
        "#16: too many elements in array initializer",
        "#17: array subscript is not an integer",
        "#18: array size missing",

        #functions:
        "#19: attempt to reference a scalar/array as a function",

        #conditional expressions:
        '#20: "if" conditional is not of type boolean',
        '#21: "for" conditional is not of type boolean',
        '#22: "while" conditional is not of type boolean',

        #parameters:
        "#23: too many actual parameters",
        "#24: too few actual parameters",
        "#25: wrong type for actual parameter"
    )

    @singledispatchmethod
    def visit(self, x):
        return super().visit(x)
    
    # Checks whether the source program, represented by its AST, satisfies the
    # language's scope rules and type rules.
    # Decorates the AST as follows:
    #  (a) Each applied occurrence of an identifier or operator is linked to
    #      the corresponding declaration of that identifier or operator.
    #  (b) Each expression and value-or-variable-name is decorated by its type.

    def check(self, progAST: Program):
        self.visit(progAST)
        # STEP 3:
        # Check Error 0
        #
        # Retrieve "main" from the scope stack. If it is not there (null is
        # returned, then the program does not contain a main function.
        
        # Start of your code:
        
        # End of your code
    
    @visit.register
    def _(self, x: Program):
        x.D.accept(self)
    
    @visit.register
    def _(self, x: EmptyDecl):
        pass

    @visit.register
    def _(self, x: FunDecl):
        self.currentFunctionReturnType = x.tAST
        # STEP 1:
        # Enter this function in the scope stack. Return Error 2 if this
        # name is already present in this scope.

        # Start of your code:

        # End of your code

        
        # STEP 3:
        # Check Error 1: 
        # If this function is the "main" function, then ensure that
        # x.tAST is of type int.

        # Start of your code: 

        # End of your code 

        # STEP 1:
        # Open a new scope in the scope stack. This will be the scope for the
        # function's formal parameters and the function's body.
        # We will close this scope in the visit procedure of this
        # function's compound_stmt.

        # Start of your code: 

        # End of your code


        # The following flag is needed when we visit compound statements {...},
        # to avoid opening a fresh scope for function bodies (because we have
        # already opened one, for the formal parameters).
        self.IsFunctionBlock = True     # needed in {...}, to avoid opening a fresh scope.
        
        x.paramsAST.accept(self)
        x.stmtAST.accept(self)

    @visit.register
    def _(self, x: TypeDecl):
        assert False    # TypeDecl nodes occur only in the StdEnvironment AST.
    
    @visit.register
    def _(self, x: FormalParamDecl):
        if isinstance(x.astType, ArrayType):
            (x.astType).astExpr.accept(self)
        # STEP 1:
        # Here we visit the declaration of a formal parameter. You should enter
        # the lexeme x.astIdent.Lexeme together with its declaration x into
        # the scope stack. If this name is already present in the current scope,
        # the scope stack enter method will return false. You should report
        # Error 2 in that case.

        # Start of your code:

        # End of your code

        # STEP 3:
        # Check that the formal parameter is not of type void or void[]. 
        # Report error messages 3 and 4 respectively:

        # Start of your code:

        # End of your code
    
    @visit.register
    def _(self, x: FormalParamDeclSequence):
        x.lAST.accept(self)
        x.rAST.accept(self)
        
    @visit.register
    def _(self, x: EmptyFormalParamDecl):
        pass

    @visit.register
    def _(self, x: StmtSequence):
        x.s1AST.accept(self)
        x.s2AST.accept(self)
    
    @visit.register
    def _(self, x: AssignStmt):
        x.lAST.accept(self)
        x.rAST.accept(self)
        #STEP 2:
        # Here we type-check assignment statements
        # Two conditions must be ensured:
        # 1) The type of the right-hand side of the assignment statement
        #    (x.rAST.type) must be assignment-compatible
        #    to the left-hand side of the assignment statement.
        #    You can use x.rAST.type.AssignableTo to test assignment-compatibility
        #    of the type of the left-hand side (x.lAST.type).
        # 2) If 2 types are assignment-compatible, then we need to check
        #    whether a coercion from int to float is needed. You can use
        #    x.lAST.type.Tequal(StdEnvironment.floatType) to check whether
        #    the left-hand side is of type float. Check the right-hand side
        #    for type int and use i2f if a coercion is needed. Hint: the return
        #    statement uses a similar mechanism....
        # If conditions (1) or (2) are violated, then you should report Error 6.

        # Start of your code: 

        # End of your code 
        
        if (not isinstance(x.lAST, VarExpr)) and (not isinstance(x.lAST, ArrayExpr)):
            self.reporter.reportError(self.errMsg[7], "", x.lAST.pos)
    
    @visit.register
    def _(self, x: IfStmt):
        x.eAST.accept(self)
        #STEP 2:
        # Here we are visiting an if statement. If the condition x.eAST.type
        # is not of type bool, we have to issue Error 20. You can have a
        # look at "for" loops, which use a similar check for the loop condition.

        # Start of your code:

        # End of your code
        x.thenAST.accept(self)
        if x.elseAST != None:
            x.elseAST.accept(self)
    
    @visit.register
    def _(self, x: WhileStmt):
        x.eAST.accept(self)
        #STEP 2:
        # Here we are visiting a while statement. If the loop condition
        # is not of type bool, we have to issue Error 22. You can have a
        # look at "for" loops which use a similar check.

        # Start of your code:

        # End of your code
        x.stmtAST.accept(self)
    
    @visit.register
    def _(self, x: ForStmt):
        x.e1AST.accept(self)
        if not isinstance(x.e2AST, EmptyExpr):
            x.e2AST.accept(self)
            if not x.e2AST.type.Tequal(StdEnvironment.boolType):
                self.reporter.reportError(self.errMsg[21], "", x.e2AST.pos)
        if not isinstance(x.e3AST, EmptyExpr):
            x.e3AST.accept(self)
        x.stmtAST.accept(self)
    
    @visit.register
    def _(self, x: ReturnStmt):
        # STEP 2:
        # The following code checks assignment-compatibility of the return
        # statement's expression with the return type of the function.
        # Uncomment this code
        # as soon as you have finished type-checking of expressions.
        ''' START:
        if isinstance(x.eAST, EmptyExpr):
            # "return;" requires void function return type:
            if not self.currentFunctionReturnType.Tequal(StdEnvironment.voidType):
                self.reporter.reportError(self.errMsg[8], "", x.eAST.pos)
            return  # done -> early exit
        
        #
        # Falling through here means x.eAST != EmptyExpr
        #
        x.eAST.accept(self)
        if x.eAST.type.AssignableTo(self.currentFunctionReturnType):
            # Check for type coercion: if the function returns float, but
            # the expression of the return statement is of type int, we
            # need to convert this expression to float.
            if self.currentFunctionReturnType.Tequal(StdEnvironment.floatType) and \
                self.eAST.type.Tequal(StdEnvironment.intType):
                #coercion of operand to int:
                x.eAST = self.i2f(x.eAST)
        else:
            self.reporter.reportError(self.errMsg[8], "", x.eAST.pos)
        END '''
    
    @visit.register
    def _(self, x: CompoundStmt):
        '''
        If this CompoundStmt is the CompoundStmt of a Function, then
        we already opened the scope before visiting the formal parameters.
        No need to open a scope in that case. Otherwise set IsFunctionBlock
        to false, to remember for nested {...}.
        '''
        if self.IsFunctionBlock:
            self.IsFunctionBlock = False    # nested {...} need to open their own scope.
        else:
            # STEP 1:
            # Open a new scope for the compound statement (nested block within
            # a function body.

            # Start of your code:
            pass
            # End of your code
        
        # STEP 1:
        # Invoke the semantic analysis visitor for the declarations and the
        # statements of this CompoundStmt. Hint: look up the file AstGen/CompoundStmt.java
        # to learn about the AST children of this node.

        # Start of your code:

        # End of your code

        # STEP 1:
        # Visiting of this {...} compound statement is done. Close the scope
        # for this compound statement (even if it represents a function body).

        # Start of your code:

        # End of your code

    @visit.register
    def _(self, x: EmptyStmt):
        pass

    @visit.register
    def _(self, x: EmptyCompoundStmt):
        # STEP 1:
        # Close this scope if this EmptyCompoundStmt is the body of
        # a function.

        # Start of your code:
        pass
        # End of your code
    
    @visit.register
    def _(self, x: CallStmt):
        x.eAST.accept(self)
    
    @visit.register
    def _(self, x: VarDecl):
        if isinstance(x.tAST, ArrayType):
            (x.tAST).astExpr.accept(self)
        if not isinstance(x.eAST, EmptyExpr):
            x.eAST.accept(self)
            if isinstance(x.tAST, ArrayType):
                #STEP 4:
                #
                # Array declarations.
                # Check for error messages 15, 16, 13.
                # Perform i2f coercion if necessary.

                # Start of your code:
                pass
                # End of your code
            else:
                #STEP 4:
                #
                # Non-array declarations, i.e., scalar variables.
                # Check for error messages 14, 6.
                # Perform i2f coercion if necessary.

                # Start of your code:
                pass
                # End of your code

        #STEP 1:
        # Here we are visiting a variable declaration x.
        # Enter this variable into the scope stack. Like with formal parameters,
        # if an identifier of the same name is already present, then you should
        # report Error 2.

        # Start of your code:
        pass
        # End of your code

        # STEP 3:
        # Check that the variable is not of type void or void[]. 
        # Report error messages 3 and 4 respectively:

        # Start of your code:
        pass
        # End of your code
    
    @visit.register
    def _(self, x: DeclSequence):
        x.D1.accept(self)
        x.D2.accept(self)
    
    @visit.register
    def _(self, x: VarExpr):
        x.Ident.accept(self)
        #STEP 2:
        # Here we are visiting a variable expression.
        # Its type is synthesized from the type of the applied occurrence
        # of its identifier. Use "instanceof" to find out whether x.Ident.declAST
        # is a function declaration (FunDecl). In that case you should report
        # Error 11 and set x.type to the error type from StdEnvironment.
        x.type = self.typeOfDecl(x.Ident.declAST)
        # Start of your code:
        pass
        # End of your code
    
    @visit.register
    def _(self, x: AssignExpr):
        x.lAST.accept(self)
        x.rAST.accept(self)
        if x.rAST.type.AssignableTo(x.lAST.type):
            #check for type coercion:
            if x.lAST.type.Tequal(StdEnvironment.floatType) and \
                x.rAST.type.Tequal(StdEnvironment.intType):
                #coercion of right operand to int:
                x.rAST = self.i2f(x.rAST)
        else:
            self.reporter.reportError(self.errMsg[6], "", x.rAST.pos)
        if not(isinstance(x.lAST, VarExpr)) and not(isinstance(x.lAST, ArrayExpr)):
            self.reporter.reportError(self.errMsg[7], "", x.lAST.pos)
    
    @visit.register
    def _(self, x: IntExpr):
        #STEP 2:
        # Here we are visiting an integer literal. Set x.type of this
        # AST node to the int type from the standard environment
        # (StdEnvironment.intType).

        # Start of your code:
        pass
        # End of your code
    
    @visit.register
    def _(self, x: FloatExpr):
        #STEP 2:
        # Here we are visiting an float literal. Set x.type of this
        # AST node to the float type from the standard environment
        # (StdEnvironment.floatType).

        # Start of your code:
        pass
        # End of your code

    @visit.register
    def _(self, x: BoolExpr):
        #STEP 2:
        # Here we are visiting a bool literal. Set x.type of this
        # AST node to the bool type from the standard environment
        # (StdEnvironment.boolType).

        # Start of your code:
        pass
        # End of your code

    @visit.register
    def _(self, x: StringExpr):
        #STEP 2:
        # Here we are visiting a string literal. Set x.type of this
        # AST node to the string type from the standard environment
        # (StdEnvironment.stringType).

        # Start of your code:
        pass
        # End of your code
    
    @visit.register
    def _(self, x: ArrayExpr):
        x.idAST.accept(self)
        x.indexAST.accept(self)
        if not x.indexAST.type.Tequal(StdEnvironment.intType):
            self.reporter.reportError(self.errMsg[17], "", x.indexAST.pos)
        VE = x.idAST
        if not isinstance(self.typeOfDecl(VE.Ident.declAST), ArrayType):
            self.reporter.reportError(self.errMsg[12], "", x.pos)
            x.type = StdEnvironment.errorType
        else:
            x.type = self.typeOfArrayType(x.idAST.type)
    
    @visit.register
    def _(self, x: BinaryExpr):
        x.lAST.accept(self)
        x.oAST.accept(self)
        x.rAST.accept(self)
        if (self.HasIntOrFloatArgs(x.oAST)):
            if (x.lAST.type.Tequal(StdEnvironment.intType) and \
                x.rAST.type.Tequal(StdEnvironment.intType)):
                x.oAST.type = StdEnvironment.intType
                if self.HasBoolReturnType(x.oAST):
                    x.type = StdEnvironment.boolType
                else:
                    x.type = StdEnvironment.intType
                return
            elif (x.lAST.type.Tequal(StdEnvironment.floatType) and \
                  x.rAST.type.Tequal(StdEnvironment.floatType)):
                x.oAST.type = StdEnvironment.floatType
                if self.HasBoolReturnType(x.oAST):
                    x.type = StdEnvironment.boolType
                else:
                    x.type = StdEnvironment.floatType
                return
            elif (x.lAST.type.Tequal(StdEnvironment.intType) and \
                  x.rAST.type.Tequal(StdEnvironment.floatType)):
                #coercion of left operand to float:
                x.lAST = self.i2f(x.lAST)
                x.oAST.type = StdEnvironment.floatType
                if self.HasBoolReturnType(x.oAST):
                    x.type = StdEnvironment.boolType
                else:
                    x.type = StdEnvironment.floatType
                return
            elif (x.lAST.type.Tequal(StdEnvironment.floatType) and \
                  x.rAST.type.Tequal(StdEnvironment.intType)):
                # STEP 2:
                # This code is part of the type checking for binary
                # expressions. In this case,
                # the left-hand operand is float, the right-hand operand is int.
                # We have to type-cast the right operand to float.
                # This is the dual case to "int x float" above.

                # Start of your code:
                pass
                # End of your code
                return
        
        if self.HasBoolArgs(x.oAST):
            if (x.lAST.type.Tequal(StdEnvironment.boolType) and \
                x.rAST.type.Tequal(StdEnvironment.boolType)):
                x.oAST.type = StdEnvironment.intType 
                x.type = StdEnvironment.boolType
                return
        
        x.oAST.type = StdEnvironment.errorType
        x.type = StdEnvironment.errorType
        if not(isinstance(x.lAST.type, ErrorType) or isinstance(x.rAST.type, ErrorType)):
            # Error not spurious, because AST children are ok.
            self.reporter.reportError(self.errMsg[9], "", x.pos)
    
    @visit.register
    def _(self, x: UnaryExpr):
        x.oAST.accept(self)
        x.eAST.accept(self)
        #STEP 2:
        # Here we synthesize the type attribute for a unary operator.
        # x.eAST.type contains the type of the subexpression of this
        # unary operator.
        #
        # If x.eAST is of type int or float, and if oAST is an operator
        # that supports these types, then x.oAST.type and x.type
        # have to be set to x.eAST.type.
        #
        # If x.eAST is of type bool, and if x.oAST is an operator that
        # supports bool, then x.type is bool, but  x.oAST.type is of type
        # int (because of the JVM convention to represent true and false
        # as ints.
        #
        # In all other cases, x.oAST.type and x.type have to be set to
        # errorType, and Error 10 must be reported.
        #
        # You can have a look at visit(BinaryExpr) for a similar, yet
        # slightly more complicated case.

        # Start of your code:
        pass
        # End of your code 

    @visit.register
    def _(self, x: EmptyExpr):
        pass

    @visit.register
    def _(self, x: ActualParam):
        x.pAST.accept(self)
        x.type = x.pAST.type
    
    @visit.register
    def _(self, x: EmptyActualParam):
        pass

    @visit.register
    def _(self, x: ActualParamSequence):
        x.lAST.accept(self)
        x.rAST.accept(self)
    
    @visit.register
    def _(self, x: CallExpr):
        # Here we perform semantic analysis of function calls:
        x.type = StdEnvironment.errorType
        x.idAST.accept(self)
        x.paramAST.accept(self)
        # Retrieve the declaration of x from the scope stack:
        D = self.scopeStack.retrieve(x.idAST.Lexeme)
        # STEP 3:
        # Use "instanceof" to find out if D is a FunDecl. If not, report
        # Error 19 and *return*.
        # This check detects cases like
        #  int f; f(22);
        # where f is not a function. 

        # Start of your code:

        # End of your code

        # FunDecl: F = FunDecl: D
        F = D

        # STEP 2:
        # Check that the number of formal args from F and the number of actual
        # parameters of the function call x match.
        # Use the functions GetNrOfFormalParams and
        # GetNrOfActualParams from the beginning of this file to retrieve
        # the number of formal and actual parameters.

        # Start of your code:

        # End of your code

        # STEP 2:
        # Here we check that the types of the formal and actual parameters
        # match (Error 25). This is similar to type-checking the left-hand
        # and right-hand sides of assignment statements. Two steps need
        # to be carried out:
        #
        # (1)
        # Check that types of formal and actual args match: this means that
        # the actual parameter must be assignable to the formal parameter.
        # You can imagine passing an actual parameter to a formal parameter
        # like an assignment statement: formal_par = actual_par.
        #
        # (2)
        # Perform type coercion (int->float) of the *actual* parameter if necessary.
        #

        ''' You can use the following code as part of your solution. Uncomment
            the following code as soon as you have type-checking
            of expressions working. Uncomment the matching closing parenthesis
            of the "for" loop also.

            Start of your code:

        NrFormalParams = self.GetNrOfFormalParams(F)
        for i in range(1, NrFormalParams+1):
            Form = self.GetFormalParam(F, i)
            Act = self.GetActualParam(x, i)
            FormalT = Form.astType
            ActualT = Act.pAST.type
        
        # End of your code
        '''

        # If we fall through here, no semantic error occurred -> set the 
        # return type of the call expression to the return type of
        # its function:              
        x.type = self.typeOfDecl(F)
    
    @visit.register
    def _(self, x: ExprSequence):
        x.lAST.accept(self)
        x.rAST.accept(self)
    
    @visit.register
    def _(self, x: ID):
        # STEP 1:
        # Here we look up the declaration of an identifier
        # from the scope stack. If no declaration can be found on the
        # scope stack, you should report Error 5.
        binding = self.scopeStack.retrieve(x.Lexeme)
        if binding != None:
            x.declAST = binding
        # Start of your code: 

        # End of your code
    
    @visit.register
    def _(self, x: Operator):
        pass

    @visit.register
    def _(self, x: IntLiteral):
        pass

    @visit.register
    def _(self, x: FloatLiteral):
        pass

    @visit.register
    def _(self, x: BoolLiteral):
        pass

    @visit.register
    def _(self, x: StringLiteral):
        pass

    @visit.register
    def _(self, x: IntType):
        pass

    @visit.register
    def _(self, x: FloatType):
        pass

    @visit.register
    def _(self, x: BoolType):
        pass

    @visit.register
    def _(self, x: StringType):
        pass

    @visit.register
    def _(self, x: VoidType):
        pass

    @visit.register
    def _(self, x: ArrayType):
        pass

    @visit.register
    def _(self, x: ErrorType):
        pass


