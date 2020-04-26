import sklearn
import pickle
import praw
import re
from bs4 import BeautifulSoup
import nltk
# nltk.download('all')
from nltk.corpus import stopwords
from django.conf import settings
import os

reddit = praw.Reddit(client_id='k0SKQ3dDcQFCTA', client_secret='spRZ7LM3Ot65lFmNNcGW9lC_5OI', user_agent='flaredetector', username='anirudh-ambati', password='Ambati@1')

def clean_text(text):

    REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;]')
    BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_]')
    STOPWORDS = set(stopwords.words('english'))

    text = BeautifulSoup(text, "lxml").text
    text = text.lower()
    text = REPLACE_BY_SPACE_RE.sub(' ', text)
    text = BAD_SYMBOLS_RE.sub('', text)
    text = ' '.join(word for word in text.split() if word not in STOPWORDS)
    return text

def detect_flair(url):

    BASE_DIR = settings.BASE_DIR
    path = os.path.join(BASE_DIR,'Models/finalized_model.sav')
    loaded_model = pickle.load(open(path,'rb'))

    submission = reddit.submission(url=url)

    data = {}

    data['title'] = submission.title
    data['url'] = submission.url

    submission.comments.replace_more(limit=None)
    comment = ''
    data['combine'] = data['title'] + data['url']

    try:
        for top_level_comment in submission.comments:
            comment = comment + ' ' + top_level_comment.body
            data["comment"] = comment
            data['title'] = clean_text(data['title'])
            data['comment'] = clean_text(data['comment'])
            data['combine'] = data['title'] + data['comment'] + data['url']
    except:
        data['combine'] = data['title'] + data['url']


    return loaded_model.predict([data['combine']])
