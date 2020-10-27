# UnPlag Models

This branch contains all the models for ***Part 1: The Core Logic***.  
     
 ---  
   
 ### Models implemented so far:
**(Unigram) Bag of Words Model and TF-IDF**:
   - Language used: `Python 3.8.2`
   - Libraries used:
     - **`nltk`**: Used for removing stopwords, Porter stemming and word tokenization
     - **`sklearn`**: Used the `TfidfVectorizer`
     - **`collections`**: Used `Counter` while computing the Jaccard similarity
     - **`numpy`**: Used for basic vector operations and for computing the cosine similarities
     - **`argparse`**: Used for parsing the command line arguments
     - **`glob`** : Used for iterating through the given folder of files based on the given RegEx
   - **File**: `detect.py`
   - **Similarity metrics used for the model**: Cosine similarity and Jaccard similarity
   - **Usage**:   
   `python3 detect.py -d <folder> -r "<RegEx>" -o <output>`   
   (or)  
   `python3 detect.py --data <folder> --regex "<RegEx>" --output <output> --time`   
   Arguments description:   
      - `<folder>` - The folder containing the files to be checked
      - `<RegEx>` - Any RegEx applied to the file names inside the folder (Eg. `*.txt`)
      - `<output>` - The path where the results (A `.csv` file) will be saved
      - `--time` - Optional, displays the time taken for the "core logic" to execute   
   Example usage: `python3 detect.py -d ./datasets/data/ -r "*.txt" -o results.csv --time`   
   - **Output**: 3 files (`cosine_<output>, jaccard_<output>, tfidf_<output>`)
   
---
   
### Plans for Phase-2:
- Try to find an accurately labelled dataset for testing/evaluating all the models
- Extend the above models to work well with `C++` files (Handling functional calls, language specific syntax, stub code)
- Experiment with more models and try to implement ideas from relevant research papers
- Look for different ways to visualize the matrix to gain valuable insights
     
---
    
### Papers on Plagiarism Checking:  
1. [Winnowing: Local Algorithms for Document Fingerprinting
 (MOSS)](http://theory.stanford.edu/~aiken/publications/papers/sigmod03.pdf)
2. [Plagiarism Detection on Electronic Text based
Assignments using Vector Space Model](https://arxiv.org/ftp/arxiv/papers/1412/1412.7782.pdf)
3. [AntiPlag: Plagiarism Detection on Electronic
Submissions of Text Based Assignments](https://arxiv.org/ftp/arxiv/papers/1403/1403.1310.pdf)
4. [Universal Sentence Encoder](https://arxiv.org/abs/1803.11175) (Pre-trained model by Google Research)
5. [BERTScore: Evaluating Text Generation with BERT](https://arxiv.org/abs/1904.09675)
     
---
     
### Possible Testing Datasets:  
1. [A Corpus of (100) Plagiarised Short Answers](https://ir.shef.ac.uk/cloughie/resources/plagiarism_corpus.html)
2. [PAN Plagiarism Corpus 2011 (PAN-PC-11)](https://zenodo.org/record/3250095#.X5b8EIgzZPY) *(Not yet tried this dataset, it has many files, can be used for efficiency check atleast)*
   
---
   
### References used till now:  
1. [Simple Plagiarism Detection Using NLP](https://medium.com/@heerambavi/simple-plagiarism-detection-using-nlp-1ee60c4f1d48)
2. [A Gentle Introduction to the Bag-of-Words Model](https://machinelearningmastery.com/gentle-introduction-bag-words-model/)
3. [(TF-IDF) How to compute the similarity between two text documents?
 (StackOverflow)](https://stackoverflow.com/questions/8897593/how-to-compute-the-similarity-between-two-text-documents)

