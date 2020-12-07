# Core logic

- Given a directory of `n` (english) text files `D`, for each file in `D`:
    - Read the contents of the file
    - Convert to lowercase
    - Remove punctuations
    - Remove non-ASCII characters
    - Tokenize the file into words
    - Remove english stop-words
-   Pass each token to the Porter stemmer, update the tokens using the output of the Porter stemmer
This completes the preprocessing and tokenization, we now have a list of tokens for each file in `D`. Let the output of this step be `T`
  
- Initialize the TF-IDF vectorizer from `sklearn`, override the default `preprocessor` and `tokenizer` with an identity function, since we have already preprocessed and tokenized our data.   
- Build the vocabulary using unigrams and bigrams (called "features"), if the vocabulary size exceeds 10000, only select the top 10000 features (this is done to ensure efficiency)   
- Fit the vectorizer on `T`, the result is a sparse matrix `S`, which is normalized row-wise.  
- Compute the similarity as a dot product using `sklearn.metrics.pairwise.linear_kernel`, this will be a numpy array of shape `(n, n)` containing the pairwise similarities.  