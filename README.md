# UnPlag Models

This branch contains all the models for ***Part 1: The Core Logic***.  
     
 ---  
   
 ### Models:
1. **(Unigram) Bag of Words Model and TF-IDF**:
   - **File**: `detect.py`
   - **Usage**: `python3 detect.py -d <folder> -r "<RegEx>" -o <output>` or `python3 detect.py --data <folder> --regex <RegEx> --output <output> --time`
      - `<folder>` - The folder containing the files to be checked
      - `<RegEx>` - Any RegEx applied to the file names (Eg. `*.txt`)
      - `<output>` - The path where the results (A `.csv` file) will be saved
      - `--time` - Optional, displays the time taken for the "core logic" to execute 
   - **Output**: 3 files (`cosine_<output>, jaccard_<output>, tfidf_<output>`)  

---
   
<!-- 
### Bonus:  
1. Language specific checking: Countering false positives by taking care of language specific features, syntax and stub code (alt method: Select some statistic of the data as the threshold instead?)  
-->
    
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
     
### Testing Datasets:  
1. [A Corpus of (100) Plagiarised Short Answers](https://ir.shef.ac.uk/cloughie/resources/plagiarism_corpus.html)
2. [PAN Plagiarism Corpus 2011 (PAN-PC-11)](https://zenodo.org/record/3250095#.X5b8EIgzZPY) *(Not yet tried this dataset, it has many files, can be used for efficiency check atleast)*
   
---
   
### References:  
1. [Simple Plagiarism Detection Using NLP](https://medium.com/@heerambavi/simple-plagiarism-detection-using-nlp-1ee60c4f1d48)
2. [A Gentle Introduction to the Bag-of-Words Model](https://machinelearningmastery.com/gentle-introduction-bag-words-model/)
3. [(TF-IDF) How to compute the similarity between two text documents?
 (StackOverflow)](https://stackoverflow.com/questions/8897593/how-to-compute-the-similarity-between-two-text-documents)

