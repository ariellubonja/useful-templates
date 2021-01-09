# Multithreading to make many requests simultaneously
# https://stackoverflow.com/questions/2846653/how-can-i-use-threading-in-python
# https://stackoverflow.com/questions/41920124/multiprocessing-use-tqdm-to-display-a-progress-bar

'''Read the annotated dataset'''
import pandas as pd

live_data = pd.read_csv('live-data.tsv', sep = "\t", header = 0)
urls = list(live_data.Url)

'''Get the title'''
# import urllib3.request as urllib
from bs4 import BeautifulSoup
import requests


def get_title(url):
    try:
    	# Stream gets the response in chunks. Allows us to not get all of it
        response = requests.get(url, stream=True, timeout = (3.05, 0.3))
        soup = BeautifulSoup(response.content, "html.parser", from_encoding="iso-8859-1")
        return soup.title.string
    except:
        return ""


from multiprocessing.dummy import Pool as ThreadPool
# Progress bar
from tqdm import tqdm

with ThreadPool(100) as p:
    titles = list(tqdm(p.imap(get_title, urls), total=len(urls)))


df = pd.DataFrame(titles)
df.tail()
df.to_csv("titles.csv")

