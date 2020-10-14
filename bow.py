import numpy as np
from string import punctuation
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer 
from nltk.tokenize import word_tokenize, sent_tokenize # word tokenizer and sentence tokenizer

# Paths to the 2 files to be checked
PATH1 = "data/file1.txt"
PATH2 = "data/file2.txt"

# Reading input, currently only 2 files
with open(PATH1, encoding="utf-8") as f1:
    F1 = f1.read().lower()
with open(PATH2, encoding="utf-8") as f2:
    F2 = f2.read().lower()

# PREPROCESSING:

SW = stopwords.words("english") # Common english stop-words
ps = PorterStemmer() # TODO: Try more stemming algorithms

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

F1 = preprocess(F1)
F2 = preprocess(F2)

# Create the vocabulary
vocab = F1 + F2;
# Remove all duplicates
vocab = list(set(vocab))
# Sort lexicographically, doesnt actually matter, done for reproducible order inside the vocab
vocab.sort()

def sigvec(F):
    D = {word:0 for word in vocab}
    # Count frequency
    for word in F:
        D[word] += 1 
    # The actual words don't matter from now on, convert to frequency vector
    V = np.fromiter(D.values(), dtype=float)
    return V

def cosineSimilarity(F1, F2):
    V1 = sigvec(F1)
    V2 = sigvec(F2)
    # For n files, we need to implement featurewise normalization
    return (np.dot(V1, V2)/(np.linalg.norm(V1)*np.linalg.norm(V2)))

print(cosineSimilarity(F1, F2))

