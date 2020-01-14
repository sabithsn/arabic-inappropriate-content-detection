from app import app

import numpy as np
import dill as pickled
import pandas as pd

from flask import render_template
from flask import jsonify
from flask import request

from sklearn.multiclass import OneVsRestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import MultinomialNB



def get_n_gram_feats (input, n, mode):
    ''' returns word n-gram features and vectorizer 
    for input. mode has to be "char" or "word" '''

    tokenizer = tokenizer=lambda x:x.split(' ')
    vectorizer = TfidfVectorizer(lowercase=False, ngram_range= n, analyzer=mode,tokenizer = tokenizer)
    X_t = vectorizer.fit_transform(input)
    return X_t, vectorizer


def train_classifier (classifier, input, labels):
    ''' trains classifier on input and labels'''

    clf = OneVsRestClassifier(classifier, n_jobs = 1)
    clf.fit(input, labels)
    return clf

def train_all_classifiers (train_input, train_labels):
    ''' trains all classifiers. more classifiers can
        be added here'''

    ## models and vectorizers are made global so that
    ## they are not loaded every time detect is called.
    ## it works for one user. with multiple users,
    ## there will be collisions.

    global word_unigram_vectorizer, word_3gram_vectorizer
    global char_3gram_vectorizer, char_5gram_vectorizer
    global MNB_word_unigram_model, MNB_word_3gram_model
    global SVM_word_unigram_model, SVM_word_3gram_model
    global SVM_char_3gram_model, SVM_char_5gram_model

    ## trains vectorizer for n gram features
    print ("training vectorizers")
    word_unigram_features, word_unigram_vectorizer = get_n_gram_feats(train_input, (1,1), "word")
    word_bigram_features, word_bigram_vectorizer = get_n_gram_feats(train_input, (1,2), "word")

    char_3gram_features, char_3gram_vectorizer = get_n_gram_feats(train_input, (1,3), "char")
    char_5gram_feautres, char_5gram_vectorizer = get_n_gram_feats(train_input, (1,5), "char")
    

    ## trains classifiers. this can be changed to try different classifiers
    print ("training MNB")
    MNB_word_unigram_model = train_classifier(MultinomialNB(), word_unigram_features, train_labels)
    MNB_word_bigram_model = train_classifier(MultinomialNB(), word_bigram_features, train_labels)

    print ("training SVM")
    SVM_word_unigram_model = train_classifier(LinearSVC(), word_unigram_features, train_labels)
    SVM_word_bigram_model = train_classifier(LinearSVC(), word_bigram_features, train_labels)

    SVM_char_3gram_model = train_classifier(LinearSVC(), char_3gram_features, train_labels)
    SVM_char_5gram_model = train_classifier(LinearSVC(), char_5gram_feautres, train_labels)

    print ("training complete")

    ## saves classifier models
    with open("./app/static/models/MNB_model_word_unigram.pckl", "wb") as f:
        pickled.dump(MNB_word_unigram_model, f)
    with open("./app/static/models/MNB_model_word_bigram.pckl", "wb") as f:
        pickled.dump(MNB_word_bigram_model, f)


    with open("./app/static/models/SVM_model_word_unigram.pckl", "wb") as f:
        pickled.dump(SVM_word_unigram_model, f)
    with open("./app/static/models/SVM_model_word_bigram.pckl", "wb") as f:
        pickled.dump(SVM_word_bigram_model, f)


    with open("./app/static/models/SVM_model_char_3gram.pckl", "wb") as f:
        pickled.dump(SVM_char_3gram_model, f)
    with open("./app/static/models/SVM_model_char_5gram.pckl", "wb") as f:
        pickled.dump(SVM_char_5gram_model, f)


    ## saves vectorizers
    with open("./app/static/models/word_unigram_vectorizer.pckl", "wb") as f:
        pickled.dump(word_unigram_vectorizer, f)
    with open("./app/static/models/word_bigram_vectorizer.pckl", "wb") as f:
        pickled.dump(word_bigram_vectorizer, f)


    with open("./app/static/models/char_3gram_vectorizer.pckl", "wb") as f:
        pickled.dump(char_3gram_vectorizer, f)
    with open("./app/static/models/char_5gram_vectorizer.pckl", "wb") as f:
        pickled.dump(char_5gram_vectorizer, f)

    print ("saving complete")

    return




def load_model(model_file):
    ''' loads previously trained model'''
    models = []
    with open(model_file, "rb") as f:
        while True:
            try:
                models.append(pickled.load(f))
            except EOFError:
                break
    return models



# loads all models


## loads classifiers
MNB_word_unigram_model, word_unigram_vectorizer = load_model ("./app/static/models/MNB_Final_model_word_1-gram.pckl")
MNB_word_3gram_model, word_3gram_vectorizer = load_model ("./app/static/models/MNB_Final_model_word_3-gram.pckl")

SVM_word_unigram_model, word_unigram_vectorizer = load_model ("./app/static/models/SVM_Final_model_word_1-gram.pckl")
SVM_word_3gram_model, word_3gram_vectorizer = load_model ("./app/static/models/SVM_Final_model_word_3-gram.pckl")

MNB_char_3gram_model, char_3gram_vectorizer = load_model ("./app/static/models/MNB_Final_model_char_3-gram.pckl")
MNB_char_5gram_model, char_5gram_vectorizer = load_model ("./app/static/models/MNB_Final_model_char_5-gram.pckl")

SVM_char_3gram_model, char_3gram_vectorizer = load_model ("./app/static/models/SVM_Final_model_char_3-gram.pckl")
SVM_char_5gram_model, char_5gram_vectorizer = load_model ("./app/static/models/SVM_Final_model_char_5-gram.pckl")

## loads vectorizers
# word_unigram_vectorizer = load_model("./app/static/models/word_unigram_vectorizer.pckl")
# word_bigram_vectorizer = load_model("./app/static/models/word_bigram_vectorizer.pckl")
# char_3gram_vectorizer = load_model("./app/static/models/char_3gram_vectorizer.pckl")
# char_5gram_vectorizer = load_model("./app/static/models/char_5gram_vectorizer.pckl")

print ("All models loaded")

print ("models not found")

@app.route('/')
@app.route('/index')
def index():
    ''' Home page '''
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    '''saves file in the request and loads it for training'''

    ## gets file from request and saves it
    file=request.files['file']
    filename=file.filename.split('.')[0]+'_new.'+file.filename.split('.')[-1]
    path=app.config['UPLOAD_FOLDER']+'/'+filename
    file.save(path)

    ## reads file
    try:
        readfile = pd.read_excel(path, sheet_name = "Sheet1")    
        train_input = readfile['body'].values
        train_labels = readfile['languagecomment'].values
    except:
        return jsonify("ERROR IN FILE FORMAT")

    ## trains classifier
    try:
        train_all_classifiers(train_input,train_labels)
    except:
        return jsonify("CLASSIFIER COULD NOT BE TRAINED")

    return jsonify("TRAINING COMPLETE")


@app.route('/detect', methods=['POST'])
def detect():
    global word_unigram_vectorizer, word_3gram_vectorizer
    global char_3gram_vectorizer, char_5gram_vectorizer
    global MNB_word_unigram_model, MNB_word_3gram_model
    global SVM_word_unigram_model, SVM_word_3gram_model
    global SVM_char_3gram_model, SVM_char_5gram_model
    ''' detects level of offensiveness in text posted'''

    # Gets text and classifier from client
    user_query = [request.form["text"]]
    classifier = request.form["model"]


    # gets the model chosen by client
    model = None
    vectorizer = None

    if (classifier == "Multinomial Naive Bayes (Word Unigram)"):
        model = MNB_word_unigram_model
        vectorizer = word_unigram_vectorizer
    elif (classifier == "Multinomial Naive Bayes (Word Bigram)"):
        model = MNB_word_3gram_model
        vectorizer = word_3gram_vectorizer
    elif (classifier == "Linear SVM (Word Unigram)"):
        model = SVM_word_unigram_model
        vectorizer = word_unigram_vectorizer
    elif (classifier == "Linear SVM (Word 3-gram)"):
        model = SVM_word_3gram_model
        vectorizer = word_3gram_vectorizer
    elif (classifier == "Linear SVM (Char 3-gram)"):
        model = SVM_char_3gram_model
        vectorizer = char_3gram_vectorizer
    else:
        model = SVM_char_5gram_model
        vectorizer = char_5gram_vectorizer

    # gets word n gram features and performs classification using
    # model chosen
    n_gram_features = vectorizer.transform(user_query)
    predicted_labels = model.predict(n_gram_features)
    prediction = str(predicted_labels[0])
    print (prediction)

    return jsonify({"level": prediction})
