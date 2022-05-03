import os
import numpy as np
import pandas as pd
from tqdm import tqdm
import deezer

client = deezer.Client()

def main():
    df_deezer = pd.read_csv("./dataset/annotation.csv", index_col=0)
    results, error = [], []
    for _id in tqdm(df_deezer.index):
        try:
            instance = client.get_track(_id)
            results.append({
                "track_id": instance.id,
                "title": instance.title,
                "title_short": instance.title_short,
                "duration": instance.duration,
                "release_date": instance.release_date,
                "preview": instance.preview,
                "bpm": instance.bpm,
                "gain": instance.gain,
                "artist": instance.artist.name,
                "artist_id": instance.artist.id,
                "album": instance.album.title,
                "album_id": instance.album.id,
            })
        except:
            results.append({
                "track_id": _id,
                "title": "",
                "title_short": "",
                "duration": "",
                "release_date": "",
                "preview": "",
                "bpm": "",
                "gain": "",
                "artist": "",
                "artist_id": "",
                "album": "",
                "album_id": "",
            })
            error.append(_id)

    pd.DataFrame(results).set_index("track_id").to_csv("./dataset/metadata.csv")
    print("errors", len(error))
    print(error)

if __name__ == '__main__':
    main()