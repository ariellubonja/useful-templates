# Multithreading to make many requests simultaneously
# https://stackoverflow.com/questions/2846653/how-can-i-use-threading-in-python

'''Read the annotated dataset'''
import pandas as pd

live_data = pd.read_csv('./data/live-data.tsv', sep = "\t", header = 0)

'''Get the title'''
import urllib3.request as urllib
from bs4 import BeautifulSoup
import requests

def get_title(url):
    try:
        response = requests.get(url, timeout = (3.05, 10))
        soup = BeautifulSoup(response.content, "html.parser", from_encoding="iso-8859-1")
        title = soup.title.string
        return title
    except:
        return ""

from multiprocessing.dummy import Pool as ThreadPool
pool = ThreadPool(10)

urls = list(live_data.Url)
titles = pool.map(get_title, urls)

live_data['Title'][i] = titles
live_data.to_csv()
