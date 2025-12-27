## music-recommendation-model

Dataset comes from Kaggle repository [link](https://www.kaggle.com/datasets/joebeachcapital/30000-spotify-songs/data). Almost 30,000 Songs from the Spotify API. See the readme file for a formatted data dictionary table.

I will not be using Spotify Tracks Dataset [link](https://www.kaggle.com/datasets/gauthamvijayaraj/spotify-tracks-dataset-updated-every-week) for this problem anymore as 30000-spotify-songs is enough for the problem.

## Jupyter Notebook

Use the [jupyternotebook\1_exploratory_data_analysis_spotify_data.ipynb](https://github.com/khushboochandra07/music_recommendation_model/blob/main/jupyternotebook/1_exploratory_data_analysis_spotify_data.ipynb) to look at the results and findings

### **Business Understanding**  

*   Data is from Spotify for 30000 tracks.
*   The data is based of spotify tracks, artists, genre, playlist, release date and tracks popularity and metadata like acousticness, danceability,energy, loudness, valence.   
*   The goal is to build a music recommendation model.


### **Data Understanding**  

The spotify data has data about tracks, artists, genre, popularity, release date and tracks metadata information.

*   Size of original data is 32833 rows and 23 columns
*   Out of 32833, 5 rows are missing track_name, track_artist, album name
*   Release date column seems to be not intuitive by itself, so converted it to release year.
*   Categorical columns - 'genre','subgenre','year'
*   Numerical columns - 'track_popularity', 'danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms'


### **Data Preparation**  

*   Dropped the rows with null 'track_name', 'track_artist', 'track_album_name'.
*   Renamed playlist_genre and playlist_subgenre to genre and subgenre respectively. 
*   Converted track_album_release_date to year.
*   Added spotify_url column for the app

Visualization

**Track count by genre, subgenre and year**
![alt text](/images/track_count.png)

**Average Popularity by Playlist Genre**

![alt text](/images/avg_pop.png)

**Average Popularity of tracks by year**

![alt text](/images/avg_year.png)

**Distribution of Danceability and Energy**

![alt text](/images/dance.png)

**Top 10 unique tracks**

![alt text](/images/top_track.png)

**Top 10 unique artist**

![alt text](/images/top_artist.png)


### **Modeling** 

For the music recommendation problem, we are using the Clustering (K-means) to group songs into clusters based on songs metadata like loudeness, danceability, acousticness, energy. Fot this first step is to fifure out the value for k and then group the songs into clusters by applying the KMeans algorithm.

Step 1 - Used elbow method to figure out the value of k to be 4.

![alt text](/images/elbow.png)

Step 2 - applied KMean to group the songs in clusters

![alt text](/images/kmean.png)

Compared the centers of Kmean and PCA to make sure that we have the right dimensionality of the data

![alt text](/images/kmeancluster.png)

![alt text](/images/pcacenters.png)

### **Evaluation**
After running KMean and PCA it is determined that KMean is appropriate for the music recommendation model and thus should be productionlized.

### **Deployment** 

To see the UI version of the app follow the below steps:
1. Clone or download the repository to your local system.
2. Open Command Prompt (CMD) or your preferred terminal
3. Ensure you have Python installed (python --version)
4. execute this command in command prompt - "pip install streamlit"
5. Navigate to the folder containing [pythoncode\app.py](https://github.com/khushboochandra07/music_recommendation_model/blob/main/pythoncode/app.py) using cd foldername on yopur local system.
6. execute this command in command prompt - streamlit run app.py

Note: for Macbook use [link](https://docs.streamlit.io/get-started/installation/command-line) to install streamlit.

![alt text](/images/landing.png)

![alt text](/images/recommendation1.png)

![alt text](/images/song.png)

![alt text](/images/recommendation.png)




# Copyright (c) Khushboo Chandra.
