import os
import glob
import time
import argparse
import threading
import numpy as np
import seaborn as sns
from tqdm import tqdm
from models.extractutil import *
from string import punctuation
from unidecode import unidecode
from nltk.corpus import stopwords
from django.core.files import File
from nltk.stem import PorterStemmer 
from matplotlib import pyplot as plt
from nltk.tokenize import word_tokenize
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import TfidfVectorizer

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

    # Preprocessing and tokenizing:
    def preprocessAndTokenize(self, F):
        F = F.lower() 
        F.translate(str.maketrans('', '', punctuation))
        F = unidecode(F) # Equivalent to strip_ascii of TfIdfVectorizer
        F = word_tokenize(F)
        F = [self.ps.stem(f) for f in F if f.isalnum() and f not in self.SW]
        return F
    
    def run(self):
        self.LOCK.acquire()
        if self.EXT == "gz":
            untar(self.FILE_PATH, self.BASE_PATH)
        elif self.EXT == "zip":
            unzip(self.FILE_PATH, self.BASE_PATH)
        elif self.EXT == "rar":
            unrar(self.FILE_PATH, self.BASE_PATH)

        print("extract done")
        tokenized_files = []
        filelist = []

        for filepath in tqdm(glob.glob(os.path.join(self.BASE_PATH, self.FILE_RE))):
            with open(filepath, 'r', encoding="utf-8", errors="ignore") as f:
                filelist.append(os.path.basename(filepath))
                contents = f.read()
                tokens = self.preprocessAndTokenize(contents)
                tokenized_files.append(tokens)

        N_DOCS = len(filelist)
        self.PLAG_POST.file_count = N_DOCS
        self.PLAG_POST.save()
        # Check Integrity of uploaded compressed file
        if N_DOCS == 0:
            self.LOCK.release()
            return
        #######################

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
            sublinear_tf = True,
            norm = "l2" # Each row will be unit normalized
        )

        S = vectorizer.fit_transform(tokenized_files) # Vocabulary built is inside vectorizer.vocabulary_
        # linear_kernel computes the dot product of the sparse matrix:
        tfm = linear_kernel(S, S)

        # TF-IDF Heatmap
        # thm = sns.heatmap(tfm)
        # fig = thm.get_figure()    
        # fig.savefig("plots/tfidf_heatmap.png", dpi=150)

        # Dump results into a CSV file
        SAVE_PATH = os.path.join(self.OUT_PATH, "tfidf_" + self.OUTFILE + ".csv")
        np.savetxt(SAVE_PATH, tfm, fmt="%.4f", delimiter=',', header=','.join(filelist), comments='')  

        csv_f = File(open(SAVE_PATH, 'r'))
        # time.sleep(20) # Uncomment to check
        self.PLAG_POST.outfile.save(SAVE_PATH, csv_f)
        self.LOCK.release()
