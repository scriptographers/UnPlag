# Dependencies:
We require the following libraries for proper execution.

- `os, glob`: For reading the data, applying the given RegEx
- `argparse`: For processing the command line arguments
- `numpy`: General scientific computation
- `tqdm`: For the progress bar
- `unidecode`: For translating all unicode objects into ASCII
- `nltk`: For tokenizing the words, the [Porter Stemmer](https://tartarus.org/martin/PorterStemmer/) and english stop-words
- `matplotlib, seaborn`: Data visualization  
- `sklearn`: [`linear_kernel`](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.linear_kernel.html): For computing dot products between large sparse matrices, and for the [`TfIdfVectorizer`](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html)