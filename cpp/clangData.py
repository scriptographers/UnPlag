from clang.cindex import CursorKind
from clang.cindex import TypeKind as tk

unary_operators = ["-", "++", "--", "!", "&"]

binary_operators = [
    "=", "+=", "-=", "*=", "/=", "<<=", ">>=", "&=", "|="
    "+", "-", "*", "/", "%", 
    "==", "!=", "<", ">", ">=", "<=", 
    "&&", "||",
    "&", "|", "^", "~", "<<", ">>"
]

ignorePunctuations = ["#", "{", "}", "(", ")", "[", "]", ";", ",", ".", ":"]

misc = [
    CursorKind.STRUCT_DECL,
    CursorKind.UNION_DECL,
    CursorKind.CLASS_DECL,
    CursorKind.ENUM_DECL,
    CursorKind.DESTRUCTOR,
    CursorKind.CLASS_TEMPLATE,
    CursorKind.FUNCTION_TEMPLATE,
    CursorKind.MEMBER_REF,
    CursorKind.INTEGER_LITERAL,
    CursorKind.FLOATING_LITERAL,
    CursorKind.IMAGINARY_LITERAL,
    CursorKind.STRING_LITERAL,
    CursorKind.CHARACTER_LITERAL,
    CursorKind.ARRAY_SUBSCRIPT_EXPR,
    CursorKind.INIT_LIST_EXPR,

    CursorKind.CASE_STMT,
    # A default statement.
    CursorKind.DEFAULT_STMT,
    # An if statement.
    CursorKind.IF_STMT,
    # A switch statement.
    CursorKind.SWITCH_STMT,
    # A while statement.
    CursorKind.WHILE_STMT,
    # A do statement.
    CursorKind.DO_STMT,
    # A for statement.
    CursorKind.FOR_STMT,
    # A goto statement.
    CursorKind.GOTO_STMT,
    # An indirect goto statement.
    CursorKind.INDIRECT_GOTO_STMT,
    # A continue statement.
    CursorKind.CONTINUE_STMT,
    # A break statement.
    CursorKind.BREAK_STMT,
    # A return statement.
    CursorKind.RETURN_STMT,
    # A GNU-style inline assembler statement.
    CursorKind.ASM_STMT,
    
    # C++'s catch statement.
    CursorKind.CXX_CATCH_STMT,
    # C++'s try statement.
    CursorKind.CXX_TRY_STMT,

    CursorKind.NULL_STMT
]

# Function declarations:
funcDec = [
    CursorKind.FUNCTION_DECL,
    CursorKind.CXX_METHOD
] 

varDec = [
    CursorKind.VAR_DECL
]

ignoreTypeKinds = [
    tk.INVALID, 
    tk.DEPENDENT, 
    tk.UNEXPOSED, 
    tk.FUNCTIONPROTO, 
    tk.TYPEDEF, 
    tk.LVALUEREFERENCE, 
    tk.RVALUEREFERENCE,
    tk.ELABORATED,
    tk.RECORD,
    tk.ELABORATED,
    tk.OVERLOAD
]