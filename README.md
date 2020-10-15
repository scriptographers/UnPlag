# UnPlag Models

This branch contains all the models for ***Part 1: The Core Logic***.  
     
 ---  
   
 ### Models:
1. **(Unigram) Bag of Words Model**:
   - File : `bow2.py`
   - Usage: `python3 bow2.py -d <folder> -r <RegEx> -o <output>` or `python3 bow2.py --data <folder> --regex <RegEx> --output <output>`
      - `<folder>` - The folder containing the files to be checked
      - `<RegEx>` - Any RegEx applied to the file names (Eg. `*.txt`)
      - `<output>` - The path where the results (A `.csv` file) will be saved
      
---
   
<!-- ### Bonus:  
1. Language specific checking: Countering false positives by taking care of language specific features, syntax and stub code  -->
    
### Papers on Plagiarism Checking:  
1. [Winnowing: Local Algorithms for Document Fingerprinting
 (MOSS)](http://theory.stanford.edu/~aiken/publications/papers/sigmod03.pdf)
2. [Plagiarism Detection on Electronic Text based
Assignments using Vector Space Model](https://arxiv.org/ftp/arxiv/papers/1412/1412.7782.pdf)
3. [AntiPlag: Plagiarism Detection on Electronic
Submissions of Text Based Assignments](https://arxiv.org/ftp/arxiv/papers/1403/1403.1310.pdf)
     
---
     
### Testing Datasets:  
1. [A Corpus of (100) Plagiarised Short Answers](https://ir.shef.ac.uk/cloughie/resources/plagiarism_corpus.html)
   
---
   
### References:  
1. [Simple Plagiarism Detection Using NLP](https://medium.com/@heerambavi/simple-plagiarism-detection-using-nlp-1ee60c4f1d48)
2. [A Gentle Introduction to the Bag-of-Words Model](https://machinelearningmastery.com/gentle-introduction-bag-words-model/)
3. [(TF-IDF) How to compute the similarity between two text documents?
 (StackOverflow)](https://stackoverflow.com/questions/8897593/how-to-compute-the-similarity-between-two-text-documents)

