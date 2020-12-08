from asttokens import ASTTokens
path = "example.py"
with open(path) as f:
    contents = f.read()
res = ASTTokens(contents, parse=True)
print(res.tokens)