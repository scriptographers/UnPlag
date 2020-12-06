import sys
import clang.cindex as ci
from clang.cindex import CursorKind as ck

"""
Almost all functions used are present inside cindex.py itself
Code/docs for clang.cindex: 
https://github.com/llvm-mirror/clang/blob/master/bindings/python/clang/cindex.py
"""

# Set the config (works on linux devices only)
ci.Config.set_library_path("/usr/lib/x86_64-linux-gnu")

class CTokenizer:

    # Create the index and parse the entire file:
    def __init__(self, filePath):
        self.index = ci.Index.create()
        self.parsed_data = self.index.parse(filePath) # A ci.TranslationUnit object
        self.path = filePath
        self.allowed_kinds = [
            ck.FUNCTION_DECL, 
            ck.CLASS_DECL, 
            ck.STRUCT_DECL, 
            ck.VAR_DECL,
            ck.ENUM_DECL,
            ck.CXX_METHOD,
            ck.FUNCTION_TEMPLATE,
            ck.CLASS_TEMPLATE,
        ]
        # This needs to be updated, all special identifiers from STL need to be added
        self.special_identifiers = [
            "std", "cout", "cin", "endl", "vector", "pair", "string", "NULL", "size_t"
        ]

    # Print all kinds included in clang
    def showAllKinds(self):
        # Prints all the available kinds parsed by clang:
        for kind in ck._kinds:
            if kind:
                print(kind)
    
    # Igores a set of delimiters
    def processPunctuation(self, pnc):
        if pnc in ["{", "}", "(", ")", "[", "]", ";", ",", ".", ":"]:
            return None
        else:
            return pnc
    
    # Processes literals
    def processLiteral(self, ltr):
        kind = ltr.cursor.kind
        if kind == ck.INTEGER_LITERAL:
            return "int"
        elif kind == ck.FLOATING_LITERAL:
            return "flt"
        elif kind == ck.IMAGINARY_LITERAL:
            return "imag"
        elif kind == ck.STRING_LITERAL:
            return "str"
        elif kind == ck.CHARACTER_LITERAL:
            return "char"
        elif kind == ck.CXX_BOOL_LITERAL_EXPR:
            return "bool"
        elif kind == ck.COMPOUND_STMT:
            return "cmpd"
        elif kind == ck.IF_STMT:
            return "if"
        elif kind == ck.FOR_STMT:
            return "for"
        elif kind == ck.DECL_STMT:
            return "dec"
        elif kind == ck.CXX_METHOD or kind == ck.FUNCTION_DECL:
            return "fun"
        else:
            print("Error in file: ", self.path)
            print("Token: ", ltr.spelling, kind)
            raise NameError("Unknown literal encountered")

    # To optimize
    def processIdentifier(self, idt):
        # Special "identifiers" (Not exhaustive)
        if idt.spelling in self.special_identifiers:
            return idt.spelling
        kind = idt.cursor.kind
        # Declaration:
        if kind.is_declaration():
            return "dec"
        # References:
        elif kind.is_reference():
            return "ref"
        # Expressions (Not really needed):
        # elif kind.is_expression():
        #     return "exp"
        # Statements:
        elif kind.is_statement():
            return "stm"
        # Attributes:
        elif kind.is_attribute():
            return "atr"
        # Invalid:
        elif kind.is_invalid():
            return "inv"
        # Variable use after declaration:
        elif kind == ck.DECL_REF_EXPR:
            return "use"
        else:
            # print(idt.spelling)
            return "var"

    # Tokenizes the given cursor completely:
    def completeTokenization(self, cursor):
        tokens = cursor.get_tokens()
        processedTokens = []
        for token in tokens:
            tkn = token.kind.name
            kind = token.kind
            # Comments
            if tkn == "COMMENT":
                pass
            # Constructor:
            elif kind == ck.CONSTRUCTOR:
                processedTokens.append("con")
            # Destructor:
            elif kind == ck.DESTRUCTOR:
                processedTokens.append("des")
            # Ternary operator:
            elif kind in [ck.CONDITIONAL_OPERATOR, ck.CXX_FUNCTIONAL_CAST_EXPR]:
                processedTokens.append("ter")
            # Explicit type casting:
            elif kind == ck.CSTYLE_CAST_EXPR:
                processedTokens.append("cst")
            # Punctuations:
            elif tkn == "PUNCTUATION":
                p = self.processPunctuation(token.spelling)
                if p:
                    processedTokens.append(p)
            # Literals:
            elif tkn == "LITERAL":
                processedTokens.append(self.processLiteral(token))
            # Identifiers:
            elif tkn == "IDENTIFIER":
                processedTokens.append(self.processIdentifier(token))
            # Add keyword directly
            elif tkn == "KEYWORD":
                processedTokens.append(token.spelling)
            else:
                raise NameError("Unknown token type encountered")
        return processedTokens
    
    # Treats the entire document on a global level (Not really useful), contains namespaces and headers
    def documentTokenization(self):
        mainCursor = self.parsed_data.cursor
        return self.completeTokenization(mainCursor)
    
    # (Level-1 (Global) Tokenization) Kind-wise tokenization of the document based on allowed_kinds
    def splitByKinds(self):
        kindwiseTokens = []
        # Iterate over children of L1 Tokens:
        mainCursor = self.parsed_data.cursor
        for c in mainCursor.get_children():
            currentPath = c.location.file.name
            if c.kind in self.allowed_kinds and currentPath == self.path:
                kindName = c.spelling
                # (Level-2 Tokenization) Tokenize each child of the L1 Tokens
                tokens = self.completeTokenization(c)
                kindwiseTokens.append((kindName, tokens))
        return kindwiseTokens

    # Combines kindwise tokens
    def rawTokenization(self):
        rawTokens = []
        # Iterate over children of L1 Tokens:
        mainCursor = self.parsed_data.cursor
        for c in mainCursor.get_children():
            currentPath = c.location.file.name
            if c.kind in self.allowed_kinds and currentPath == self.path:
                # (Level-2 Tokenization) Tokenize each child of the L1 Tokens
                tokens = self.completeTokenization(c)
                rawTokens += tokens # List addition
        return rawTokens

# Tester: 
if __name__ == "__main__":
    FILE_PATH = sys.argv[1] 
    ctok = CTokenizer(FILE_PATH)
    kindwiseTokens = ctok.splitByKinds()
    # rawTokens = ctok.rawTokenization()
    # print(rawTokens)
    for t in kindwiseTokens:
        print("{}:\nTokens: {}\n".format(t[0], t[1]))