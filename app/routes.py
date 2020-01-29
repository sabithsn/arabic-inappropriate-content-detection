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
import operator
from collections import Counter

import tweepy

consumer_key = "17vtdwEOtyZhiJvaIsweWPySu"
consumer_secret = "lufEk9iMyrmWj5rR6ka7jW4DhYw6KRNGrUtD1UDcWulwUR8kxh"
access_token = "767679563514208260-lTCPp3wwTRnGqogRyJNG5fr5A1ounvf"
access_token_secret = "hIIQat4QMJ4s5jkqReCqIIiqV89GqaHFdGLuTEOhKNpcv"


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify=True)


max_tweets = 1000
# query = "@QF OR @ajarabic"
result_type = "recent"



def get_n_gram_feats (input, n, mode):
    ''' returns word n-gram features and vectorizer 
    for input. mode has to be "char" or "word" '''

    tokenizer = tokenizer=lambda x:x.split(' ')
    vectorizer = TfidfVectorizer(lowercase=False, ngram_range= n, analyzer=mode,tokenizer = tokenizer)
    X_t = vectorizer.fit_transform(input)
    return X_t, vectorizer




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

# returns words and hashtags that appear more than threshold in text
def get_frequency(text, threshold):
    text = text.split(" ")
    # all words frequency
    word_counts = Counter(text)
    word_counts = Counter({x: word_counts[x] for x in word_counts if len(x) > 0})


    # only hashtags frequency
    hashtags = {x: word_counts[x] for x in word_counts if x[0]=='#'}
    hash_counts = Counter(hashtags) 

    word_counts = word_counts.most_common(threshold)
    list_counts = hash_counts.most_common(threshold)

    return (word_counts,list_counts)

# loads all models


## loads classifiers
# MNB_word_unigram_model, word_unigram_vectorizer = load_model ("./app/static/models/MNB_Final_model_word_1-gram.pckl")
# MNB_word_3gram_model, word_3gram_vectorizer = load_model ("./app/static/models/MNB_Final_model_word_3-gram.pckl")

# SVM_word_unigram_model, word_unigram_vectorizer = load_model ("./app/static/models/SVM_Final_model_word_1-gram.pckl")
# SVM_word_3gram_model, word_3gram_vectorizer = load_model ("./app/static/models/SVM_Final_model_word_3-gram.pckl")

# MNB_char_3gram_model, char_3gram_vectorizer = load_model ("./app/static/models/MNB_Final_model_char_3-gram.pckl")
# MNB_char_5gram_model, char_5gram_vectorizer = load_model ("./app/static/models/MNB_Final_model_char_5-gram.pckl")

SVM_char_3gram_model, char_3gram_vectorizer = load_model ("./app/static/models/SVM_Final_model_char_3-gram.pckl")
# SVM_char_5gram_model, char_5gram_vectorizer = load_model ("./app/static/models/SVM_Final_model_char_5-gram.pckl")


#####################
#####################

MNB_word_unigram_model_ad, word_unigram_vectorizer_ad = load_model ("./app/static/models/MNB_Add_model_word_1-gram.pckl")
# MNB_word_3gram_model_ad, word_3gram_vectorizer_ad = load_model ("./app/static/models/MNB_Add_model_word_3-gram.pckl")

SVM_word_unigram_model_ad, word_unigram_vectorizer_ad = load_model ("./app/static/models/SVM_Add_model_word_1-gram.pckl")
# SVM_word_3gram_model_ad, word_3gram_vectorizer_ad = load_model ("./app/static/models/SVM_Add_model_word_3-gram.pckl")

# MNB_char_3gram_model_ad, char_3gram_vectorizer_ad = load_model ("./app/static/models/MNB_Add_model_char_3-gram.pckl")
# MNB_char_5gram_model_ad, char_5gram_vectorizer_ad = load_model ("./app/static/models/MNB_Add_model_char_5-gram.pckl")

SVM_char_3gram_model_ad, char_3gram_vectorizer_ad = load_model ("./app/static/models/SVM_Add_model_char_3-gram.pckl")
# SVM_char_5gram_model_ad, char_5gram_vectorizer_ad = load_model ("./app/static/models/SVM_Add_model_char_5-gram.pckl")

SVM_char_3gram_model_hate, char_3gram_vectorizer_hate = load_model ("./app/static/models/SVM_Hate_model_char_5-gram.pckl")

SVM_char_3gram_model_sentiment, char_3gram_vectorizer_sentiment = load_model ("./app/static/models/SVM_Sent_model_char_3-gram.pckl")


print ("All models loaded")


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

@app.route('/detectAd', methods=['POST'])
def detectAd():
    global word_unigram_vectorizer_ad, word_3gram_vectorizer_ad
    global char_3gram_vectorizer_ad, char_5gram_vectorizer_ad
    global MNB_word_unigram_model_ad, MNB_word_3gram_model_ad
    global SVM_word_unigram_model_ad, SVM_word_3gram_model_ad
    global SVM_char_3gram_model_ad, SVM_char_5gram_model_ad
    ''' detects level of offensiveness in text posted'''

    # Gets text and classifier from client
    user_query = [request.form["text"]]
    classifier = request.form["model"]


    # gets the model chosen by client
    model = None
    vectorizer = None

    if (classifier == "Multinomial Naive Bayes (Word Unigram)"):
        model = MNB_word_unigram_model_ad
        vectorizer = word_unigram_vectorizer_ad
    elif (classifier == "Multinomial Naive Bayes (Word Bigram)"):
        model = MNB_word_3gram_model_ad
        vectorizer = word_3gram_vectorizer_ad
    elif (classifier == "Linear SVM (Word Unigram)"):
        model = SVM_word_unigram_model_ad
        vectorizer = word_unigram_vectorizer_ad
    elif (classifier == "Linear SVM (Word 3-gram)"):
        model = SVM_word_3gram_model_ad
        vectorizer = word_3gram_vectorizer_ad
    elif (classifier == "Linear SVM (Char 3-gram)"):
        model = SVM_char_3gram_model_ad
        vectorizer = char_3gram_vectorizer_ad
    else:
        model = SVM_char_3gram_model_ad
        vectorizer = char_3gram_vectorizer_ad

    # gets word n gram features and performs classification using
    # model chosen
    n_gram_features = vectorizer.transform(user_query)
    predicted_labels = model.predict(n_gram_features)
    prediction = str(predicted_labels[0])
    print (prediction)

    return jsonify({"level": prediction})

@app.route('/queryAd', methods=['POST'])
def queryAd():
    global word_unigram_vectorizer_ad, word_3gram_vectorizer_ad
    global char_3gram_vectorizer_ad, char_5gram_vectorizer_ad
    global MNB_word_unigram_model_ad, MNB_word_3gram_model_ad
    global SVM_word_unigram_model_ad, SVM_word_3gram_model_ad
    global SVM_char_3gram_model_ad, SVM_char_5gram_model_ad
    ''' detects level of offensiveness in text posted'''

    # Gets text and classifier from client
    user_query = request.form["text"]
    classifier = request.form["model"]


    # gets the model chosen by client
    model = None
    vectorizer = None

    if (classifier == "Multinomial Naive Bayes (Word Unigram)"):
        model = MNB_word_unigram_model_ad
        vectorizer = word_unigram_vectorizer_ad
    elif (classifier == "Multinomial Naive Bayes (Word Bigram)"):
        model = MNB_word_3gram_model_ad
        vectorizer = word_3gram_vectorizer_ad
    elif (classifier == "Linear SVM (Word Unigram)"):
        model = SVM_word_unigram_model_ad
        vectorizer = word_unigram_vectorizer_ad
    elif (classifier == "Linear SVM (Word 3-gram)"):
        model = SVM_word_3gram_model_ad
        vectorizer = word_3gram_vectorizer_ad
    elif (classifier == "Linear SVM (Char 3-gram)"):
        model = SVM_char_3gram_model_ad
        vectorizer = char_3gram_vectorizer_ad
    else:
        model = SVM_char_3gram_model_ad
        vectorizer = char_3gram_vectorizer_ad

    ## searches twitter for query
    searched_tweets = []
    last_id = -1
    while len(searched_tweets) < max_tweets:
        # print ("pookey")
        count = max_tweets - len(searched_tweets)
        # count = 5
        try:
            new_tweets = api.search(q=user_query, count=count, max_id=str(last_id - 1), result_type = result_type, lang = "ar")
            if not new_tweets:
                break
            searched_tweets.extend(new_tweets)
            last_id = new_tweets[-1].id
        except tweepy.TweepError as e:
            print (e)
            # depending on TweepError.code, one may want to retry or wait
            # to keep things simple, we will give up on an error
            break

    users = []
    names = []
    alltext = ""
    searched_tweets = searched_tweets[:max_tweets]

    # gets tweet text and info about the user
    for i in range (len(searched_tweets)):

        user = searched_tweets[i].user.screen_name
        name = searched_tweets[i].user.name

        users.append(user)
        names.append(name)

        searched_tweets[i] = searched_tweets[i].text




    if len (searched_tweets) == 0:
        return jsonify({"tweets":[], "levels": [], "blue":[], "red":[], "blue_names":[], "red_names":[], "word_counts":[], "hash_counts":[]})
    # gets word n gram features and performs classification using
    # model chosen
    n_gram_features = vectorizer.transform(searched_tweets)
    predicted_labels = list(model.predict(n_gram_features))

    red_users = {}
    blue_users = {}

    reds = {}
    blues = {}

    for i in range (len(predicted_labels)):
        label = predicted_labels[i]
        user = users[i]
        name = names[i]

        if (label == "__label__NOTADS"):
            # stores name of the user
            blues[user] = name
            if user in blue_users:
                blue_users[user] += 1
            else:
                blue_users[user] = 1
        else:
            #stores name of the red user
            reds[user] = name
            if user in red_users:
                red_users[user] += 1
            else:
                red_users[user] = 1
            alltext += (" " + searched_tweets[i])

    word_counts, hash_counts = get_frequency(alltext, 20)
    sorted_blue = sorted(blue_users.items(), key=operator.itemgetter(1),reverse=True) [:20]
    sorted_red = sorted(red_users.items(), key=operator.itemgetter(1),reverse=True) [:20]

    blue_names = []
    red_names = []
    # gets user names of top 20
    for x in sorted_blue:
        blue_names.append(blues[x[0]])

    for x in sorted_red:
        red_names.append(reds[x[0]])

    # prediction = str(predicted_labels[0])
    # print (prediction)

    return jsonify({"tweets":list(searched_tweets), "levels": predicted_labels, "blue":sorted_blue, "red":sorted_red, "blue_names":blue_names, "red_names":red_names, "word_counts":word_counts, "hash_counts":hash_counts})

@app.route('/detectOffense', methods=['POST'])
def detectOffense():
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
        model = SVM_char_3gram_model
        vectorizer = char_3gram_vectorizer

    # gets word n gram features and performs classification using
    # model chosen
    n_gram_features = vectorizer.transform(user_query)
    predicted_labels = model.predict(n_gram_features)
    prediction = str(predicted_labels[0])
    print (prediction)

    return jsonify({"level": prediction})



@app.route('/queryOffense', methods=['POST'])
def queryOffense():
    global word_unigram_vectorizer, word_3gram_vectorizer
    global char_3gram_vectorizer, char_5gram_vectorizer
    global MNB_word_unigram_model, MNB_word_3gram_model
    global SVM_word_unigram_model, SVM_word_3gram_model
    global SVM_char_3gram_model, SVM_char_5gram_model
    ''' detects level of offensiveness in text posted'''

    # Gets text and classifier from client
    user_query = request.form["text"]
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
        model = SVM_char_3gram_model
        vectorizer = char_3gram_vectorizer

    searched_tweets = []
    last_id = -1
    while len(searched_tweets) < max_tweets:
        # print ("pookey")
        count = max_tweets - len(searched_tweets)
        # count = 5
        try:
            new_tweets = api.search(q=user_query, count=count, max_id=str(last_id - 1), result_type = result_type, lang = "ar")
            if not new_tweets:
                break
            searched_tweets.extend(new_tweets)
            last_id = new_tweets[-1].id
        except tweepy.TweepError as e:
            # depending on TweepError.code, one may want to retry or wait
            # to keep things simple, we will give up on an error
            break


    users = []
    names = []
    alltext = ""
    searched_tweets = searched_tweets[:max_tweets]

    # gets tweet text and info about the user
    for i in range (len(searched_tweets)):

        user = searched_tweets[i].user.screen_name
        name = searched_tweets[i].user.name

        users.append(user)
        names.append(name)

        searched_tweets[i] = searched_tweets[i].text




    if len (searched_tweets) == 0:
        return jsonify({"tweets":[], "levels": [], "blue":[], "red":[], "blue_names":[], "red_names":[], "word_counts":[], "hash_counts":[]})
    # gets word n gram features and performs classification using
    # model chosen
    n_gram_features = vectorizer.transform(searched_tweets)
    predicted_labels = list(model.predict(n_gram_features))

    red_users = {}
    blue_users = {}

    reds = {}
    blues = {}

    for i in range (len(predicted_labels)):
        label = predicted_labels[i]
        user = users[i]
        name = names[i]

        if (label == "NOT"):
            # stores name of the user
            blues[user] = name
            if user in blue_users:
                blue_users[user] += 1
            else:
                blue_users[user] = 1
        else:
            #stores name of the red user
            reds[user] = name
            if user in red_users:
                red_users[user] += 1
            else:
                red_users[user] = 1
            alltext += (" " + searched_tweets[i])

    word_counts, hash_counts = get_frequency(alltext, 20)
    sorted_blue = sorted(blue_users.items(), key=operator.itemgetter(1),reverse=True) [:20]
    sorted_red = sorted(red_users.items(), key=operator.itemgetter(1),reverse=True) [:20]

    blue_names = []
    red_names = []
    # gets user names of top 20
    for x in sorted_blue:
        blue_names.append(blues[x[0]])

    for x in sorted_red:
        red_names.append(reds[x[0]])

    # prediction = str(predicted_labels[0])
    # print (prediction)

    return jsonify({"tweets":list(searched_tweets), "levels": predicted_labels, "blue":sorted_blue, "red":sorted_red, "blue_names":blue_names, "red_names":red_names, "word_counts":word_counts, "hash_counts":hash_counts})


# detect hatespeech
@app.route('/detectHate', methods=['POST'])
def detectHate():
    global char_3gram_vectorizer_hate

    global SVM_char_3gram_model_hate
    ''' detects level of offensiveness in text posted'''

    # Gets text and classifier from client
    user_query = [request.form["text"]]
    classifier = request.form["model"]


    # gets the model chosen by client
    model = None
    vectorizer = None

    if (classifier == "Multinomial Naive Bayes (Word Unigram)"):
        model = MNB_word_unigram_model_hate
        vectorizer = word_unigram_vectorizer_hate
    elif (classifier == "Multinomial Naive Bayes (Word Bigram)"):
        model = MNB_word_3gram_model_hate
        vectorizer = word_3gram_vectorizer_hate
    elif (classifier == "Linear SVM (Word Unigram)"):
        model = SVM_word_unigram_model_hate
        vectorizer = word_unigram_vectorizer_hate
    elif (classifier == "Linear SVM (Word 3-gram)"):
        model = SVM_word_3gram_model_hate
        vectorizer = word_3gram_vectorizer_hate
    elif (classifier == "Linear SVM (Char 3-gram)"):
        model = SVM_char_3gram_model_hate
        vectorizer = char_3gram_vectorizer_hate
    else:
        model = SVM_char_3gram_model_hate
        vectorizer = char_3gram_vectorizer_hate

    # gets word n gram features and performs classification using
    # model chosen
    n_gram_features = vectorizer.transform(user_query)
    predicted_labels = model.predict(n_gram_features)
    prediction = str(predicted_labels[0])
    print (prediction)

    return jsonify({"level": prediction})

@app.route('/queryHate', methods=['POST'])
def queryHate():
    global char_5gram_vectorizer_hate
    global SVM_char_5gram_model_hate
    ''' detects level of offensiveness in text posted'''

    # Gets text and classifier from client
    user_query = request.form["text"]
    classifier = request.form["model"]


    # gets the model chosen by client
    model = None
    vectorizer = None

    if (classifier == "Multinomial Naive Bayes (Word Unigram)"):
        model = MNB_word_unigram_model_hate
        vectorizer = word_unigram_vectorizer_hate
    elif (classifier == "Multinomial Naive Bayes (Word Bigram)"):
        model = MNB_word_3gram_model_hate
        vectorizer = word_3gram_vectorizer_hate
    elif (classifier == "Linear SVM (Word Unigram)"):
        model = SVM_word_unigram_model_hate
        vectorizer = word_unigram_vectorizer_hate
    elif (classifier == "Linear SVM (Word 3-gram)"):
        model = SVM_word_3gram_model_hate
        vectorizer = word_3gram_vectorizer_hate
    elif (classifier == "Linear SVM (Char 3-gram)"):
        model = SVM_char_3gram_model_hate
        vectorizer = char_3gram_vectorizer_hate
    else:
        model = SVM_char_3gram_model_hate
        vectorizer = char_3gram_vectorizer_hate

    ## searches twitter for query
    searched_tweets = []
    last_id = -1
    while len(searched_tweets) < max_tweets:
        # print ("pookey")
        count = max_tweets - len(searched_tweets)
        # count = 5
        try:
            new_tweets = api.search(q=user_query, count=count, max_id=str(last_id - 1), result_type = result_type, lang = "ar")
            if not new_tweets:
                break
            searched_tweets.extend(new_tweets)
            last_id = new_tweets[-1].id
        except tweepy.TweepError as e:
            print (e)
            # depending on TweepError.code, one may want to retry or wait
            # to keep things simple, we will give up on an error
            break


    users = []
    names = []
    alltext = ""
    searched_tweets = searched_tweets[:max_tweets]

    # gets tweet text and info about the user
    for i in range (len(searched_tweets)):

        user = searched_tweets[i].user.screen_name
        name = searched_tweets[i].user.name

        users.append(user)
        names.append(name)

        searched_tweets[i] = searched_tweets[i].text


    if len (searched_tweets) == 0:
        return jsonify({"tweets":[], "levels": [], "blue":[], "red":[], "blue_names":[], "red_names":[], "word_counts":[], "hash_counts":[]})
    # gets word n gram features and performs classification using
    # model chosen
    n_gram_features = vectorizer.transform(searched_tweets)
    predicted_labels = list(model.predict(n_gram_features))

    red_users = {}
    blue_users = {}

    reds = {}
    blues = {}

    for i in range (len(predicted_labels)):
        label = predicted_labels[i]
        user = users[i]
        name = names[i]

        if (label == "NOT_HS"):
            # stores name of the user
            blues[user] = name
            if user in blue_users:
                blue_users[user] += 1
            else:
                blue_users[user] = 1
        else:
            #stores name of the red user
            reds[user] = name
            if user in red_users:
                red_users[user] += 1
            else:
                red_users[user] = 1
            alltext += (" " + searched_tweets[i])
    word_counts, hash_counts = get_frequency(alltext, 20)


    sorted_blue = sorted(blue_users.items(), key=operator.itemgetter(1),reverse=True) [:20]
    sorted_red = sorted(red_users.items(), key=operator.itemgetter(1),reverse=True) [:20]

    blue_names = []
    red_names = []
    # gets user names of top 20
    for x in sorted_blue:
        blue_names.append(blues[x[0]])

    for x in sorted_red:
        red_names.append(reds[x[0]])

    # prediction = str(predicted_labels[0])
    # print (prediction)

    return jsonify({"tweets":list(searched_tweets), "levels": predicted_labels, "blue":sorted_blue, "red":sorted_red, "blue_names":blue_names, "red_names":red_names, "word_counts":word_counts, "hash_counts":hash_counts})


@app.route('/detectSentiment', methods=['POST'])
def detectSentiment():
    # global word_unigram_vectorizer_ad, word_3gram_vectorizer_ad
    global char_3gram_vectorizer_ad, char_5gram_vectorizer_ad
    # global MNB_word_unigram_model_ad, MNB_word_3gram_model_ad
    # global SVM_word_unigram_model_ad, SVM_word_3gram_model_ad
    global SVM_char_3gram_model_ad, SVM_char_5gram_model_ad
    ''' detects level of offensiveness in text posted'''

    # Gets text and classifier from client
    user_query = [request.form["text"]]
    classifier = request.form["model"]


    # gets the model chosen by client
    model = None
    vectorizer = None

    if (classifier == "Multinomial Naive Bayes (Word Unigram)"):
        model = MNB_word_unigram_model_sentiment
        vectorizer = word_unigram_vectorizer_sentiment
    elif (classifier == "Multinomial Naive Bayes (Word Bigram)"):
        model = MNB_word_3gram_model_sentiment
        vectorizer = word_3gram_vectorizer_sentiment
    elif (classifier == "Linear SVM (Word Unigram)"):
        model = SVM_word_unigram_model_sentiment
        vectorizer = word_unigram_vectorizer_sentiment
    elif (classifier == "Linear SVM (Word 3-gram)"):
        model = SVM_word_3gram_model_sentiment
        vectorizer = word_3gram_vectorizer_sentiment
    elif (classifier == "Linear SVM (Char 3-gram)"):
        model = SVM_char_3gram_model_sentiment
        vectorizer = char_3gram_vectorizer_sentiment
    else:
        model = SVM_char_3gram_model_sentiment
        vectorizer = char_3gram_vectorizer_sentiment

    # gets word n gram features and performs classification using
    # model chosen
    n_gram_features = vectorizer.transform(user_query)
    predicted_labels = model.predict(n_gram_features)
    prediction = str(predicted_labels[0])
    print (prediction)

    return jsonify({"level": prediction})

@app.route('/querySentiment', methods=['POST'])
def querySentiment():
    global word_unigram_vectorizer_sentiment, word_3gram_vectorizer_sentiment
    global char_3gram_vectorizer_sentiment, char_5gram_vectorizer_sentiment
    # global MNB_word_unigram_model_ad, MNB_word_3gram_model_ad
    # global SVM_word_unigram_model_ad, SVM_word_3gram_model_ad
    global SVM_char_3gram_model_sentiment, SVM_char_5gram_model_sentiment
    ''' detects level of offensiveness in text posted'''

    # Gets text and classifier from client
    user_query = request.form["text"]
    classifier = request.form["model"]


    # gets the model chosen by client
    model = None
    vectorizer = None

    if (classifier == "Multinomial Naive Bayes (Word Unigram)"):
        model = MNB_word_unigram_model_sentiment
        vectorizer = word_unigram_vectorizer_sentiment
    elif (classifier == "Multinomial Naive Bayes (Word Bigram)"):
        model = MNB_word_3gram_model_sentiment
        vectorizer = word_3gram_vectorizer_sentiment
    elif (classifier == "Linear SVM (Word Unigram)"):
        model = SVM_word_unigram_model_sentiment
        vectorizer = word_unigram_vectorizer_sentiment
    elif (classifier == "Linear SVM (Word 3-gram)"):
        model = SVM_word_3gram_model_sentiment
        vectorizer = word_3gram_vectorizer_sentiment
    elif (classifier == "Linear SVM (Char 3-gram)"):
        model = SVM_char_3gram_model_sentiment
        vectorizer = char_3gram_vectorizer_sentiment
    else:
        model = SVM_char_3gram_model_sentiment
        vectorizer = char_3gram_vectorizer_sentiment

    ## searches twitter for query
    searched_tweets = []
    last_id = -1
    while len(searched_tweets) < max_tweets:
        # print ("pookey")
        count = max_tweets - len(searched_tweets)
        # count = 5
        try:
            new_tweets = api.search(q=user_query, count=count, max_id=str(last_id - 1), result_type = result_type, lang = "ar")
            if not new_tweets:
                break
            searched_tweets.extend(new_tweets)
            last_id = new_tweets[-1].id
        except tweepy.TweepError as e:
            print (e)
            # depending on TweepError.code, one may want to retry or wait
            # to keep things simple, we will give up on an error
            break

    users = []
    names = []
    alltext = ""
    searched_tweets = searched_tweets[:max_tweets]

    # gets tweet text and info about the user
    for i in range (len(searched_tweets)):

        user = searched_tweets[i].user.screen_name
        name = searched_tweets[i].user.name

        users.append(user)
        names.append(name)

        searched_tweets[i] = searched_tweets[i].text




    if len (searched_tweets) == 0:
        return jsonify({"tweets":[], "levels": [], "blue":[], "red":[], "blue_names":[], "red_names":[], "word_counts":[], "hash_counts":[]})
    # gets word n gram features and performs classification using
    # model chosen
    n_gram_features = vectorizer.transform(searched_tweets)
    predicted_labels = list(model.predict(n_gram_features))

    red_users = {}
    blue_users = {}

    reds = {}
    blues = {}

    for i in range (len(predicted_labels)):
        label = predicted_labels[i]
        user = users[i]
        name = names[i]

        if (label == "Positive"):
            # stores name of the user
            blues[user] = name
            if user in blue_users:
                blue_users[user] += 1
            else:
                blue_users[user] = 1
        elif (label == "Negative"):

            #stores name of the red user
            reds[user] = name
            if user in red_users:
                red_users[user] += 1
            else:
                red_users[user] = 1
            alltext += (" " + searched_tweets[i])

    word_counts, hash_counts = get_frequency(alltext, 20)
    sorted_blue = sorted(blue_users.items(), key=operator.itemgetter(1),reverse=True) [:20]
    sorted_red = sorted(red_users.items(), key=operator.itemgetter(1),reverse=True) [:20]

    blue_names = []
    red_names = []
    # gets user names of top 20
    for x in sorted_blue:
        blue_names.append(blues[x[0]])

    for x in sorted_red:
        red_names.append(reds[x[0]])

    # prediction = str(predicted_labels[0])
    # print (prediction)

    return jsonify({"tweets":list(searched_tweets), "levels": predicted_labels, "blue":sorted_blue, "red":sorted_red, "blue_names":blue_names, "red_names":red_names, "word_counts":word_counts, "hash_counts":hash_counts})

