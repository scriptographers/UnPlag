import os
import glob
import time
import argparse
import numpy as np
import seaborn as sns
from tqdm import tqdm
from sklearn.manifold import TSNE
from matplotlib import pyplot as plt
from features import extractFeatures
from sklearn.preprocessing import MinMaxScaler, StandardScaler

# Arguments parsing
parser = argparse.ArgumentParser()
parser.add_argument("--data", "-d", type=str, required=True)
parser.add_argument("--regex", "-r", type=str, required=True)
parser.add_argument("--output", "-out", type=str, required=True)
args = parser.parse_args()

BASE_PATH = args.data
FILE_RE   = args.regex
OUT_PATH  = args.output

# Create Nx21 dimensional unlabelled data
idxToPath = []
X = []
for filepath in tqdm(glob.glob(os.path.join(BASE_PATH, FILE_RE))):
     X.append(extractFeatures(filepath))
     idxToPath.append(filepath) 
N_DOCS = len(X)
X = np.array(X, dtype=float)

# Since different features have different units:
scaler = StandardScaler()
X = scaler.fit_transform(X)

# Visualize the distribution in 2D using t-SNE:
X_lower = TSNE(n_components=2, perplexity=10, n_iter=2000).fit_transform(X)
sc = sns.scatterplot(x = X_lower[:, 0], y = X_lower[:, 1], size=1)
fig = sc.get_figure()    
fig.savefig("plots/tSNE.jpg", dpi=150)

# Find pairs with high similarity based on Euclidean distance:
print("Based on euclidean distance: ")
THRESH = 0.2 # Hyperparameter
for i in range(N_DOCS):
    for j in range(i+1, N_DOCS):
        euclidean_dist = np.linalg.norm(X[i] - X[j])
        #print(euclidean_dist)
        if euclidean_dist <= THRESH:
            print("High similarity in {} and {}".format(idxToPath[i], idxToPath[j]))


# Find pairs with high similarity based on cosine similarity:
print("")
print("Based on cosine similarity")
THRESH_CS = 0.998 # Hyperparameter
for i in range(N_DOCS):
    for j in range(i+1, N_DOCS):
        cs = np.dot(X[i], X[j])/(np.linalg.norm(X[i])*np.linalg.norm(X[j]))
        if cs >= THRESH_CS:
            print("High similarity in {} and {}".format(idxToPath[i], idxToPath[j]))

# Hyperparameters: Euclidean distance: 0.2, Cosine similarity: 0.998