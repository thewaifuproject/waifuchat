# waifuchat
AI-based chatbot trained on specific waifus' speech

## Using it
### Set up / Installation
1. [Install Kaldi](http://kaldi-asr.org/doc/install.html)
2. Install ffmpeg and mkvtoolnix (`sudo apt-get install mkvtoolnix ffmpeg`)
3. Install python dependencies (`pip install -r requirements.txt`)
4. Download VoxCeleb1 and VoxCeleb2 datasets and train the DNN on them 
**OR**
4. Download a pretrained network like [2] and install it by replacing the files in `kaldi/egs/voxceleb/v2` with the ones downloaded

### Data

The scripts assume that 

### Run
```
python3 main.py
```

## How does it work?
1. Extracts the audio and subtitle tracks from anime episodes.
2. Using timing information from the subtitles, split the audio segment associated with each subtitle so that we have a list of (subtitle text, audio segment) tuples for all subtitles in a serie.
3. Extract the xvector associated with each audio segment. This is done by extracting a set of features from the audio segment and then feeding them to a neural network to extract an embedding called xvector. The original research behind this can be found in [1], we are just using an implementation of it in Kaldi using a pretrained DNN[2] that was training on the VoxCeleb datasets[3][4].
4. Use DBSCAN[5] to perform clustering on the xvectors in order to group together the audio segments spoken by the same speaker. Ater this step we should have a list of (subtitle text, speaker) tuples for all subtitles.
5. Select the speaker or set of speakers to mimic by using user-input
6. Train a seq2seq[6] model
7. Serve the chatbot as a discord bot


## References
[1] Snyder, D. and Garcia-Romero, D. and Sell, G. and Povey, D. and Khudanpur, S. 2018. X-vectors: Robust DNN Embeddings for Speaker Recognition. 2018 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP).
[2] http://kaldi-asr.org/models/m7 (VoxCeleb Xvector System 1a), retrieved the 19th of December of 2018.
[3] Nagrani, A. and Chung, J.~S. and Zisserman, A. 2017. VoxCeleb: a large-scale speaker identification dataset. INTERSPEECH.
[4] J. S. Chung, A. Nagrani, A. Zisserman. 2018. VoxCeleb2: Deep Speaker Recognition. INTERSPEECH.
[5] DBSCAN
[6] Ilya Sutskever, Oriol Vinyals and Quoc V. Le. 2014. Sequence to Sequence Learning with Neural Networks.  Conference and Workshop on Neural Information Processing Systems (NIPS).


