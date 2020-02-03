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

from flask import send_file, send_from_directory, safe_join, abort


# credentials
consumer_key = "17vtdwEOtyZhiJvaIsweWPySu"
consumer_secret = "lufEk9iMyrmWj5rR6ka7jW4DhYw6KRNGrUtD1UDcWulwUR8kxh"
access_token = "767679563514208260-lTCPp3wwTRnGqogRyJNG5fr5A1ounvf"
access_token_secret = "hIIQat4QMJ4s5jkqReCqIIiqV89GqaHFdGLuTEOhKNpcv"

# authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify=True)

# search params
max_tweets = 1000
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


# gets valence score for each item in two classes
def get_valence_score(freqs1, freqs2):
    tot_words1 = sum(list(freqs1.values()))
    tot_words2 = sum(list(freqs2.values()))

    # print ("total words:")
    # print (tot_words1, tot_words2)
    new_freqs1 = {}
    new_freqs2 = {}

    for freq in freqs1:
        try:
            if freqs1[freq] < 3:
                continue
            new_freqs1[freq] = 2.0*((1.0*freqs1[freq]/tot_words1)/ ((1.0*freqs1[freq]/tot_words1) + (1.0*freqs2[freq]/tot_words2)))-1.0
            # if (new_freqs1[freq] >= 1):
                # print (new_freqs1[freq])
                # print (freqs1[freq], tot_words1, freqs2[freq], tot_words2)

        except:
            # print (freqs1[freq], tot_words1, freqs2[freq], tot_words2)
            new_freqs1[freq] = 1.0*freqs1[freq]/tot_words1

    for freq in freqs2:
        try:
            if freqs2[freq] < 2:
                continue
            new_freqs2[freq] = 2.0*((1.0*freqs2[freq]/tot_words2)/ ((1.0*freqs2[freq]/tot_words2) + (1.0*freqs1[freq]/tot_words1)))-1.0
        except:
            new_freqs2[freq] = 1.0*freqs2[freq]/tot_words2
    return (Counter(new_freqs1), Counter(new_freqs2))

# filter returns true if word is not a hashtag, not same as query, not RT etc
def filter_word(word, query):
    word = word.lower()
    query = query.lower()
    return (len(word) > 0 and word[0] != '#' and word != query and word != query+":" and word != "rt")

# filter returns true if word is a hashtag, not same as query, etc
def filter_hash(word, query):
    word = word.lower()
    query = query.lower()
    return ((len(word) > 0 and word[0] == '#' and word != query))

# returns words and hashtags that appear more than threshold in text
def get_frequency_words(blue_text, red_text, threshold, query):
    
    word_counts_blue = Counter(blue_text)
    word_counts_blue = Counter({x: word_counts_blue[x] for x in word_counts_blue if (filter_word(x,query))})

    word_counts_red = Counter(red_text)
    word_counts_red = Counter({x: word_counts_red[x] for x in word_counts_red if (filter_word(x,query))})

    # word_counts_blue, word_counts_red = get_valence_score(word_counts_blue, word_counts_red)
    # print ("BLUE WORDS")
    # print (word_counts_blue)
    # print ("##############")
    # print ("RED WORDS")
    # print (word_counts_red)
    # print ("##############")


    word_counts_blue = word_counts_blue.most_common(threshold)
    word_counts_red = word_counts_red.most_common(threshold)

    return (word_counts_blue, word_counts_red)

# returns words and hashtags that appear more than threshold in text
def get_frequency_hashtags(blue_text, red_text, threshold, query):

    hash_counts_blue = Counter(blue_text)
    hash_counts_blue = Counter({x: hash_counts_blue[x] for x in hash_counts_blue if (filter_hash(x,query))})

    hash_counts_red = Counter(red_text)
    hash_counts_red = Counter({x: hash_counts_red[x] for x in hash_counts_red if (filter_hash(x,query))})
    
    # hash_counts_blue, hash_counts_red = get_valence_score (hash_counts_blue, hash_counts_red)

    # print ("BLUE HASH")
    # print (hash_counts_blue)
    # print ("##############")
    # print ("RED HASH")
    # print (hash_counts_red)
    # print ("##############")

    hash_counts_blue = hash_counts_blue.most_common(threshold)
    hash_counts_red = hash_counts_red.most_common(threshold)


    return (hash_counts_blue, hash_counts_red)



# calls twitter with query, classifies each tweet with model and vectorizer. analyzes results.
def processTweets (user_query, model, vectorizer, pos_label, neg_label):

    # searches twitter with query
    searched_tweets = []
    last_id = -1
    while len(searched_tweets) < max_tweets:
        count = max_tweets - len(searched_tweets)
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

    # in case more than max_tweets are retrieved
    searched_tweets = searched_tweets[:max_tweets]

    # screen name + user name
    users = []
    names = []

    # gets tweet text and info about the user
    for i in range (len(searched_tweets)):

        user = searched_tweets[i].user.screen_name
        name = searched_tweets[i].user.name

        users.append(user)
        names.append(name)

        searched_tweets[i] = searched_tweets[i].text

    # no tweets found
    if len (searched_tweets) == 0:
        return jsonify({"tweets":[], "levels": [], "blue":[], "red":[], "blue_names":[], "red_names":[], 
            "word_counts_red":[], "hash_counts_red":[], "word_counts_blue":[], "hash_counts_blue":[]})
    
    # gets word n gram features and performs classification using model chosen
    n_gram_features = vectorizer.transform(searched_tweets)
    predicted_labels = list(model.predict(n_gram_features))

    # users/tweets who post "negative tweets" are red, and users/tweets who post "positive tweets" are blue
    
    # dictionary of user: tweet count for red and blue tweets
    red_users = {}
    blue_users = {}

    # stores user names of users
    reds = {}
    blues = {}

    # accumulates all text, depending on whether red or blue
    red_text = ""
    blue_text = ""

    for i in range (len(predicted_labels)):
        label = predicted_labels[i]
        user = users[i]
        name = names[i]

        if (label == neg_label):
            # stores name of the user
            blues[user] = name
            if user in blue_users:
                blue_users[user] += 1
            else:
                blue_users[user] = 1
            blue_text += (" " + searched_tweets[i])

        elif (label == pos_label):
            #stores name of the red user
            reds[user] = name
            if user in red_users:
                red_users[user] += 1
            else:
                red_users[user] = 1
            red_text += (" " + searched_tweets[i])

    # splits text into words. wordpunct tokenizer could be used instead
    blue_text = blue_text.split(" ")
    red_text = red_text.split(" ")

    # gets top n words for blue/red tweets based on valence score
    word_counts_blue, word_counts_red = get_frequency_words(blue_text, red_text, 20, user_query)
    # print (word_counts_blue, word_counts_red)
    
    # gets top n hashtags for blue/red tweets based on valence score
    hash_counts_blue, hash_counts_red = get_frequency_hashtags(blue_text, red_text, 20, user_query)
    # print (hash_counts_blue, hash_counts_red)

    # gets top n users who post blue and red tweets
    sorted_blue = sorted(blue_users.items(), key=operator.itemgetter(1),reverse=True) [:20]
    sorted_red = sorted(red_users.items(), key=operator.itemgetter(1),reverse=True) [:20]

    # gets usernames of top 20. 
    blue_names = []
    red_names = []

    # gets user names of top 20
    for x in sorted_blue:
        blue_names.append(blues[x[0]])

    for x in sorted_red:
        red_names.append(reds[x[0]])

    return jsonify({"tweets":list(searched_tweets), "levels": predicted_labels, "blue":sorted_blue, "red":sorted_red, "blue_names":blue_names, "red_names":red_names, 
        "word_counts_red":word_counts_red, "hash_counts_red":hash_counts_red, "word_counts_blue":word_counts_blue, "hash_counts_blue":hash_counts_blue})


# loads all models
#####################
#####################
SVM_char_3gram_model, char_3gram_vectorizer = load_model ("./app/static/models/SVM_Final_model_char_3-gram.pckl")
SVM_char_3gram_model_ad, char_3gram_vectorizer_ad = load_model ("./app/static/models/SVM_Add_model_char_3-gram.pckl")
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
    task = request.form["task"]
    print ("task", task)

    if task == "offensive":
        model = SVM_char_3gram_model
        vectorizer = char_3gram_vectorizer
    elif task == "advertisement":
        model = SVM_char_3gram_model_ad
        vectorizer = char_3gram_vectorizer_ad
    elif task == "hate-speech":
        model = SVM_char_3gram_model_hate
        vectorizer = char_3gram_vectorizer_hate
    elif task == "sentiment":
        model = SVM_char_3gram_model_sentiment
        vectorizer = char_3gram_vectorizer_sentiment
    else:
        print ("WHAt", task)
        return jsonify("ERROR")

    ## gets file from request and saves it
    file=request.files['file']
    filename=file.filename.split('.')[0]+'_output.'+file.filename.split('.')[-1]
    path=app.config['UPLOAD_FOLDER']+filename
    file.save(path)

    input_text = []
    ## reads file
    try:
        with open (path, "r") as f:
            for line in f:
                input_text.append(line.strip())

    except:
        print ("ERRRRRROR")
        return jsonify("ERROR")
    
    print (len (input_text))


    n_gram_features = vectorizer.transform(input_text)
    predicted_labels = list(model.predict(n_gram_features))

    with open (path, 'w') as f:
        for i in range (len(input_text)):
            f.write(input_text[i] + "\t" + predicted_labels[i] + "\n")

    # path = "/static/data/" + filename
    # file = open(path, 'rb')
    # path = "static/data/" + filename
    # response = FileResponse(file)

    print (filename)
    # print (app.config['UPLOAD_FOLDER'])
    return send_from_directory ("static/data/", filename=filename, as_attachment=True)



    ## trains classifier


# @app.route('/upload', methods=['POST'])
# def upload():
#     '''saves file in the request and loads it for training'''

#     ## gets file from request and saves it
#     file=request.files['file']
#     filename=file.filename.split('.')[0]+'_new.'+file.filename.split('.')[-1]
#     path=app.config['UPLOAD_FOLDER']+'/'+filename
#     file.save(path)

#     ## reads file
#     try:
#         readfile = pd.read_excel(path, sheet_name = "Sheet1")    
#         train_input = readfile['body'].values
#         train_labels = readfile['languagecomment'].values
#     except:
#         return jsonify("ERROR IN FILE FORMAT")

#     ## trains classifier
#     try:
#         train_all_classifiers(train_input,train_labels)
#     except:
#         return jsonify("CLASSIFIER COULD NOT BE TRAINED")

#     return jsonify("TRAINING COMPLETE")


@app.route('/detectAd', methods=['POST'])
def detectAd():
    ''' detects level of offensiveness in text posted'''

    global char_3gram_vectorizer_ad, SVM_char_3gram_model_ad

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

    return jsonify({"level": prediction})

@app.route('/queryAd', methods=['POST'])
def queryAd():
    ''' detects level of offensiveness in text posted'''

    # preloaded model
    global char_3gram_vectorizer_ad, SVM_char_3gram_model_ad

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

    return processTweets(user_query, model, vectorizer, "__label__ADS", "__label__NOTADS")


@app.route('/detectOffense', methods=['POST'])
def detectOffense():
    ''' detects level of offensiveness in text posted'''
    global char_3gram_vectorizer, SVM_char_3gram_model

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

    return jsonify({"level": prediction})



@app.route('/queryOffense', methods=['POST'])
def queryOffense():
    ''' detects level of offensiveness in text posted'''
    global char_3gram_vectorizer, SVM_char_3gram_model


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

    return processTweets(user_query, model, vectorizer, "OFF", "NOT")


# detect hatespeech
@app.route('/detectHate', methods=['POST'])
def detectHate():
    ''' detects level of hate speech in text posted'''
    global char_3gram_vectorizer_hate, SVM_char_3gram_model_hate

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

    return jsonify({"level": prediction})

@app.route('/queryHate', methods=['POST'])
def queryHate():
    ''' detects level of offensiveness in text posted'''
    global char_3gram_vectorizer_hate, SVM_char_3gram_model_hate

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

    return processTweets(user_query, model, vectorizer, "HS", "NOT_HS")



@app.route('/detectSentiment', methods=['POST'])
def detectSentiment():

    global char_3gram_vectorizer_sentiment, SVM_char_3gram_model_sentiment

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

    return jsonify({"level": prediction})

@app.route('/querySentiment', methods=['POST'])
def querySentiment():
    ''' detects level of sentiment in text posted'''
    global char_3gram_vectorizer_sentiment, SVM_char_3gram_model_sentiment


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

    return processTweets(user_query, model, vectorizer, "Negative", "Positive")
   

