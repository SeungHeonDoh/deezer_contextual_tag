# Rebulid Deezer Contextual Dataset

Modules and scripts for downloading Deezer's Contextual Tag dataset, a dataset of ~50K million annotated audios.

Unfortunately, 12.6K data cannot be downloaded on deezer API. That's 25% of the total dataset. 

This repository recovers the lost data as much as possible through the youtube source.

### Reference
- Track-Tag Binary Matrix: https://zenodo.org/record/3648287
- DataSplit: 
- Paper Reference: [Audio-Based Auto-Tagging With Contextual Tags for Music, ICASSP, 2020](https://hal.archives-ouvertes.fr/hal-02481374/document)

### Process

`python 1.build_meta.py` The first step is to build the metadata using the Deezer API. 
We utilize the csv file `Context_tags_dataset.csv` used in this [link](https://zenodo.org/record/3648287). I rename to `annotation.csv`. 
That metadata has preview audio. This is the audio used in the ISMIR reference.

```python
    100%|████████████████████████████████| 49929/49929 [6:58:36<00:00,  1.99it/s]
    errors 15
    [71098866, 101559476, 71098865, 458162472, 505006432, 4544005, 
    493685342, 140438203, 468950282, 474565662, 140438211, 483500142, 
    119641258, 118747976, 71098864]
```

`python 2.crawling_with_id` The second stage is crawling using preview audio of metadata. We use python wget to build the data.

The audio format is as follows.

```python
    {'channels': 2,
    'sample_rate': 44100.0,
    'bitdepth': None,
    'bitrate': 128000.0,
    'duration': 30.719002,
    'num_samples': 1354708,
    'encoding': 'MPEG audio (layer I, II or III)',
    'silent': False}
 ```

`python 3.crawling_from_youtube.py` The third step is to restore the lost preview track.

We use the track name and artist name in the metadata to find the yotubue link, and crawl the music based on this. (I haven't checked all of them for 12.6K. If there are any errors, please leave an issue.) This function performs two tasks. Data for the first task is at this [json file](https://github.com/SeungHeonDoh/deezer_contextual_tag/blob/master/dataset/id_to_url.json).

1. track & artist name -> url
2. url -> audio

The audio format is as follows.

```python
    100%|█████████████████████████████████████████| 12659/12659 [26:33:43<00:00]
    save_to_error_ratio : 12650 / 9

    {'channels': 2,
    'sample_rate': 44100.0,
    'bitdepth': None,
    'bitrate': 192000.0,
    'duration': 207.327007,
    'num_samples': 9143121,
    'encoding': 'MPEG audio (layer I, II or III)',
    'silent': False}
 ```