# UnPlag

Course project for **CS 251: Software Systems Lab**

---

## **How to run**

### Backend

```
cd to UnPlag/
python3 -m venv UnPlag
source UnPlag/bin/activate
pip install -r requirements.txt
cd unplag
python manage.py makemigrations account plagsample organization
python manage.py migrate
python manage.py runserver
```

### Frontend

```
cd to UnPlag/
cd frontend
npm install
ng serve
```

### Command Line Interface

```
cd to UnPlag/
cd cli
npm install
npm link
```

---

---

## **Core Logic**

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
2. [PAN Plagiarism Corpus 2011 (PAN-PC-11)](https://zenodo.org/record/3250095#.X5b8EIgzZPY) _(Not yet tried this dataset, it has many files, can be used for efficiency check atleast)_

---

### References used till now:

1. [Simple Plagiarism Detection Using NLP](https://medium.com/@heerambavi/simple-plagiarism-detection-using-nlp-1ee60c4f1d48)
2. [A Gentle Introduction to the Bag-of-Words Model](https://machinelearningmastery.com/gentle-introduction-bag-words-model/)
3. [(TF-IDF) How to compute the similarity between two text documents?
   (StackOverflow)](https://stackoverflow.com/questions/8897593/how-to-compute-the-similarity-between-two-text-documents)

---

---

## **UnPlag Backend API Documentation**

### API Endpoints Implemented (Links given to the detailed documentation)

#### Token API Endpoints :

1. ['/api/token/'](#token)
2. ['/api/token/refresh/'](#token-refresh)

#### Account API Endpoints :

3. ['/api/account/signup/'](#user-signup)
4. ['/api/account/profile/'](#profile-details)
5. ['/api/account/update/'](#profile-update)
6. ['/api/account/upassword/'](#password-update)
7. ['/api/account/pastchecks/'](#get-past-plagchecks)

#### Plagsample API Endpoints :

8. ['/api/plagsample/upload/'](#upload-files)
9. ['/api/plagsample/download/<int:id>/'](#download-csv)
10. ['/api/plagsample/info/<int:id>/'](#plagsample-info)

#### Organization API Endpoints :

11. ['/api/organization/makeorg/'](#create-new-organization)
12. ['/api/organization/get/<int:id>/'](#organization-info)
13. ['/api/organization/update/<int:id>/'](#update-organization)
14. ['/api/organization/joinorg/'](#join-organization)

### Detailed API Documentation

#### **Token**

`ENDPOINT : '/api/token/' | REQUEST TYPE : POST`

Returns an 'access' and a 'refresh' **JWT token** for a given valid 'username' and 'password'

```
Format :

@[in body] username, password
@[JSON response] username, userid, access, refresh
```

#### **Token Refresh**

`ENDPOINT : '/api/token/refresh/' | REQUEST TYPE : POST`

Returns an 'access' token for a given valid 'refresh' token

```
Format:

@[in body] refresh
@[JSON response] access
```

#### **User Signup**

`ENDPOINT : 'api/account/signup/' | REQUEST TYPE : POST`

Returns a 'username', 'userid' and the 'access' and 'refresh' JWT tokens, for a given valid 'username', 'password', 'password2'

```
Format:

@[in body] username, password, password2
@[JSON response] response(string), username, userid, access, refresh
```

#### **Profile Details**

`ENDPOINT : 'api/account/profile/' | REQUEST TYPE : GET (Authenticated Endpoint)`

Returns profile details of the current authenticated user

```
Format:

@[in header] “Authorization: Bearer <access>”
@[JSON response] id(profile id), user(user id), username, nick, orgs: [{org_id, org_name},...]
```

#### **Profile Update**

`ENDPOINT : 'api/account/update/' | REQUEST TYPE : PUT (Authenticated Endpoint)`

Updates the profile with the given input data

```
Format:

@[in header] “Authorization: Bearer <access>”
@[in body] nick(optional and it's the only field as of now)
@[JSON response] id(profile id), user(user id), username, nick
```

#### **Password Update**

`ENDPOINT : 'api/account/upassword/' | REQUEST TYPE : PUT (Authenticated Endpoint)`

Updates the user password

```
Format:

@[in header] “Authorization: Bearer <access>”
@[in body] old_password, new_password (required fields)
@[JSON response] status : ‘success’, message : ‘Password updated successfully’
```

#### **Get Past PlagChecks**

`ENDPOINT : 'api/account/pastchecks/' | REQUEST TYPE : GET (Authenticated Endpoint)`

Returns a list of past plagiarism check IDs by the user along with the uploaded filename

```
Format:

@[in header] “Authorization: Bearer <access>”
@[in body]
@[JSON response] // Sorted by org_id and then date_posted.
{
   "pastchecks": [
       {
           "filename": "Outlab5-Resources.tar_e3Ce4OJ.gz",
           "file_type": "txt"
           "id": 2,
           "name": "Outlab5-Resources",
           "timestamp": "2020-11-26 20:15:30",
           "org_id": "1",
           "org_name": "scriptographers",
       },
       ...,
       ...
   ]
}
```

#### **Upload Files**

`ENDPOINT : 'api/plagsample/upload/' | REQUEST TYPE : POST (Authenticated Endpoint)`

Returns a plagiarism check id for the uploaded compressed file
Supplied org_id must be valid and the user must be in it

This method processes the uploaded compressed file on a separate thread, so as to keep the backend open to further uploads.

```
Format:

@[in header] “Authorization: Bearer <access>”
@[in body] name, org_id, file_type(must, available choices : [“txt”, “cpp”]),
plagzip (Filefields) (As of now zip, tar.gz, rar are allowed)
@[JSON response] id(plagsample id), name, file_type, plagzip(name of the files),
user(user id), date_posted, outfile (name of output csv)
```

#### **Download CSV**

`ENDPOINT : 'api/plagsample/download/<id>' | REQUEST TYPE : GET (Authenticated Endpoint)`

Returns the processed CSV file as a JSON file attachment response blob(If the authentication details match correctly: User needs to be a part of the organization to which the uploaded sample belongs)

```
Format:

@[in header] “Authorization: Bearer <access>”
@[out]  CSV is returned as a file attachment in the body(as a file Blob).
Name of the file can be found under the "Content-Disposition" header.
@[out in case of error] JSON form of error is returned along with correct HTTP error code.
Throws 415_UNSUPPORTED_MEDIA HTTP Error if no files of give file_type is
found after extracting the compressed ball.
```

#### **Plagsample Info**

`ENDPOINT : 'api/plagsample/info/<int:id>/' | REQUEST TYPE : GET (Authenticated Endpoint)`

Returns details of a particular plag check
Supplied id must correspond to a valid plagsample and the user must be in the organization to which it belongs.

```
Format:

@[in header] “Authorization: Bearer <access>”
@[in body]
@[JSON response] id, name , filename, file_type, timestamp, org_id, org_name, uploader, uploader_id, file_count
```

#### **Create New Organization**

`ENDPOINT : 'api/organization/makeorg/' | REQUEST TYPE : POST (Authenticated Endpoint)`

Signs up a new organization with the currently logged in user as its first and only member.

```
Format:

@[in header] “Authorization: Bearer <access>”
@[in body] name(required), title(optional description)
@[JSON response] id(organization id), creator(name of creator), title, date_created, unique_code
```

#### **Organization Info**

`ENDPOINT : 'api/organization/get/<int:id>/' | REQUEST TYPE : GET (Authenticated Endpoint)`

Returns details of the inquired organization. Inquiring user must be a member of the organization.

```
Format:

@[in header] “Authorization: Bearer <access>”
@[in body]
@[JSON response] id(org id), name, creator, title, unique_code, date_created,
members : [{“id” : 1, “username” : “ardy”}, {...}, {...}] (sorted according to user_id),
pastchecks : [{filename, id, file_type, timestamp}, ...]
```

#### **Update Organization**

`ENDPOINT : 'api/organization/update/<int:id>/' | REQUEST TYPE : PUT (Authenticated Endpoint)`

A user belonging to the organizaation can update the title.

```
Format:

@[in header] “Authorization: Bearer <access>”
@[in body] title
@[JSON response] id(org id), name, title, creator, date_created
```

#### **Join Organization**

`ENDPOINT : 'api/organization/joinorg/' | REQUEST TYPE : POST (Authenticated Endpoint)`

Given a unique_code adds the user to the org(unless its a personal organization)

```
Format:

@[in header] “Authorization: Bearer <access>”
@[in body] unique_code
@[JSON response] id(org id), creator, name, title, date_created, unique_code,
members : [{“id” : 1, “username” : “ardy”}, {...}, {...}] (sorted according to user_id)
```

---

---

## **Angular Frontend Routes Documentation**

### Routes Implemented (Links given to the detailed documentation)

#### User Account Routes :

1. ['/register'](#register)
2. ['/login'](#login)

#### Dashboard Routes :

3. ['/dashboard'](#dashboard)

#### Profile Routes :

4. ['/profile/changepwd'](#change-password)
5. ['/profile/view'](#view-profile)
6. ['/profile/edit'](#edit-profile)

#### Organization Routes :

7. ['/org/create'](#create-an-organization)
8. ['/org/join'](#join-an-organization)
9. ['/org/view/:id'](#view-organization)
10. ['/org/edit/:id'](#edit-organization)

#### Plagsample Routes :

11. ['/upload'](#upload-sample)
12. ['/report/:id'](#display-report)

### Detailed API Documentation

#### **Token**

#### **Register**

- Create a new user
- Accessible only if the user is not logged in
- Redirects to dashboard if successful

#### **Login**

- Login the user
- Accessible only if the user is not logged in
- Redirects to dashboard if successful

#### **Dashboard**

- Landing page after login
- Displays list of organizations and uploads belonging to each sorted by latest.
- Accessible only if the user is logged in and if the token has not expired

#### **Change Password**

- User can change(update) the password
- Accessible only if the user is logged in and if the token has not expired
- Redirects to dashboard if successful

#### **View Profile**

- Contains the profile details and list of organizations
- Accessible only if the user is logged in and if the token has not expired

#### **Edit Profile**

- User can update the profile
- Accessible only if the user is logged in and if the token has not expired
- Redirects to the profile page if successful.

#### **Create an Organization**

- Create a new organization
- Accessible only if the user is logged in and if the token has not expired
- Redirects to the organization's page if successful.

#### **Join an Organization**

- Join an existing organization
- Accessible only if the user is logged in and if the token has not expired
- Redirects to the organization's page if successful.

#### **View Organization**

- User can update the profile
- Only if the user is logged in and if the token has not expired
- Redirects to the profile page if the edit was successful.

#### **Edit Organization**

- User can update the profile
- Only if the user is logged in and if the token has not expired
- Redirects to the profile page if the edit was successful.

#### **Upload Sample**

- User uploads files here (for now only zip, tar, gz, rar are allowed)
- Only if the user is logged in and if the token has not expired
- Redirects to the display of the result if the upload is successful.

#### **Display Report**

- Users can view the result here.
- Only if the user is logged in and if the token has not expired.
- Throws 403 error if the user is not allowed to view this or it doesn’t exist -> back to dashboard

---

---

## **Bonus plan: Terminal Client**

### Thoughts and references

There are two options to develop a CLI - NodeJS or Python.  
Links referred to:

1. [Build a Terminal Chat Application With Node.js](https://getstream.io/blog/build-a-terminal-chat-application-with-node-js/)
2. [Making a simple Web based SSH client using Node.js and Socket.io](https://hub.packtpub.com/making-simple-web-based-ssh-client-using-nodejs-and-socketio/)
3. [SSH web console](https://medium.com/codingtown/ssh-web-console-21e87b611674)
4. [xterm.js Docs](https://xtermjs.org/)
5. [How to build a CLI with Node.js](https://www.twilio.com/blog/how-to-build-a-cli-with-node-js)
6. [How to write a login script in python via an interactive CLI](https://stackoverflow.com/questions/57194845/how-to-write-a-login-script-in-python-via-an-interactive-cli)
7. [Creating A Real-World CLI App With Node](https://timber.io/blog/creating-a-real-world-cli-app-with-node/)
8. [How To Build A Command-Line Tool With NodeJS - A step-by-step guide](https://dev.to/dendekky/how-to-build-a-command-line-tool-with-nodejs-a-step-by-step-guide-386k)
9. [Build a Password Field for the Terminal using Nodejs](https://blog.bitsrc.io/build-a-password-field-for-the-terminal-using-nodejs-31cd6cfa235)
10. [How do I prompt users for input from a command-line script?](https://nodejs.org/en/knowledge/command-line/how-to-prompt-for-command-line-input/)

---
