import ast
from pyData import *

# Excellent documentation for python ast: https://greentreesnakes.readthedocs.io/

# Given an operator, convert to it's string representation
def typeToStr(t):
    return type(t).__name__.lower()

# Used for traversing the tree in pre-order, use ast.walk() for BFS/level-order
class PreOrder(ast.NodeVisitor):

    def __init__(self):
        self.preorder = []

    def visit(self, node):
        self.preorder.append(node)
        super(PreOrder, self).generic_visit(node)

# Tokenizes the python3 file present at "path"
def tokenize(path):
    with open(path, 'r', encoding="utf-8", errors="ignore") as f:
        src = f.read()

    # Create the AST
    tree = ast.parse(src, mode="exec") # tree contains the root node of the tree

    visitor = PreOrder()
    visitor.visit(tree)
    dfs = visitor.preorder

    # Traverses the tree in pre-order:
    tokens = []
    for node in dfs:

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
                elif type(i) == ast.Subscript:
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
            tokens.append(typeToStr(node.op))
        
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
                elif type(i) == ast.Subscript:
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

        ## Operators
        elif kind in [ast.UnaryOp, ast.BinOp, ast.BoolOp]:
            token = typeToStr(node.op)

        elif kind == ast.Compare:
            for op in node.ops:
                tokens.append(typeToStr(op))

        ## Function calls:
        elif kind == ast.Call:
            token = "func_call"
            tokens.append("n_args_" + str(len(node.args)))

        ## If-expressions, a = b if c is treated same as vanilla if-else
        elif kind == ast.IfExp:
            token = "if_else" # All inside content is treated as separate nodes

        elif kind == ast.Attribute:
            if type(node.ctx) == ast.Load:
                token = "attr_used"

        elif kind == ast.Subscript:
            token = "subscript_" + typeToStr(node.slice)

        # Expressions: end #


        # Control flow: start #

        elif kind == ast.If:
            token = "if_else"

        elif kind == ast.For: # Doesn't include the for present inside list comprehensions
            token = "for"

        elif kind == ast.comprehension: # The for present inside list comprehensions
            token = "for"

        # Control flow: end #


        # Functions and Class definitions: start #

        elif kind == ast.FunctionDef:
            arguments = node.args
            args = arguments.args
            decs = node.decorator_list
            token = "func_def_nd_" + str(len(decs))
            for _ in range(len(args)):
                tokens.append("arg")

        elif kind == ast.Lambda:
            arguments = node.args
            args = arguments.args
            token = "lambda"
            for _ in range(len(args)):
                tokens.append("arg")

        elif kind == ast.ClassDef:
            bases = node.bases
            decs = node.decorator_list
            token = "class_def_na_" + str(len(bases)) + "_nd_" + str(len(decs))


        # Functions and Class definitions: end #


        # Async and await: start #

        elif kind == ast.AsyncFunctionDef:
            arguments = node.args
            args = arguments.args
            decs = node.decorator_list
            token = "async_func_def_nd_" + str(len(decs))
            for _ in range(len(args)):
                tokens.append("arg")

        # Async and await: end #


        # Add the type directly:
        elif kind in addDirectly:
            token = typeToStr(node)

        # Finally, add the single token:
        if token:
            tokens.append(token)

    return tokens
