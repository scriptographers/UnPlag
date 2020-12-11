import ast
from pyData import *

path = "example.py"
with open(path, 'r', encoding="utf-8", errors="ignore") as f:
    src = f.read()

# Create the AST
tree = ast.parse(src, mode="exec")

# Given an operator, convert to it's string representation
def opToStr(op):
    return type(op).__name__

# Traverses the tree in BFS order:
tokens = []
bfs = ast.walk(tree)
for node in bfs:

    # To be added at last:
    token = None
    # Denotes the type of the ast node:
    kind = type(node)

    # Statements: start

    ## Assignments:
    if kind == ast.Assign:
        for i in node.targets:
            if type(i) == ast.Name:
                tokens.append("var_assign")
            elif type(i) == ast.Tuple:
                tokens.append("unpack_assign")
            elif type(i) == ast.Attribute:
                tokens.append("attr_assign")
            elif type(node.target) == ast.Subscript:
                tokens.append("subscr_assign")
            else:
                tokens.append("assign")

    elif kind == ast.AnnAssign:
        # Annotated assign and simple assign are treated the same
        if type(node.target) == ast.Subscript:
            token = "subscr_assign"
        elif type(node.target) == ast.Attribute:
            token = "attr_assign"
        elif type(node.target) == ast.Name:
            token = "var_assign"
        else:
            token = "assign"

    elif kind == ast.AugAssign:
        # Assignments of the form (a += 1)
        if type(node.target) == ast.Subscript:
            token = "subscr_assign"
        elif type(node.target) == ast.Attribute:
            token = "attr_assign"
        elif type(node.target) == ast.Name:
            token = "var_assign"
        else:
            token = "assign"
        tokens.append(opToStr(node.op))
    
    ## Print: Python 2 only
    # elif kind == ast.Print:
    #     token = "print"
        
    ## Delete:
    elif kind == ast.Delete:
        for i in node.targets:
            if type(i) == ast.Name:
                tokens.append("var_delete")
            elif type(i) == ast.Attribute:
                tokens.append("attr_delete")
            elif type(node.target) == ast.Subscript:
                tokens.append("subscr_delete")
            else:
                tokens.append("delete")
    
    ## All imports are ignored

    # Statements: end #


    # Literals: start #

    elif kind == ast.Constant:
        # TODO: Treat all numeric literals the same, although in python this won't matter much
        token = type(node.value).__name__ + "_literal" 

    elif kind == ast.JoinedStr:
        token = "str_literal"
    
    # Literals: end #


    # Variables: start #

    elif kind == ast.Name:
        if type(node.ctx) == ast.Load:
            token = "var_used"

    elif kind == ast.Starred:
        token = "var_ref"
    
    # Variables: end #


    # Expressions: start #
    # Expressions: end #


    # Control flow: start #
    # Control flow: end #


    # Functions and Class definitions: start #
    # Functions and Class definitions: end #


    # Async and await: start #
    # Async and await: end #


    # Add the type directly:
    elif kind in addDirectly:
        token = kind.__name__.lower()

    # Add the single token finally:
    if token:
        tokens.append(token)


print(tokens)
