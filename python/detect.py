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
from sklearn.preprocessing import StandardScaler

# Arguments parsing
parser = argparse.ArgumentParser()
parser.add_argument("--data", "-d", type=str, required=True)
parser.add_argument("--regex", "-r", type=str, required=True)
parser.add_argument("--output", "-out", type=str, required=True)
args = parser.parse_args()

BASE_PATH = args.data
FILE_RE   = args.regex
OUT_PATH  = args.output

# Create NxD dimensional unlabelled data
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
# X_lower = TSNE(n_components=2, perplexity=4, n_iter=1000).fit_transform(X)
# sc = sns.scatterplot(x = X_lower[:, 0], y = X_lower[:, 1], size=1)
# fig = sc.get_figure()    
# fig.savefig("plots/tSNE.jpg", dpi=150)

# Find pairs with high similarity based on Euclidean distance:
# print("Based on euclidean distance: ")
# THRESH = 0.2 # Hyperparameter
# for i in range(N_DOCS):
#     for j in range(i+1, N_DOCS):
#         euclidean_dist = np.linalg.norm(X[i] - X[j])
#         print(idxToPath[i], idxToPath[j], euclidean_dist)
#         if euclidean_dist <= THRESH:
#             print("High similarity in {} and {}".format(idxToPath[i], idxToPath[j]))

cosine_matrix  = np.zeros((N_DOCS, N_DOCS), dtype=float)

for i in range(N_DOCS):
    for j in range(i+1, N_DOCS):
        cs = np.dot(X[i], X[j])/(np.linalg.norm(X[i])*np.linalg.norm(X[j]))
        if cs > 0.7:
            print(idxToPath[i], idxToPath[j], cs)
        cosine_matrix[i, j] = cs

# Utilize the symmetric nature of the matrix
for i in range(N_DOCS):
    for j in range(i):
        cosine_matrix[i][j]  = cosine_matrix[j][i]

np.fill_diagonal(cosine_matrix, 1)

# Cosine Heatmap
chm = sns.heatmap(cosine_matrix)
fig1 = chm.get_figure()
fig1.savefig("plots/cosine_heatmap_1.png", dpi=150)   
plt.figure() 

# Dump results into a CSV file
np.savetxt("results/cosine_" + OUT_PATH, cosine_matrix, fmt="%.4f", delimiter=',')

# print(idxToPath)