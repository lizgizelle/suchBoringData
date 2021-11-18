import pdb
import time
import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import matplotlib
from summary import run_entire_process
from wordcloud import WordCloud
from PIL import Image
import matplotlib.image as mpimg
matplotlib.use('Agg')
matplotlib.rc('figure', figsize=(12, 4))


def load_pickle(report_name, base_path="./pickles/"):
    try:
        return pd.read_pickle(base_path + report_name)
    except Exception as e:
        print("load_pickle fucked up : ", e)


def get_graph(wc_df, sentiment_df, ticker):

    #Prices line Graph (ticker)
    
    period1 = int(time.mktime(datetime.datetime(2016, 1, 1, 23, 59).timetuple()))
    period2 = int(time.mktime(datetime.datetime(2021, 10, 29, 23, 59).timetuple()))
    interval = '1d' # 1d, 1m

    query_string = f'https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'

    full_schedule_df = pd.read_csv(query_string)

    x="Date"
    y="Open"
    y1="High"
    fig = full_schedule_df.plot(x,y, label = "Open")
    ax = fig
    ax.set_facecolor('black')   

    ax.spines['bottom'].set_color('blue')
    ax.spines['top'].set_color('blue') 
    ax.spines['right'].set_color('blue')
    ax.spines['right'].set_linewidth(3)
    ax.spines['left'].set_color('blue')
    ax.spines['left'].set_lw(3)

    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.tick_params(colors='white', which='both')
    plt.xlabel('Timeline of 10-Qs')
    plt.ylabel('Prices')
    plt.title('Stock Prices for '+ ticker) 
    plt.style.use(['dark_background'])

    # plt.show()

    fig_file3 = BytesIO()
    plt.savefig(fig_file3, format='png')
    fig_file3.seek(0)
    graph_png3 = base64.b64encode(fig_file3.getvalue())


    #Number of Words line graph (wc_df)
    x="key"
    y="Number of words:"
    fig = wc_df.plot(x, color='white')

    ax = fig
    ax.set_facecolor('black')   

    ax.spines['bottom'].set_color('magenta')
    ax.spines['top'].set_color('magenta') 
    ax.spines['right'].set_color('magenta')
    ax.spines['right'].set_linewidth(3)
    ax.spines['left'].set_color('magenta')
    ax.spines['left'].set_lw(3)

    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.tick_params(colors='white', which='both')
    plt.xlabel('Date')
    plt.ylabel("Total Number of Words for each 10-Q Report")
    plt.title('Number of words', color='white') 
    plt.style.use(['dark_background'])
 
    fig_file = BytesIO()
    plt.savefig(fig_file, format='png')
    fig_file.seek(0)
    graph_png = base64.b64encode(fig_file.getvalue())


    #Subjectivity line graph (sentimental_df)
    x="key"
    y="polarity"
    y2='subjectivity'
    sentiment_df.plot(x,y, label = "polarity", color="green")
    fig = sentiment_df.plot(x,y2, label = "open")
    
    ax = fig
    ax.set_facecolor('black')   

    ax.spines['bottom'].set_color('blue')
    ax.spines['top'].set_color('blue') 
    ax.spines['right'].set_color('blue')
    ax.spines['right'].set_linewidth(3)
    ax.spines['left'].set_color('blue')
    ax.spines['left'].set_lw(3)

    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.tick_params(colors='white', which='both')

    plt.xlabel('Date')
    plt.ylabel('Degree from -1 to 1')   
    plt.title('Sentimental Analysis')

    fig_file1 = BytesIO()
    plt.savefig(fig_file1, format='png')
    fig_file1.seek(0)
    graph_png1 = base64.b64encode(fig_file1.getvalue())


    #Polarity line graph (sentimental_df)
    x="key"
    y="polarity"
    fig = sentiment_df.plot(x,y, label = "polarity", color="yellow")
    ax = fig
    ax.set_facecolor('black')   

    ax.spines['bottom'].set_color('red')
    ax.spines['top'].set_color('red') 
    ax.spines['right'].set_color('red')
    ax.spines['right'].set_linewidth(3)
    ax.spines['left'].set_color('red')
    ax.spines['left'].set_lw(3)

    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.tick_params(colors='white', which='both')
    plt.xlabel('Date')
    plt.ylabel('Degree from -1 to 1')   
    plt.title('Polarity Analysis') 

    fig_file2 = BytesIO()
    plt.savefig(fig_file2, format='png')
    fig_file2.seek(0)
    graph_png2 = base64.b64encode(fig_file2.getvalue()) 

    return [graph_png, graph_png1, graph_png2, graph_png3]


# ticker = "AAPL"


def run_entire_process_graphs(ticker):
    # ticker = "AAPL"

    sentiment_df = load_pickle(f"{ticker} - Sentimental and Polarity")
    wc_df = load_pickle(f"{ticker} - Number of Words and Frequency")

    return get_graph(wc_df, sentiment_df, ticker) 
    

    

