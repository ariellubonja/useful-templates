# Multithreading to make many requests simultaneously
# https://stackoverflow.com/questions/2846653/how-can-i-use-threading-in-python
# https://stackoverflow.com/questions/41920124/multiprocessing-use-tqdm-to-display-a-progress-bar

'''Read the annotated dataset'''
import pandas as pd

live_data = pd.read_csv('./data/live-data.tsv', sep = "\t", header = 0)
urls = list(live_data.Url)

'''Get the title'''
# import urllib3.request as urllib
# from bs4 import BeautifulSoup
import requests


def get_title(url):
    try:
        response = requests.get(url, timeout = (3.05, 10))
        # soup = BeautifulSoup(response.content, "html.parser", from_encoding="iso-8859-1")
        # title = soup.title.string
        return str(response)
    except:
        return ""


from multiprocessing.dummy import Pool as ThreadPool
# Progress bar
from tqdm import tqdm

with ThreadPool(300) as p:
    titles = list(tqdm(p.imap_unordered(get_title, urls), total=len(urls)))

print("Writing results to CSV...")

import csv

with open('filename', 'w') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerow(titles)

