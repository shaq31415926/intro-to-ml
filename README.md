# Audio Data Clustering using K-Means


## Content
This repo contains all the code needed to cluster a sample of audio files using K-Means.

Data was downloaded from here: http://marsyas.info/downloads/datasets.html


## Requirements
- Jupyter Notebooks with Python 3.7 +
- To install all the libraries `pip install -r requirements.txt`


## Structure
```
├── data          <- The data with 30 audio files (.wav)
│   
├── notebooks          
│  ├── 01-sh-audio-data-exploring.ipynb
│  ├── 02-sh-k-means-clustering.ipynb
│
├── src           <- Source code for use in this project.
│  ├── create_audio_features_df.py
│  ├── optimal_number_clusters.py
│
├── README.md          
├── requirements.txt   <- The libraries required for reproducing the environment.
│
└──── 
```