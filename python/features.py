# https://pypi.org/project/radon/
import numpy as np
from radon.raw import analyze
from radon.metrics import mi_parameters, mi_compute, h_visit, h_visit_ast

idxToDesc = [
    # Raw metrics:
    "loc", "lloc", "sloc", "comments", "multi", "single", "blank",

    # Halstead metrics:
    "h1: the number of distinct operators",
    "h2: the number of distinct operands",
    "N1: the total number of operators",
    "N2: the total number of operands",
    "h: the vocabulary, i.e. h1 + h2",
    "N: the length, i.e. N1 + N2",
    "calculated_length: h1 * log2(h1) + h2 * log2(h2)",
    "volume: V = N * log2(h)",
    "difficulty: D = h1 / 2 * N2 / h2",
    "effort: E = D * V",
    "time: T = E / 18 seconds",
    "bugs: B = V / 3000 - an estimate of the errors in the implementation",

    # McCabe's complexity
    "Cyclometric complexity",
    
    # Maintainibility index:
    "maintainibility index",
]

def extractFeatures(path):

    with open(path, "r") as f:
        contents = f.read()

    raw_metrics = analyze(contents)
    features = [r for r in raw_metrics]

    halsteadMetrics = h_visit(contents)[0]
    for hm in halsteadMetrics:
        features.append(hm)

    miMetrics = mi_parameters(contents)
    features.append(miMetrics[1]) # Cyclometric complexity
    features.append(mi_compute(*miMetrics))

    features = np.array(features, dtype=float)
    return features