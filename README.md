# Violence Detection in Arabic Text

This app detects level of violence in Arabic Text. It detects whether a given Arabic text is offensive, obscene or does not contain any violence.
This app only works for Arabic text currently.

The app is hosted here: https://violence-detection-lm.herokuapp.com/

## Running the app locally

To run the app locally ensure python 3.6 is installed and run
pip install requirements.txt

Running  python3 violence-detection.py will launch the app locally and can be accessed at localhost:5000


## Models for violence detection

The models for violence detection are located in the directory **app/static/models**
There are six trained models: 
1. Linear SVM with word unigram features
2. Linear SVM with word bigram features
3. Linear SVM with character 3-gram features
4. Linear SVM with character 5-gram features
5. Multinomial Bayes with word unigram features
6. Multinomial Bayes with word bigram features

There are four vectorizers:
1. Word unigram vectorizer
2. Word bigram vectorizer
3. Char 3-gram vectorizer
4. Char 5-gram vectorizer

These models were trained using portion of the AlJazeera data described in http://www.aclweb.org/anthology/W17-3008

