import sys
import clang.cindex as ci
from clang.cindex import CursorKind as ck
from clang.cindex import TypeKind as tk
from clangData import *

# Set the config (works on linux devices only)
ci.Config.set_library_path("/usr/lib/x86_64-linux-gnu")

def tokenize(path):

    index = ci.Index.create()
    root  = index.parse(path)
    cursor = root.cursor

    tokens = []
    # Traverse the AST
    preOrder = cursor.walk_preorder() # A generator of cursors
    for c in preOrder:
        if str(c.location.file) == path:

            ckind = c.kind
            tkind = c.type.kind

            if ckind in funcDec:
                if c.is_const_method():
                    tokens.append("const_func")
                elif c.is_static_method():
                    tokens.append("static_func")
                else:
                    tokens.append("func")
                # https://stackoverflow.com/questions/7035356/c-why-static-member-function-cant-be-created-with-const-qualifier

            elif ckind == ck.CONSTRUCTOR:
                if c.is_converting_constructor():
                    tmp = "conv_con"
                elif c.is_copy_constructor():
                    tmp = "copy_con"
                elif c.is_default_constructor():
                    tmp = "def_con"
                elif c.is_move_constructor():
                    tmp = "move_con"
                else:
                    tmp = "con"
                tokens.append(tmp)

            elif ckind in varDec:
                if tkind not in ignoreTypeKinds:
                    if tkind in numeric_types:
                        tokens.append("num_var")
                    else:
                        tokens.append(tkind.name + "_var")
                else:
                    tokens.append("var")

            elif ckind == ck.PARM_DECL:
                if tkind not in ignoreTypeKinds:
                    if tkind in numeric_types:
                        tokens.append("num_par")
                    else:
                        tokens.append(tkind.name + "_par")
                else:
                    tokens.append("par")

            elif ckind == ck.TEMPLATE_TYPE_PARAMETER:
                tokens.append("T_par")

            elif ckind == ck.CXX_ACCESS_SPEC_DECL:
                tokens.append(str(c.access_specifier).split('.')[1])

            elif ckind == ck.DECL_REF_EXPR:
                if tkind not in ignoreTypeKinds:
                    if tkind in numeric_types:
                        tokens.append("num_used")
                    else:
                        tokens.append(tkind.name + "_used")

            elif ckind == ck.CALL_EXPR:
                if tkind not in ignoreTypeKinds:
                    if tkind in numeric_types:
                        tokens.append("num_called")
                    else:
                        tokens.append(tkind.name + "_called")

            elif ckind == ck.UNARY_OPERATOR:
                subtokens = c.get_tokens()
                for st in subtokens:
                    if st.kind.name == "PUNCTUATION" and st.spelling in unary_operators:
                        tokens.append(st.spelling)
            elif ckind == ck.BINARY_OPERATOR:
                subtokens = c.get_tokens()
                for st in subtokens:
                    # print(st.spelling, end=' ')
                    if st.kind.name == "PUNCTUATION" and st.spelling in binary_operators:
                        if st.spelling == "<<":
                            tokens.append("lshift")
                        elif st.spelling == ">>":
                            tokens.append("rshift")
                        else:
                            tokens.append(st.spelling)
                # print("")
                # alreadyProcessedChildren = c.get_children()
                # for child in alreadyProcessedChildren:
                #     if child.kind == ck.BINARY_OPERATOR:
                #         preOrder.remove(child)
            elif ckind == ck.COMPOUND_ASSIGNMENT_OPERATOR:
                # Compund assignment operator is equivalent to binary operator
                subtokens = c.get_tokens()
                for st in subtokens:
                    if st.kind.name == "PUNCTUATION" and "=" in st.spelling:
                        tmp = st.spelling.split("=")[0]
                        if tmp == "<<":
                            tokens.append("lshift")
                        elif tmp == ">>":
                            tokens.append("rshift")
                        else:
                            tokens.append(tmp)
            elif ckind == ck.CONDITIONAL_OPERATOR:
                tokens.append("?:")

            elif ckind == ck.CSTYLE_CAST_EXPR or ckind == ck.CXX_FUNCTIONAL_CAST_EXPR:
                if tkind not in ignoreTypeKinds:
                    if tkind in numeric_types:
                        tokens.append("cast_num")
                    else:
                        tokens.append("cast_" + tkind.name)
                else:
                    tokens.append("cast")

            elif ckind == ck.CXX_BOOL_LITERAL_EXPR:
                tokens.append("BOOL_LITERAL")
            elif ckind == ck.CXX_NULL_PTR_LITERAL_EXPR:
                tokens.append(tkind.name)

            elif ckind == ck.CXX_THIS_EXPR:
                tokens.append("this")
            elif ckind == ck.CXX_THROW_EXPR:
                tokens.append("throw")
            elif ckind == ck.CXX_NEW_EXPR:
                tokens.append("new")
            elif ckind == ck.CXX_DELETE_EXPR:
                tokens.append("delete")

            elif ckind == ck.CXX_FOR_RANGE_STMT:
                tokens.append("FOR_STMT")
 
            elif ckind in misc:
                tokens.append(ckind.name)

    tokens = [token.lower() for token in tokens]

    return tokens