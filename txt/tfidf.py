import os
import glob
import argparse
import numpy as np
import seaborn as sns
from tqdm import tqdm
from string import punctuation
from unidecode import unidecode
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer 
from matplotlib import pyplot as plt
from nltk.tokenize import word_tokenize
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import TfidfVectorizer

# Arguments parsing
parser = argparse.ArgumentParser()
parser.add_argument("--data", "-d", type=str, required=True)
parser.add_argument("--regex", "-r", type=str, required=True)
parser.add_argument("--output", "-out", type=str, required=True)
args = parser.parse_args()

BASE_PATH = args.data
FILE_RE   = args.regex
OUT_PATH  = args.output

SW = stopwords.words("english") # Common english stop-words
ps = PorterStemmer()

# Preprocessing and tokenizing:
def preprocessAndTokenize(F):
    F = F.lower() 
    F.translate(str.maketrans('', '', punctuation))
    F = unidecode(F) # Equivalent to strip_ascii of TfIdfVectorizer
    F = word_tokenize(F)
    F = [ps.stem(f) for f in F if f.isalnum() and f not in SW]
    return F

tokenized_files = []
for filepath in tqdm(glob.glob(os.path.join(BASE_PATH, FILE_RE))):
    with open(filepath, 'r', encoding="utf-8", errors="ignore") as f:
        contents = f.read()
        tokens = preprocessAndTokenize(contents)
        tokenized_files.append(tokens)

N_DOCS = len(tokenized_files)

def identityFunction(file):
    return file

VOCAB_LIMIT = 10000 # Can be increased if efficency is not an issue
vectorizer = TfidfVectorizer(
    # Already preprocessed and tokenized
    analyzer = "word",
    tokenizer = identityFunction,
    preprocessor = identityFunction,
    # Consider unigrams and bigrams
    ngram_range = (1, 2),
    max_features = VOCAB_LIMIT,
    encoding = "utf-8", 
    decode_error="ignore",
    stop_words = None,
    lowercase = False,
    norm = "l2" # Each row will be unit normalized
)

S = vectorizer.fit_transform(tokenized_files) # Vocabulary built is inside vectorizer.vocabulary_
# linear_kernel computes the dot product of the sparse matrix:
tfm = linear_kernel(S, S)

# print(vectorizer.vocabulary_)
# print(len(vectorizer.vocabulary_))

# TF-IDF Heatmap
thm = sns.heatmap(tfm)
fig = thm.get_figure()    
fig.savefig("plots/tfidf_heatmap.png", dpi=150)

np.savetxt("results/tfidf_" + OUT_PATH, tfm, fmt="%.4f", delimiter=',')
