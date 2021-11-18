from os import name
from re import X
from pandas.io import pickle

from werkzeug.datastructures import CombinedMultiDict

from bs4 import BeautifulSoup
import pdb

import time
import datetime
import numpy as np
from matplotlib import pyplot as plt
# from io import BytesIO
# import base64
import matplotlib
# matplotlib.use('Agg')
from wordcloud import WordCloud

import nltk
# nltk.download(["names", "stopwords", "state_union", "twitter_samples", "movie_reviews", "averaged_perceptron_tagger", "vader_lexicon", "punkt"])
# nltk.download(["PorterStemmer"])

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from nltk.stem import WordNetLemmatizer
from nltk.stem import WordNetLemmatizer

from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.sentiment import SentimentIntensityAnalyzer

from textblob import TextBlob
import pandas as pd

def read_raw_text(ticker, file_number):
    query_string = f"./raw/sec-edgar-filings/{ticker}/10-Q/{file_number}/filing-details.html"
    with open(query_string) as fp:
        soup = BeautifulSoup(fp, 'html.parser')

    texts = soup.findAll(text=True)
    words = u" ".join(t.strip() for t in texts)
    print('Number of words: ', len(words))
    return words

def clean(raw):
    lowercase = str.lower(raw) 
    numbs = '''!()-[]{};:'”"’“–|\,<>./-?@#$%^&*_~(,†,|,•,—,1234567890'''
    for ele in lowercase: 
        if ele in numbs:
            lowercase = str(lowercase).replace(ele, " ")
    return lowercase

def tokenize(clean_text):
    text_tokens = word_tokenize(clean_text)
    tokens_without_sw = [word for word in text_tokens if not word in stopwords.words()]
    return tokens_without_sw

# def get_wordCloud(tokens, company_name, company_file):
#     wordcloud = WordCloud(max_font_size=50, max_words=100, background_color="white").generate(str(tokens))
#     plt.figure()
#     plt.imshow(wordcloud, interpolation="bilinear")
#     plt.axis("off")
#     wordcloud.to_file(f"./wordcloud/{company_name}/{company_file}.png")


def get_sentiment(tokens):
    words_sentiment = TextBlob(str(tokens)).sentiment
    return {'polarity': words_sentiment.polarity, 'subjectivity': words_sentiment.subjectivity}

def get_frequency(tokens):
    fd = nltk.FreqDist(tokens) 
    print(fd.most_common(50))

def pickle_and_save(df, report_name, base_path="./pickles/"):
    try:
        df.to_pickle(base_path + report_name)
    except Exception as e:
        print("pickle_and_save fucked up : ", e)

def load_pickle(report_name, base_path="./pickles/"):
    try:
        return pd.read_pickle(base_path + report_name)
    except Exception as e:
        print("load_pickle fucked up : ", e)

def run_entire_process(reports):
    # print(fuckingfuckfuck)
    combined_sentiment_data = []
    combined_number_of_words = []
    for company_name, company_files in reports:
        for file in company_files:
            raw = read_raw_text(company_name, file)
            cleaned = clean(raw)
            tokens = tokenize(cleaned)
            frequency = get_frequency(tokens) #top 50 words
            # wordcloud_image = get_wordCloud(tokens, company_name, file) #word cloud image
            
            sentiment = get_sentiment(tokens)
           
            key = f"{company_name}-{file}"

            number_of_words = {'key': key, 'Number of words:' : len(tokens)}
            combined_number_of_words.append(number_of_words)

            company_report_sentiment = {'key': key, **sentiment}
            combined_sentiment_data.append(company_report_sentiment)

    df1 = pd.DataFrame(combined_number_of_words)
    df2 = pd.DataFrame(combined_sentiment_data)

    df = df1
    pickle_and_save(df, f"{ticker} - Number of Words and Frequency")

    df = df2
    pickle_and_save(df, f"{ticker} - Sentimental and Polarity")

def start(ticker):
    combinedReports = [
        (f"{ticker}", ["2016 - 1Q",  
            "2016 - 2Q",
            "2016 - 3Q",
            "2017 - 1Q",
            "2017 - 2Q",
            "2017 - 3Q",
            "2018 - 1Q",
            "2018 - 2Q",
            "2018 - 3Q",
            "2019 - 1Q",
            "2019 - 2Q",
            "2019 - 3Q",
            "2020 - 1Q",
            "2020 - 2Q",
            "2020 - 3Q",
            "2021 - 1Q",
            "2021 - 2Q"]
        )
    ]

    run_entire_process(combinedReports)    

if __name__ == "__main__":
    
    combinedTickers = [ 
        "ACN", 
        "ADI",
        "AMZN",
        "AAPL",
        "FB",
        "GOOGL",
        "NFLX",
        "PFE",
        "PYPL",
        "SBUX",
        "TSLA",
        "XOM" ]
        
    for ticker in combinedTickers:
        start(ticker)
        print(f"👉{ticker} is done")

    

