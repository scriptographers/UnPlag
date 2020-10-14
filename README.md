# UnPlag Models

This branch contains all the models for `Part 1: The Core Logic`.  
   
1. (Unigram) Bag of Words Model:
- File : `bow2.py`
- Usage: `python bow2.py -d data/ -r *.txt -o results.csv`
 
---

Input: Compressed folder of files  
Output: Similarity metrics between each pair of files and the visualization for the same.   

Bonus:  

1. Language specific:   
Countering false positives by taking care of language specific features, syntax and stub code  

---

Papers on Plagiarism Checking:  
1. [MOSS](http://theory.stanford.edu/~aiken/publications/papers/sigmod03.pdf)
2. [Vector Space Models](https://arxiv.org/ftp/arxiv/papers/1412/1412.7782.pdf)
    
Testing Datasets:  
1. [Created by Paul Clough (Information Studies) and Mark Stevenson (Computer Science), University of Sheffield](https://ir.shef.ac.uk/cloughie/resources/plagiarism_corpus.html)

---

References:  
1. [Medium Article](https://medium.com/@heerambavi/simple-plagiarism-detection-using-nlp-1ee60c4f1d48)
2. [Bag of Words](https://machinelearningmastery.com/gentle-introduction-bag-words-model/)
3. [TF-IDF](https://stackoverflow.com/questions/8897593/how-to-compute-the-similarity-between-two-text-documents)

