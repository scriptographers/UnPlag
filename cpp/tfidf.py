import os
import glob
import argparse
import numpy as np
import seaborn as sns
from tqdm import tqdm
from ctokenizer import *
from matplotlib import pyplot as plt
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import TfidfVectorizer

# Arguments parsing
parser = argparse.ArgumentParser()
parser.add_argument("--data", "-d", type=str, required=True)
parser.add_argument("--regex", "-r", type=str, required=True)
parser.add_argument("--output", "-out", type=str, required=True)
parser.add_argument("--time", required=False, default=False, action="store_true")
args = parser.parse_args()

BASE_PATH = args.data
FILE_RE   = args.regex
OUT_PATH  = args.output
showTime  = args.time

files = []
problematic_files = []
for filepath in tqdm(glob.glob(os.path.join(BASE_PATH, FILE_RE))):
    tokens = tokenize(filepath)
    if len(tokens) > 0:
        files.append(tokens)
    else:
        # Files which result in empty tokens
        problematic_files.append(filepath)

# Show problematic files
if len(problematic_files) > 0:
    print("The following files have some problem: ")
    for pf in problematic_files:
        print(pf)

N_DOCS = len(files)

# A good reference: http://www.davidsbatista.net/blog/2018/02/28/TfidfVectorizer/

def identityFunction(file):
    return file

VOCAB_LIMIT = 1000 # Can be increased if efficency is not an issue
vectorizer = TfidfVectorizer(
    analyzer='word',
    tokenizer = identityFunction,
    preprocessor = identityFunction,
    # Consider unigrams, bigrams and trigrams
    ngram_range = (1, 3),
    max_features = VOCAB_LIMIT,
    encoding = "utf-8", 
    decode_error="ignore",
    stop_words = None,
    lowercase=False,
    norm = "l2" # Each row will be normalized
)
S = vectorizer.fit_transform(files)

# print(vectorizer.vocabulary_)
print(len(vectorizer.vocabulary_))

tfm = linear_kernel(S, S)
#tfm = tfm.toarray()

# TF-IDF Heatmap
thm = sns.heatmap(tfm)
fig = thm.get_figure()    
fig.savefig("plots/tfidf_heatmap_large.png", dpi=150)

np.savetxt("results/tfidf_" + OUT_PATH, tfm, fmt="%.4f", delimiter=',')