import os
import wget
import json
import numpy as np
import pandas as pd
from tqdm import tqdm
import multiprocessing
from functools import partial
from contextlib import contextmanager

import youtube_dl
from selenium import webdriver as wd
from bs4 import BeautifulSoup
import pandas as pd
import requests
from selenium.webdriver.chrome.options import Options


chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("--disable-dev-shm-usage")

def audio_crawl(url, _id):
    save_dir = "./dataset/audio_crawl"
    audio_out_dir = os.path.join(save_dir, _id + ".") # "." need to file formating

    ydl_opts = {
        'format': 'bestaudio/best',
        'extractaudio' : True,      # only keep the audio
        'audioformat' : 'mp3',      # convert to mp3
        'writeinfojson': False,
        'noplaylist': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'postprocessor_args': [
            '-ar', '44100'
        ],
        'outtmpl': audio_out_dir
    }
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.extract_info(url, download = True)
    except:
        np.save(os.path.join(f"./dataset/error/crawl_error/{_id}.npy"), _id)
        
@contextmanager
def poolcontext(*args, **kwargs):
    pool = multiprocessing.Pool(*args, **kwargs)
    yield pool
    pool.terminate()

def query_to_url(query):
    url = "https://www.youtube.com/results?search_query=" + query
    driver = wd.Chrome(executable_path="./dataset/chromedriver",chrome_options=chrome_options)
    driver.get(url)
    html_source = driver.page_source
    driver.quit()
    soup = BeautifulSoup(html_source, 'html.parser')
    datas = soup.select("a#video-title")
    title = datas[0].text.replace('\n', '')
    url = "https://www.youtube.com" + datas[0].get('href')
    return url, title

def make_urls():
    """
    you need chromdriver!
    """
    id_to_url, error = {}, []
    df_meta = pd.read_csv("./dataset/metadata.csv", index_col=0)
    df_no_preview = df_meta[df_meta['preview'].isna()]
    for idx in tqdm(range(len(df_no_preview))):
        item = df_no_preview.iloc[idx]
        query = str(item['title'])  + " " + str(item['artist'])
        try:
            url, title = query_to_url(query)
            id_to_url[str(item.name)] = {
                'url': url,
                'title': title
            }
        except:
            error.append(str(item.name))
    print(len(id_to_url), len(error))

    with open("./dataset/id_to_url.json", mode="w") as io:
        json.dump(id_to_url, io, indent=4)
    np.save(os.path.join("./dataset/error/no_meta_sample.npy"), error)

def crawl_audios(error_crawl=False):
    id_to_url = json.load(open("./dataset/id_to_url.json", 'r'))
    df_meta = pd.read_csv("./dataset/metadata.csv", index_col=0)
    if error_crawl:
        for key in os.listdir("./dataset/audio_crawl"):
            del id_to_url[key.replace(".mp3","")]
    ids, urls = [], []
    for _id, item in id_to_url.items():
        ids.append(str(_id))
        urls.append(item['url'])
    with poolcontext(processes=multiprocessing.cpu_count()-5) as pool:
        pool.starmap(audio_crawl, zip(urls, ids))
    print("finish extract: ", len(os.listdir("./dataset/audio_crawl")))
    
    for key,value in id_to_url.items():
        item = df_meta.loc[int(key)]
        ground_truth = str(item['title']) + " " + str(item['artist'])
        predict = value['title']
        value['query'] = ground_truth
    with open("./dataset/id_to_url.json", mode="w") as io:
        json.dump(id_to_url, io, indent=4)

def main():
    # make_urls()
    crawl_audios(error_crawl=False)
    

if __name__ == '__main__':
    main()