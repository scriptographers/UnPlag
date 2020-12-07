from clang.cindex import CursorKind
from clang.cindex import TypeKind

# This is a helper file, should be present in the same directory as ctokenize.py

# The following punctuations are ignored during tokenization:
ignorePunctuations = [ 
    ";", ",", ".", "{", "}", "(", ")", "[", "]", ":", "#"
]

# Operators:
unary_operators = [
    "-", "++", "--", "!", "&"
]
binary_operators = [
    # Arithmetic operators:
    "+", "-", "*", "/", "%",
    # Relational operators: 
    "==", "!=", "<", ">", ">=", "<=", 
    # Logical operators:
    "&&", "||",
    # Bit operators:
    "&", "|", "^", "~", "<<", ">>"
]
compound_operators = [
    "=", "+=", "-=", "*=", "/=", "<<=", ">>=", "&=", "|="
]

# We treat all numeric data types as the same
# We treat character types differently: https://docs.microsoft.com/en-us/cpp/cpp/char-wchar-t-char16-t-char32-t?view=msvc-160
# This ensures changing all INTs to LONG LONG INTs doesn't affect the similarity
# This also reduces the vocabulary size required
numeric_literals = [
    CursorKind.INTEGER_LITERAL,
    CursorKind.FLOATING_LITERAL,
]
numeric_types = [
    TypeKind.SHORT,
    TypeKind.INT,
    TypeKind.LONG,
    TypeKind.LONGLONG,
    TypeKind.INT128,
    TypeKind.FLOAT,
    TypeKind.DOUBLE,
    TypeKind.LONGDOUBLE,
    TypeKind.FLOAT128,
    TypeKind.USHORT,
    TypeKind.UINT,
    TypeKind.ULONG, 
    TypeKind.ULONGLONG, 
    TypeKind.UINT128,
]

# These types are directly included as tokens. 
# For example, CursorKind.STRUCT_DECL gets included as STRUCT_DECL token
misc = [

    CursorKind.STRUCT_DECL,
    CursorKind.UNION_DECL,
    CursorKind.CLASS_DECL,
    CursorKind.ENUM_DECL,

    CursorKind.DESTRUCTOR,

    CursorKind.CLASS_TEMPLATE,
    CursorKind.FUNCTION_TEMPLATE,

    CursorKind.MEMBER_REF,

    CursorKind.IMAGINARY_LITERAL,
    CursorKind.STRING_LITERAL,
    CursorKind.CHARACTER_LITERAL,

    CursorKind.ARRAY_SUBSCRIPT_EXPR,
    CursorKind.INIT_LIST_EXPR,

    CursorKind.IF_STMT,
    CursorKind.SWITCH_STMT,
    CursorKind.CASE_STMT,
    CursorKind.DEFAULT_STMT,

    CursorKind.DO_STMT,
    CursorKind.WHILE_STMT,
    CursorKind.FOR_STMT,

    CursorKind.GOTO_STMT,
    CursorKind.INDIRECT_GOTO_STMT,

    CursorKind.CONTINUE_STMT,
    CursorKind.BREAK_STMT,

    CursorKind.RETURN_STMT,
    CursorKind.ASM_STMT,
    
    CursorKind.CXX_TRY_STMT,
    CursorKind.CXX_CATCH_STMT,

    CursorKind.NULL_STMT
]

# Function declarations, both are treated the same:
funcDec = [
    CursorKind.FUNCTION_DECL,
    CursorKind.CXX_METHOD
] 

# These types are not tokenized at all
ignoreTypeKinds = [
    TypeKind.INVALID, 
    TypeKind.DEPENDENT, 
    TypeKind.UNEXPOSED, 
    TypeKind.FUNCTIONPROTO, 
    TypeKind.TYPEDEF, 
    TypeKind.LVALUEREFERENCE, 
    TypeKind.RVALUEREFERENCE,
    TypeKind.RECORD,
    TypeKind.ELABORATED,
    TypeKind.OVERLOAD
]