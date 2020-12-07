import os
import glob
import time
import numpy as np
import seaborn as sns
import threading
from string import punctuation
from collections import Counter
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer 
from matplotlib import pyplot as plt
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer as tfidfv 
from models.extractutil import *
from django.core.files import File

class TxtPlagChecker(threading.Thread):
    def __init__(self, BASE_PATH, FILE_PATH, FILE_RE, OUT_PATH, OUTFILE, EXT, PLAG_POST, LOCK):
        super(TxtPlagChecker, self).__init__()
        self.BASE_PATH = BASE_PATH
        self.FILE_RE = FILE_RE
        self.OUT_PATH = OUT_PATH
        self.OUTFILE = OUTFILE
        self.EXT = EXT
        self.FILE_PATH = FILE_PATH
        self.PLAG_POST = PLAG_POST
        self.LOCK = LOCK

        # Global variables
        self.SW = stopwords.words("english") # Common english stop-words
        self.ps = PorterStemmer() # TODO: Try more stemming algorithms

    # FUNCTIONS

    # Preprocessing:
    def preprocess(self, F):
        # 1. Convert to lowercase
        F = F.lower() 
        # 2. Remove all punctuations
        F.translate(str.maketrans('', '', punctuation))
        # 3. Tokenize the words
        F = word_tokenize(F)
        # 4. Stem each word and remove all stop_words (can also use isalpha() here)
        F = [self.ps.stem(f) for f in F if f.isalnum() and f not in self.SW] # TODO: Make this more efficient
        # We can also use PySpellChecker to correct common mispellings, but that may decrease the efficiency
        return F

    # Creates the signature vector for a file
    def sigvec(self, F, vocab):
        # TODO: A more efficient way needed
        D = {word:0 for word in vocab}
        # Count frequency
        for word in F:
            D[word] += 1 
        # The actual words don't matter from now on, convert to frequency vector
        V = np.fromiter(D.values(), dtype=float)
        return V

    # Computes the cosine similarity between 2 preprocessed_files
    def cosineSimilarity(self, F1, F2, vocab):
        V1 = self.sigvec(F1, vocab)
        V2 = self.sigvec(F2, vocab)
        return (np.dot(V1, V2)/(np.linalg.norm(V1)*np.linalg.norm(V2)))

    # Computes the Jaccard similarity between 2 preprocessed_files
    def jaccardSimilarity(self, F1, F2):
        n1, n2 = len(F1), len(F2)
        D1, D2 = Counter(F1), Counter(F2)
        D = D1 & D2 # Intersection
        ni = sum(D.values())
        nu = n1 + n2 - ni # Union
        niou = ni/nu # Jaccard Similarity: Intersection over Union
        return niou

    # TF-IDF Approach
    def TfIdfSimilarity(self, files):
        S = tfidfv(
            decode_error="ignore", # Ignore encoding errors
            stop_words = "english",
            strip_accents="ascii", # Removes characters like: á
            norm="l2"
        ).fit_transform(files) # Converts list of files to TF-IDF features
        # S is already normalized, ||S|| = 1, thus cosine similarity: S*S.T
        similarity = S*S.T # Of the type: scipy.sparse.csr.csr_matrix
        similarity = similarity.toarray() # Converting into a standard numpy array
        return similarity

    # MAIN:
    def run(self):
        self.LOCK.acquire()
        if self.EXT == "gz":
            untar(self.FILE_PATH, self.BASE_PATH)
        elif self.EXT == "zip":
            unzip(self.FILE_PATH, self.BASE_PATH)
        elif self.EXT == "rar":
            unrar(self.FILE_PATH, self.BASE_PATH)

        print("extarct done")

        preprocessed_files = []
        unpreprocessed_files = []
        filelist = []

        # TODO: A more efficient way to extend to n files

        for filepath in glob.glob(os.path.join(self.BASE_PATH, self.FILE_RE)):
            with open(filepath, 'r', encoding="utf-8", errors="ignore") as f:
                F = f.read()
                filelist.append(os.path.basename(filepath))
                unpreprocessed_files.append(F)

        N_DOCS = len(filelist)
        self.PLAG_POST.file_count = N_DOCS
        self.PLAG_POST.save()
        # Check Integrity of uploaded compressed file
        if N_DOCS == 0:
            self.LOCK.release()
            return
        #######################

        # TF-IDF similarity matrix
        tfidf_matrix = self.TfIdfSimilarity(unpreprocessed_files) 
        
        tfidf_matrix_wfn = np.vstack([filelist, tfidf_matrix])
        
        # Dump results into a CSV file
        SAVE_PATH = os.path.join(self.OUT_PATH, "tfidf_" + self.OUTFILE + ".csv")
        np.savetxt(SAVE_PATH, tfidf_matrix_wfn, fmt="%s", delimiter=',')  

        csv_f = File(open(SAVE_PATH, 'r'))
        # time.sleep(20) # Uncomment to check
        self.PLAG_POST.outfile.save(SAVE_PATH, csv_f)
        self.LOCK.release()