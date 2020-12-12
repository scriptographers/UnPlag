# Documentation for  the code

*Note: For the core logic part, we have not used any explicit functional/OOP logic. The files are simple well-commented python scripts meant to be used directly by using certain commands/options. They have been integrated into the Django REST backend in a similar way.*

## Dependencies
We require the following libraries for proper execution.
Run `pip install -r requirements.txt`, you may need to perform some additional steps for installing `clang`
- `os, glob`: For reading the data, applying the given RegEx
- `argparse`: For processing the command line arguments
- `numpy`: General scientific computation
- `tqdm`: For the command line based progress bar
- `unidecode`: For translating all unicode objects into ASCII
- `nltk`: For tokenizing the words, the [Porter Stemmer](https://tartarus.org/martin/PorterStemmer/) and english stop-words
- `matplotlib, seaborn`: Data visualization  
- `sklearn`:
	-  [`linear_kernel`](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.linear_kernel.html): For computing dot products between large sparse matrices.
	- [`TfIdfVectorizer`](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html): For building the n-gram based vocabulary, computing the TF-IDF weights
- `clang`: For parsing `c++` files, creating and traversing the AST, and tokenizing it.
*(Note: `clang` as used by us works only on `linux` based machines. You also may need to install it using `sudo apt-get`, and create symbolic links)*

## Usage (for textual files)

- **Main file:** `models/txt/tfidf.py`  
- **Direct usage:** 
	  `python3 tfidf.py -d <dataset> -r "<RegEx>" -out <output>`
    - `<dataset>`: This must contain the path to directory containing all the files which you want to check. The files are expected to be in English.
    - `<regEx>`: This must contain the regular expression for testing some subset of the files inside `<dataset>`. For example, if you have Java, C++ and text files in your dataset, and you want to check for plagiarism only for the text files, then your `<regEx>` will be `*.txt`.
    - `<output>`: This contains a string which determines where the output `.csv` file will be saved. For example, if `<output> = my_file.csv` then the output csv file is saved at `txt/results/tfidf_my_file.csv` 
- **Output:** Running the code generates:
    - A `.csv` file at `txt/results/tfidf_<output>`
    This contains the pairwise similarities between the pairs of files. The axis is indexed as `0,..., n-1` where `n` is the number of files, the index to file mapping can be found via running `ls -U` in the `<dataset>`.
    - A heatmap corresponding to the `.csv` file, at `txt/plots/tfidf_heatmap.png`, same indexing is followed as in the csv file. 
    - A progress bar will also been shown on the terminal, this indicates the progress made in reading, processing and tokenizing the files.
    - *Note: Analyzing this output for a large number of files may be cumbersome, so it is advised to use the front-end interface which contains much nicer interactive plots.*


## Usage (for C++ files)
- **Main file:** `models/cpp/tfidf.py`  
- **Direct usage:** 
	  `python3 tfidf.py -d <dataset> -r "<RegEx>" -out <output>`
    - `<dataset>`: This must contain the path to directory containing all the files which you want to check. The files are expected to be `C++` files.
    - `<regEx>`: This must contain the regular expression for testing some subset of the files inside `<dataset>`. For example, if you have Java, C++ and text files in your dataset, and you want to check for plagiarism only for the `C++` files, then your `<regEx>` will be `*.cpp`.
    - `<output>`: This contains a string which determines where the output `.csv` file will be saved. For example, if `<output> = my_file.csv` then the output csv file is saved at `cpp/results/tfidf_my_file.csv` 
- **Output:** Running the code generates:
    - A `.csv` file at `cpp/results/tfidf_<output>`
    This contains the pairwise similarities between the pairs of files. The axis is indexed as `0,..., n-1` where `n` is the number of files, the index to file mapping can be found via running `ls -U` in the `<dataset>`.
    - A heatmap corresponding to the `.csv` file, at `cpp/plots/tfidf_heatmap.png`, same indexing is followed as in the csv file. 
    - A progress bar will also been shown on the terminal, this indicates the progress made in reading, processing and tokenizing the files.
    - *Note: Analyzing this output for a large number of files may be cumbersome, so it is advised to use the front-end interface which contains much nicer interactive plots.*


## Usage (for Python-3 files)
- **Main file:** `models/python/tfidf.py`  
- **Direct usage:** 
	  `python3 tfidf.py -d <dataset> -r "<RegEx>" -out <output>`
    - `<dataset>`: This must contain the path to directory containing all the files which you want to check. The files are expected to be `Python-3` files.
    - `<regEx>`: This must contain the regular expression for testing some subset of the files inside `<dataset>`. For example, if you have Java, C++. Python and text files in your dataset, and you want to check for plagiarism only for the `Python-3` files, then your `<regEx>` will be `*.py`.
    - `<output>`: This contains a string which determines where the output `.csv` file will be saved. For example, if `<output> = my_file.csv` then the output csv file is saved at `python/results/tfidf_my_file.csv` 
- **Output:** Running the code generates:
    - A `.csv` file at `python/results/tfidf_<output>`
    This contains the pairwise similarities between the pairs of files. The axis is indexed as `0,..., n-1` where `n` is the number of files, the index to file mapping can be found via running `ls -U` in the `<dataset>`.
    - A heatmap corresponding to the `.csv` file, at `python/plots/tfidf_heatmap.png`, same indexing is followed as in the csv file. 
    - A progress bar will also been shown on the terminal, this indicates the progress made in reading, processing and tokenizing the files.
    - *Note: This was added after the project was officially closed, thus, this has not been integrated into the backend*
