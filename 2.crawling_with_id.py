import os
import wget
import numpy as np
import pandas as pd
from tqdm import tqdm
import librosa
import multiprocessing
from functools import partial
from contextlib import contextmanager

@contextmanager
def poolcontext(*args, **kwargs):
    pool = multiprocessing.Pool(*args, **kwargs)
    yield pool
    pool.terminate()

def download(url, savename):
    download_path = "./dataset/audio"
    error_path = "./dataset/error"
    os.makedirs(download_path, exist_ok=True)
    os.makedirs(error_path, exist_ok=True)
    wget.download(url, os.path.join(download_path, savename))
    y,sr = librosa.load(os.path.join(download_path, savename), res_type='kaiser_fast')
    if len(y)/sr < 10:
        print(save_name, "is shorter than 10 sec")
        np.save(os.path.join(error_path, save_name.replace(".mp3",".npy")). save_name)
def main():
    df_annotation = pd.read_csv("./dataset/annotation.csv", index_col=0)
    df_preview = df_annotation[~df_annotation['preview'].isna()]
    urls = list(df_preview['preview'])
    save_names = list([str(i)+".mp3" for i in df_preview.index])
    for url, save_name in zip(urls, save_names):
        download(url, save_name)

    # for multi-processing
    # with poolcontext(processes=multiprocessing.cpu_count()-5) as pool:
    #     pool.starmap(download, zip(urls, save_names))

if __name__ == '__main__':
    main()