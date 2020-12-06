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
        # tic = time.time()
        self.LOCK.acquire()
        if self.EXT == "gz":
            untar(self.FILE_PATH, self.BASE_PATH)
        elif self.EXT == "zip":
            unzip(self.FILE_PATH, self.BASE_PATH)
        elif self.EXT == "rar":
            unrar(self.FILE_PATH, self.BASE_PATH)

        print("extarct doen")

        preprocessed_files = []
        unpreprocessed_files = []
        filelist = []

        # TODO: A more efficient way to extend to n files

        for filepath in glob.glob(os.path.join(self.BASE_PATH, self.FILE_RE)):
            with open(filepath, 'r', encoding="utf-8", errors="ignore") as f:
                F = f.read()
                filelist.append(os.path.basename(filepath))
                unpreprocessed_files.append(F)
                preprocessed_files.append(self.preprocess(F))

        N_DOCS = len(preprocessed_files)

        cosine_matrix  = np.zeros((N_DOCS, N_DOCS), dtype=float)
        jaccard_matrix = np.zeros((N_DOCS, N_DOCS), dtype=float)

        for i in range(N_DOCS):
            for j in range(i+1, N_DOCS):
                F1 = preprocessed_files[i]
                F2 = preprocessed_files[j]
                # Create the vocabulary
                vocab = F1 + F2
                # Remove all duplicates
                vocab = list(set(vocab))
                cosine_matrix[i, j]  = self.cosineSimilarity(F1, F2, vocab)
                jaccard_matrix[i, j] = self.jaccardSimilarity(F1, F2)

        # Utilize the symmetric nature of the matrix
        for i in range(N_DOCS):
            for j in range(i):
                cosine_matrix[i][j]  = cosine_matrix[j][i]
                jaccard_matrix[i][j] = jaccard_matrix[j][i]

        np.fill_diagonal(cosine_matrix, 1)
        np.fill_diagonal(jaccard_matrix, 1)

        # TF-IDF similarity matrix
        tfidf_matrix = self.TfIdfSimilarity(unpreprocessed_files) 
        
        tfidf_matrix_wfn = np.vstack([tfidf_matrix, filelist])
        # toc = time.time()

        # if showTime:
        #     print("Time: {:.4f}".format(toc-tic))

        # Heatmaps

        # ## Cosine Heatmap
        # chm = sns.heatmap(cosine_matrix)
        # fig1 = chm.get_figure()
        # fig1.savefig("plots/cosine_heatmap.png", dpi=150)   
        # plt.figure() 

        # ## Jaccard Heatmap
        # jhm = sns.heatmap(jaccard_matrix)
        # fig2 = jhm.get_figure()    
        # fig2.savefig("plots/jaccard_heatmap.png", dpi=150)
        # plt.figure()

        # ## TF-IDF Heatmap
        # thm = sns.heatmap(tfidf_matrix)
        # fig3 = thm.get_figure()    
        # fig3.savefig("plots/tfidf_heatmap.png", dpi=150)
        # plt.figure()

        # Dump results into a CSV file
        # np.savetxt("cosine_" + OUT_PATH, cosine_matrix, fmt="%.4f", delimiter=',')
        # SAVE_PATH = os.path.join(self.OUT_PATH, "jaccard_" + self.OUTFILE + ".csv")
        # np.savetxt(SAVE_PATH, jaccard_matrix, fmt="%.4f", delimiter=',')
        SAVE_PATH = os.path.join(self.OUT_PATH, "tfidf_" + self.OUTFILE + ".csv")
        np.savetxt(SAVE_PATH, tfidf_matrix_wfn, fmt="%.10s", delimiter=',')  

        csv_f = File(open(SAVE_PATH, 'r'))
        # time.sleep(20) # Uncomment to check
        self.PLAG_POST.outfile.save(SAVE_PATH, csv_f)
        self.LOCK.release()