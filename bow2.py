import os
import glob
import numpy as np
from string import punctuation
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer 
from nltk.tokenize import word_tokenize, sent_tokenize # word tokenizer and sentence tokenizer

# Global variables
SW = stopwords.words("english") # Common english stop-words
ps = PorterStemmer() # TODO: Try more stemming algorithms

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
    D = {word:0 for word in vocab}
    # Count frequency
    for word in F:
        D[word] += 1 
    # The actual words don't matter from now on, convert to frequency vector
    V = np.fromiter(D.values(), dtype=float)
    return V

# Computed cosine similarity between 2 preprocessed_files
def cosineSimilarity(F1, F2, vocab):
    V1 = sigvec(F1, vocab)
    V2 = sigvec(F2, vocab)
    # For n files, we need to implement featurewise normalization
    return (np.dot(V1, V2)/(np.linalg.norm(V1)*np.linalg.norm(V2)))

BASE_PATH = "data/"
FILE_RE   = "*.txt"

preprocessed_files = []

# TODO: A more efficient way to extend to n files

for filepath in glob.glob(os.path.join(BASE_PATH, FILE_RE)):
    with open(filepath, encoding="utf-8") as f:
        F = f.read()
        preprocessed_files.append(preprocess(F))

N_DOCS = len(preprocessed_files)

similarity_matrix = np.zeros((N_DOCS, N_DOCS), dtype=float)

for i in range(N_DOCS):
    for j in range(N_DOCS):
        if (j > i) :
            F1 = preprocessed_files[i]
            F2 = preprocessed_files[j]
            # Create the vocabulary
            vocab = F1 + F2;
            # Remove all duplicates
            vocab = list(set(vocab))
            # Sort lexicographically, doesnt actually matter, done for reproducible order inside the vocab
            vocab.sort()
            similarity_matrix[i, j] = cosineSimilarity(F1, F2, vocab)

print(similarity_matrix)
