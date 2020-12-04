import os
import glob
import time
import argparse
import numpy as np
import seaborn as sns
from tqdm import tqdm
from collections import Counter
from ctokenizer import CTokenizer
from matplotlib import pyplot as plt

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
    return (np.dot(V1, V2)/(np.linalg.norm(V1)*np.linalg.norm(V2)))

# Computes the Jaccard similarity between 2 preprocessed_files
def jaccardSimilarity(F1, F2):
    n1, n2 = len(F1), len(F2)
    D1, D2 = Counter(F1), Counter(F2)
    D = D1 & D2 # Intersection
    ni = sum(D.values())
    nu = n1 + n2 - ni # Union
    if nu == 0:
        print("n1: ", n1, " n2:", n2)
        raise ValueError("nu is set to 0")
    niou = ni/nu # Jaccard Similarity: Intersection over Union
    return niou

# MAIN:
tic = time.time()

# TODO: A more efficient way to extend to n files
files = []
problematic_files = []
for filepath in tqdm(glob.glob(os.path.join(BASE_PATH, FILE_RE))):
    t = CTokenizer(filepath)
    tokens = t.rawTokenization()
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

cosine_matrix  = np.zeros((N_DOCS, N_DOCS), dtype=float)
jaccard_matrix = np.zeros((N_DOCS, N_DOCS), dtype=float)

for i in range(N_DOCS):
    for j in range(i+1, N_DOCS):
        F1 = files[i]
        F2 = files[j]
        # Create the vocabulary
        vocab = F1 + F2;
        # Remove all duplicates
        vocab = list(set(vocab))
        cosine_matrix[i, j]  = cosineSimilarity(F1, F2, vocab)
        jaccard_matrix[i, j] = jaccardSimilarity(F1, F2)

# Utilize the symmetric nature of the matrix
for i in range(N_DOCS):
    for j in range(i):
        cosine_matrix[i][j]  = cosine_matrix[j][i]
        jaccard_matrix[i][j] = jaccard_matrix[j][i]

np.fill_diagonal(cosine_matrix, 1)
np.fill_diagonal(jaccard_matrix, 1)

toc = time.time()

if showTime:
    print("Time: {:.4f}".format(toc-tic))

# Heatmaps

## Cosine Heatmap
chm = sns.heatmap(cosine_matrix)
fig1 = chm.get_figure()
fig1.savefig("plots/cosine_heatmap.png", dpi=150)   
plt.figure() 

## Jaccard Heatmap
jhm = sns.heatmap(jaccard_matrix)
fig2 = jhm.get_figure()    
fig2.savefig("plots/jaccard_heatmap.png", dpi=150)
plt.figure()

# Dump results into a CSV file
np.savetxt("results/cosine_" + OUT_PATH, cosine_matrix, fmt="%.4f", delimiter=',')
np.savetxt("results/jaccard_" + OUT_PATH, jaccard_matrix, fmt="%.4f", delimiter=',')

# Thresholded results:
# thresh = 0.8
# csm_t = (cosine_matrix > thresh)
# csm_t = csm_t.astype(float)
# ## Cosine Heatmap
# chmt = sns.heatmap(csm_t)
# fig3 = chmt.get_figure()
# fig3.savefig("plots/cosine_heatmap_thresholded.png", dpi=150)   
# plt.figure()