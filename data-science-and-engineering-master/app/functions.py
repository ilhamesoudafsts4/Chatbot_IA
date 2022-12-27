import random
import json
import pickle
import numpy as np

import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from tensorflow.keras.models import load_model
import urllib.request
import codecs
lemmatizer = WordNetLemmatizer()

intents = json.loads(codecs.open('intents.json', 'r', 'utf-8-sig').read())

words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('chatbotmodel.h5')

def clean_up_sentence(sentence):
    sentence_words = set(stopwords.words('french'))
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word)  for word in sentence_words]
   
    return sentence_words

def bag_of_words(sentence):
    sentence_words= clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1

    return np.array(bag)

def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

    results.sort(key=lambda  x:x[1], reverse=True)
    return_list = []
    result="n'hésitez pas de choisir parmi nos offres"
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
        if float(r[1])>0.7:
             tag= return_list[0]['intent']
             print(return_list)
             list_of_intents =intents['intents']
             
             for i in list_of_intents:
              
               if i['tag'] == tag:
                result = random.choice(i['responses'])
               
                return result
                
        else:
            return result   
    return result
