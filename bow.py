from string import punctuation
from nltk.tokenize import word_tokenize, sent_tokenize # word tokenizer and sentence tokenizer
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer 

# Run the following block once
##
# from nltk import download
# download("punkt")
# download("stopwords")
##

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
    return F

F1 = preprocess(F1)
F2 = preprocess(F2)

print(F1, F2)
