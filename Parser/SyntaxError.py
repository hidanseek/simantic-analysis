from Parser.Parser import *

class SyntaxError(Exception):
    def __init__(self, message=""):
        super().__init__(message)
