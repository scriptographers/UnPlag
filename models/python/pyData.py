import ast

addDirectly = [
    
    # Statements
    ast.Raise,
    ast.Assert,
    ast.Pass,

    # Literals
    ast.List,
    ast.Tuple,
    ast.Set,
    ast.Dict,

    # Comprehensions:
    ast.ListComp,
    ast.SetComp,
    ast.GeneratorExp,
    ast.DictComp,

    # Control-flow
    ast.While,
    ast.Break,
    ast.Continue,
    ast.Try,
    ast.With,

    # Functions and Class definitions:
    ast.Return,
    ast.Yield,
    ast.YieldFrom,
    ast.Global,
    ast.Nonlocal,

    # Async and await
    ast.Await,
    ast.AsyncFor,
    ast.AsyncWith

]