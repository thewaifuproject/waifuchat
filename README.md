# Waifu Chat
> AI-based chatbot trained on specific waifus' speech

## Using it
### Set up / Installation
1. [Install Kaldi](http://kaldi-asr.org/doc/install.html)
2. Install ffmpeg and mkvtoolnix (`sudo apt-get install mkvtoolnix ffmpeg`)
3. Install python dependencies (`pip install -r requirements.txt`)
4. Download VoxCeleb1 and VoxCeleb2 datasets and train the voxceleb Kaldi DNN on them (by running `kaldi/egs/voxceleb/v2/run.sh`)  
**- OR -**  
  Download a pretrained network like [2] and install it by replacing the files in `kaldi/egs/voxceleb/v2` with the downloaded ones
5. Prepare the data following the guidelines in the **Data** section

### Data

The system takes unmodified anime episodes as input. It assumes these are in `.mkv` format and that the first audio and susbtitle tracks, as listed by `mkvmerge --identify`, are the ones that should be used to build the model. This is usually the case and the only issue that may arise because of this assumption is that, if a series has it's first subtitle track in japanese and the second one in english, the model is going to use the japanese one, resulting in a chatbot that speaks japanese. If that's the case, the subtitle track being used can be changed by modifying the definition of the variable `subtitleTrack` in `main.py`, setting it to the 0-based index of the subtitle track (so if it's set to `0`, the system is gonna use the first subtitle track listed by `mkvmerge --identify`, if it's set to `2`, it's gonna use the third subtitle track listed by `mkvmerge --identify`, and so on).

These episodes should be in the `series` folder, organized by series, so that all the episodes from a series are in the same folder, thus following this folder structure:
- `series`  
  - `series/Shingeki no Kyojin`  
    - `series/Shingeki no Kyojin/1x01.mkv`  
    - `series/Shingeki no Kyojin/1x02.mkv`  
    - `series/Shingeki no Kyojin/1x03.mkv`  
    - `...`  
    - `series/Shingeki no Kyojin/2x01.mkv`  
    - `series/Shingeki no Kyojin/2x02.mkv`  
    - `...`  
  - `series/Sword Art Online`  
    - `series/Sword Art Online/Episode 1x01.mkv`  
    - `series/Sword Art Online/Episode 1x02.mkv`  
    - `series/Sword Art Online/Episode 1x03.mkv`  
    - `...`  

### Run
```
python3 main.py
```

## How does it work?
1. Extract the audio and subtitle tracks from anime episodes.
2. Using timing information from the subtitles, extract the audio segment associated with each subtitle so that we have a list of (subtitle text, audio segment) tuples for all the subtitles in a series.
3. Extract the xvector associated with each audio segment. This is done by extracting a set of features from the audio segment and then feeding them to a neural network to extract an embedding called xvector. The original research behind this can be found in [1]. We use an implementation of it in Kaldi using a pretrained DNN[2] that was trained on the VoxCeleb datasets[3][4].
4. Use DBSCAN[5] to perform clustering on the xvectors in order to group together the audio segments spoken by the same speaker. Ater this step we should have a list of (subtitle text, speaker) tuples for all subtitles.
5. Select the speaker or set of speakers to mimic by using user-input
6. Train a seq2seq[6] model
7. Serve the chatbot as a discord bot

## Why?
> No waifu no laifu
<p align="right">- Adolf Hitler</p>

## References
[1] Snyder, D. and Garcia-Romero, D. and Sell, G. and Povey, D. and Khudanpur, S. 2018. X-vectors: Robust DNN Embeddings for Speaker Recognition. 2018 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP).  
[2] http://kaldi-asr.org/models/m7 (VoxCeleb Xvector System 1a), retrieved the 19th of December of 2018.  
[3] Nagrani, A. and Chung, J.~S. and Zisserman, A. 2017. VoxCeleb: a large-scale speaker identification dataset. INTERSPEECH.  
[4] J. S. Chung, A. Nagrani, A. Zisserman. 2018. VoxCeleb2: Deep Speaker Recognition. INTERSPEECH.  
[5] DBSCAN  
[6] Ilya Sutskever, Oriol Vinyals and Quoc V. Le. 2014. Sequence to Sequence Learning with Neural Networks.  Conference and Workshop on Neural Information Processing Systems (NIPS).
