from Scanner.Token import *
from Scanner.SourceFile import *
from Scanner.SourcePos import *
from Scanner.Scanner import *
from Parser.Parser import *
from Parser.SyntaxError import *
from TreePrinter.Printer import Printer
from TreeDrawer.Drawer import Drawer
from Unparser.Unparser import Unparser
from StdEnvironment import *
from SemanticAnalysis.SemanticAnalysis import *

import sys

class MiniC:
    def __init__(self):
        self.scanner = None
        self.parser = None
        self.sem = None

        self.reporter = None
        self.drawer = None
        self.printer = None
        self.unparser = None

        self.stdenv = None

        # The abstract syntax tree representing the source program

        self.AST = None
        #commandline args:
        self.sourceName = ""

        self.DrawTree1 = None
        self.DrawTree2 = None
        self.DrawTreeF = ''
        self.DrawStdEnvTree = None
        self.PrintTree = None
        self.UnparseTree = None
        self.PrintTreeF = ''
        self.UnparseTreeF = ''

    def compileProgram(self, sourceName):
        print("********** " + "MiniC Compiler" + " **********")

        self.source = SourceFile(sourceName)

        self.scanner = Scanner(self.source)
        '''
            Enable this to observe the sequence of tokens
            delivered by the scanner:
        '''
        #scanner.enableDebugging()
        self.reporter   = ErrorReporter()
        self.stdenv     = StdEnvironment()
        self.parser     = Parser(self.scanner, self.reporter)
        self.sem        = SemanticAnalysis(self.reporter)
        self.drawer     = Drawer()
        self.printer    = Printer()
        self.unparser   = Unparser()

        if self.DrawStdEnvTree:
            envdrawer = Drawer()
            envdrawer.draw(self.stdenv.AST, 'envast')
            #envdrawer.draw(StdEnvironment.AST, 'envast')
        
        print("Syntax Analysis ...")
        self.AST = self.parser.parse()  # 1st pass

        if self.reporter.numErrors == 0:
            if self.PrintTree:
                self.printer.print(self.AST, self.PrintTreeF)
            if self.UnparseTree:
                self.unparser.unparse(self.AST, self.UnparseTreeF)
            if self.DrawTree1:
                self.drawer.draw(self.AST, self.DrawTreeF)
            print("Semantic Analysis ...")
            self.sem.check(self.AST)    # 2nd pass
            if self.DrawTree2:
                self.drawer.draw(self.AST, self.DrawTreeF)
        
        successful = (self.reporter.numErrors == 0)
        if successful:
            print("Compilation was successful.")
        else:
            print("Compilation was unsuccessful.")

    def usage(self):
        print('Usage: MiniC filename')
        print('Option: -ast1 <file> to draw the AST to <file> before semantic analysis')
        print('Option: -ast2 <file> to draw the AST to <file> after semantic analysis')
        print('Option: -envast <file> to draw the StdEnvironment AST')
        print('Option: -t <file> to dump the AST to <file>')
        print('Option: -u <file> to unparse the AST to <file>')
        exit(1)
    
    def processCmdLine(self, args):
        self.DrawTree1 = False
        self.DrawTree2 = False
        self.DrawStdEnvTree = False
        self.PrintTree = False
        self.PrintTreeF = ""
        self.UnparseTree = False
        self.UnparseTreeF = ""
        self.sourceName = ''
        
        arg_index = 1

        while arg_index < len(args):
            if args[arg_index] == '-ast1':
                self.DrawTree1 = True
                if len(args) < arg_index + 1:
                    self.usage()
                else:
                    arg_index+=1
                    self.DrawTreeF = args[arg_index]
                    arg_index += 1
            elif args[arg_index] == '-ast2':
                self.DrawTree2 = True
                if len(args) < arg_index + 1:
                    self.usage()
                else:
                    arg_index+=1
                    self.DrawTreeF = args[arg_index]
                    arg_index += 1
            elif args[arg_index] == '-envast':
                self.DrawStdEnvTree = True
                if len(args) < arg_index + 1:
                    self.usage()
                else:
                    arg_index += 1
                    self.DrawTreeF = args[arg_index]
                    arg_index += 1
            elif args[arg_index] == '-t':
                self.PrintTree = True
                if len(args) < arg_index + 1:
                    self.usage()
                else:
                    arg_index += 1
                    self.PrintTreeF = args[arg_index]
                    arg_index += 1
            elif args[arg_index] == '-u':
                self.UnparseTree = True
                if len(args) < arg_index + 1:
                    self.usage()
                else:
                    arg_index += 1
                    self.UnparseTreeF = args[arg_index]
                    arg_index += 1
            else:
                self.sourceName = args[arg_index]
                arg_index += 1
                if arg_index < len(args):
                    # After the input source file no arg is allowed:
                    self.usage()

        if self.sourceName == '':
            self.usage()
        
miniC = MiniC()

if __name__ == '__main__':
    miniC.processCmdLine(sys.argv)
    miniC.compileProgram(miniC.sourceName)