# UnPlag
Course project for **CS 251: Software Systems Lab**   

# Plan of Action
## Completed :
### Backend
1. Implemented Backend with **Django 3** and **Django REST Framework**
2. Used **JWT based User Authentication**
3. Created serializers for Login, Register, Change Password
4. Created a User Profile Model
5. Created serializers for View Profile and update Profile
6. Created PlagSample Model which stores the zip file uploaded by the user and the corresponding processed csv file.
7. Created serializers for uploading zip files, dowloading csv files and history of uploads
### Frontend
1. Implemented Frontend with **AngularTS 9.0**
2. Created components for Register, Login, Change Password, Dashboard, Profile, Edit Profile, Upload and Download
3. Added **JWT support** in **Auth Service** which takes care of Login, Register as well as Refreshing of Tokens
4. Added **HTTP Interceptor** which added the token if present to the header whenever required.
5. Added **HTTP Guard** to prevent unauthorized user to visit urls which are meant for only certain users.
6. Added **DataService** to upload zip files and download the csv file and display it (for now as a table).
### Models
1. Created and tested models for text files.
2. Fill

## How to run :
### Backend
1. Fill
### Frontend
1. Fill

## Tasks ahead :
### Backend
1. Fill
### Frontend :
1. Design and styling using SCSS/CSS
### Models :
1. Fill

# Backend - API Documentation

## API Endpoints Implemented (Links given to the detailed documentation)

### Token API Endpoints :
1. ['/api/token/'](#token)
2. ['/api/token/refresh/'](#token-refresh)

### Account API Endpoints :
3. ['/api/account/signup/'](#user-signup)
4. ['/api/account/profile/'](#profile-details)
5. ['/api/account/update/'](#profile-update)
6. ['/api/account/upassword/'](#password-update)
7. ['/api/account/pastchecks/'](#get-past-plagchecks)
### Plagsample API Endpoints :
8. ['/api/plagsample/upload/'](#upload-files)
9. ['/api/plagsample/download/'](#download-csv)


## Detailed API Documentation

### Token

```ENDPOINT : '/api/token/' | REQUEST TYPE : POST```

Returns an 'access' and a 'refresh' **JWT token** for a given valid 'username' and 'password'.
```
Format :

@[in body] username, password
@[JSON response] username, userid, access, refresh
```

### Token Refresh

```ENDPOINT : '/api/token/refresh/' | REQUEST TYPE : POST```

Returns an 'access' token for a given valid 'refresh' token.
```
Format:

@[in body] refresh
@[JSON response] access
```

### User Signup

```ENDPOINT : 'api/account/signup/' | REQUEST TYPE : POST```

Returns a 'username', 'userid' and the 'access' and 'refresh' JWT tokens, for a given valid 'username', 'password', 'password2'
```
Format:

@[in body] username, password, password2
@[JSON response] response(string), username, userid, access, refresh
```

### Profile Details

```ENDPOINT : 'api/account/profile/' | REQUEST TYPE : GET (Authenticated Endpoint)```

Returns profile details of the current authenticated user.
```
Format:

@[in header] “Authorization: Bearer <access>”
@[JSON response] id(profile id), user(user id), username, nick
```

### Profile Update

```ENDPOINT : 'api/account/update/' | REQUEST TYPE : PUT (Authenticated Endpoint)```

Updates the profile with the given input data.
```
Format:

@[in header] “Authorization: Bearer <access>”
@[in body] nick(optional and it's the only field as of now)
@[JSON response] id(profile id), user(user id), username, nick
```

### Password Update

```ENDPOINT : 'api/account/upassword/' | REQUEST TYPE : PUT (Authenticated Endpoint)```

Updates the user password.
```
Format:

@[in header] “Authorization: Bearer <access>”
@[in body] old_password, new_password (required fields)
@[JSON response] status : ‘success’, message : ‘Password updated successfully’
```

### Get Past PlagChecks

```ENDPOINT : 'api/account/pastchecks/' | REQUEST TYPE : GET (Authenticated Endpoint)```

Returns a list of past plagiarism check IDs by the user along with the uploaded filename.
```
Format:

@[in header] “Authorization: Bearer <access>”
@[in body]
@[JSON response]
{
   "pastchecks": [
       {
           "filename": "filename1.xip",
           "id": 10,
           "date-posted": "2020-10-25T16:29:12.954791Z"
       },
       ...,
       ...
   ]
}
```

### Upload Files

```ENDPOINT : 'api/plagsample/upload/' | REQUEST TYPE : POST (Authenticated Endpoint)```

Returns a plagiarism check id for the uploaded compressed file.
```
Format:

@[in header] “Authorization: Bearer <access>”
@[in body] plagzip (Filefields) (As of now zip, tar.gz, rar are allowed, but just checking extensions wont work !)
@[JSON response] id(plagsample id), plagzip(name of the files), user(user id), date_posted, outfile (name of output csv)
```

### Download CSV

```ENDPOINT : 'api/plagsample/download/<id>' | REQUEST TYPE : GET (Authenticated Endpoint)```

Returns the processed CSV file as a JSON file attachment response blob(If the authentication details match correctly).
```
Format:

@[in header] “Authorization: Bearer <access>”
@[out]  CSV is returned as a file attachment in the body(as a file Blob). Name of the file can be found under the "Content-Disposition" header.
@[out in case of error] JSON form of error is returned along with correct HTTP error code.
```


---
  
## *Part 1: The Core Logic* 
    
### Models implemented so far:
**(Unigram) Bag of Words Model and TF-IDF**:
   - Language used: `Python 3.8.2`
   - Libraries used:
     - **`nltk`**: Used for removing stopwords, Porter stemming and word tokenization
     - **`sklearn`**: Used the `TfidfVectorizer`
     - **`collections`**: Used `Counter` while computing the Jaccard similarity
     - **`numpy`**: Used for basic vector operations and for computing the cosine similarities
     - **`seaborn`**: Used for creating heatmaps
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
   - **Output**: 
      - 3 files (`cosine_<output>, jaccard_<output>, tfidf_<output>`)
      - 2 heatmaps corresponding to each similarity metric and one heatmap for TF-IDF 
   
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


