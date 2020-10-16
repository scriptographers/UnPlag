import os
import glob
import time
import argparse
import numpy as np
from string import punctuation
from collections import Counter
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer 
from nltk.tokenize import word_tokenize, sent_tokenize # word tokenizer and sentence tokenizer

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

# Global variables
SW = stopwords.words("english") # Common english stop-words
ps = PorterStemmer() # TODO: Try more stemming algorithms

# FUNCTIONS

# Preprocessing:
def preprocess(F):
    # 1. Convert to lowercase
    F = F.lower() 
    # 2. Remove all punctuations
    F.translate(str.maketrans('', '', punctuation))
    # 3. Tokenize the words
    F = word_tokenize(F)
    # 4. Stem each word and remove all stop_words (can also use isalpha() here)
    F = [ps.stem(f) for f in F if f.isalnum() and f not in SW] # TODO: Make this more efficient
    # We can also use PySpellChecker to correct common mispellings, but that may decrease the efficiency
    return F

# Creates the signature vector for a file
def sigvec(F, vocab):
    # TODO: A more efficient way needed
    D = {word:0 for word in vocab}
    # Count frequency
    for word in F:
        D[word] += 1 
    # The actual words don't matter from now on, convert to frequency vector
    V = np.fromiter(D.values(), dtype=float)
    return V

# Computes the cosine similarity between 2 preprocessed_files
def cosineSimilarity(F1, F2, vocab):
    V1 = sigvec(F1, vocab)
    V2 = sigvec(F2, vocab)
    # For n files, we need to implement featurewise normalization
    return (np.dot(V1, V2)/(np.linalg.norm(V1)*np.linalg.norm(V2)))

# Computes the Jaccard similarity between 2 preprocessed_files
def jaccardSimilarity(F1, F2):
    n1, n2 = len(F1), len(F2)
    D1, D2 = Counter(F1), Counter(F2)
    D = D1 & D2 # Intersection
    ni = sum(D.values())
    nu = n1 + n2 - ni # Union
    niou = ni/nu # Jaccard Similarity: Intersection over Union
    return niou


# MAIN:
tic = time.time()

preprocessed_files = []

# TODO: A more efficient way to extend to n files

for filepath in glob.glob(os.path.join(BASE_PATH, FILE_RE)):
    with open(filepath, 'r', encoding="utf-8", errors="ignore") as f:
        F = f.read()
        preprocessed_files.append(preprocess(F))

N_DOCS = len(preprocessed_files)

cosine_matrix  = np.zeros((N_DOCS, N_DOCS), dtype=float)
jaccard_matrix = np.zeros((N_DOCS, N_DOCS), dtype=float)

for i in range(N_DOCS):
    for j in range(i+1, N_DOCS):
        F1 = preprocessed_files[i]
        F2 = preprocessed_files[j]
        # Create the vocabulary
        vocab = F1 + F2;
        # Remove all duplicates
        vocab = list(set(vocab))
        # Sort lexicographically, doesnt actually matter, done for reproducible order inside the vocab
        # vocab.sort()
        cosine_matrix[i, j]  = cosineSimilarity(F1, F2, vocab)
        jaccard_matrix[i, j] = jaccardSimilarity(F1, F2)

# Utilize the symmetric nature of the matrix
for i in range(N_DOCS):
    for j in range(i):
        cosine_matrix[i][j]  = cosine_matrix[j][i]
        jaccard_matrix[i][j] = jaccard_matrix[j][i]

# Not needed, added for consistency
np.fill_diagonal(cosine_matrix, 1)
np.fill_diagonal(jaccard_matrix, 1)

toc = time.time()

if showTime:
    print("Time: {:.4f}".format(toc-tic))

# Dump results into a CSV file
np.savetxt("cosine_" + OUT_PATH, cosine_matrix, fmt="%.4f", delimiter=',')
np.savetxt("jaccard_" + OUT_PATH, jaccard_matrix, fmt="%.4f", delimiter=',')