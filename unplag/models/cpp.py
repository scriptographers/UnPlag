import os
import glob
import argparse
import threading
import numpy as np
import seaborn as sns
from tqdm import tqdm
from models.ctokenizer import *
from models.extractutil import *
from django.core.files import File
from matplotlib import pyplot as plt
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import TfidfVectorizer


class CppPlagChecker(threading.Thread):
    def __init__(self, BASE_PATH, FILE_PATH, FILE_RE, OUT_PATH, OUTFILE, EXT, PLAG_POST, LOCK):
        super(CppPlagChecker, self).__init__()
        self.BASE_PATH = BASE_PATH
        self.FILE_RE = FILE_RE
        self.OUT_PATH = OUT_PATH
        self.OUTFILE = OUTFILE
        self.EXT = EXT
        self.FILE_PATH = FILE_PATH
        self.PLAG_POST = PLAG_POST
        self.LOCK = LOCK
    
    def run(self):
        self.LOCK.acquire()
        files = []
        problematic_files = []
        filelist = []

        if self.EXT == "gz":
            untar(self.FILE_PATH, self.BASE_PATH)
        elif self.EXT == "zip":
            unzip(self.FILE_PATH, self.BASE_PATH)
        elif self.EXT == "rar":
            unrar(self.FILE_PATH, self.BASE_PATH)

        print("extarct done")

        for filepath in tqdm(glob.glob(os.path.join(self.BASE_PATH, self.FILE_RE))):
            tokens = tokenize(filepath)
            if len(tokens) > 0:
                files.append(tokens)
                filelist.append(os.path.basename(filepath))
            else:
                # Files which result in empty tokens
                problematic_files.append(filepath)

        N_DOCS = len(filelist)
        self.PLAG_POST.file_count = N_DOCS
        self.PLAG_POST.save()
        # Check Integrity of uploaded compressed file
        if N_DOCS == 0:
            self.LOCK.release()
            return
        #######################
        
        # Show problematic files
        if len(problematic_files) > 0:
            print("The following files have some problem: ")
            for pf in problematic_files:
                print(pf)

        # A good reference for customizing TfIdf: http://www.davidsbatista.net/blog/2018/02/28/TfidfVectorizer/
        def identityFunction(file):
            return file

        VOCAB_LIMIT = 2000 # Can be increased if efficency is not an issue
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
            norm = "l2" # Each row will be unit normalized
        )

        S = vectorizer.fit_transform(files) # Vocabulary built is inside vectorizer.vocabulary_
        # linear_kernel computes the dot product of the sparse matrix:
        tfm = linear_kernel(S, S)

        # TF-IDF Heatmap
        # thm = sns.heatmap(tfm)
        # fig = thm.get_figure()    
        # fig.savefig("tfidf_heatmap.png", dpi=150)

        SAVE_PATH = os.path.join(self.OUT_PATH, "tfidf_" + self.OUTFILE + ".csv")
        np.savetxt(SAVE_PATH, tfm, fmt="%.4f", delimiter=',', header=','.join(filelist), comments='')

        csv_f = File(open(SAVE_PATH, 'r'))
        # time.sleep(20) # Uncomment to check
        self.PLAG_POST.outfile.save(SAVE_PATH, csv_f)
        self.LOCK.release()