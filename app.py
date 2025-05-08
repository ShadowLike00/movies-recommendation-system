import streamlit as st
import pickle
import pandas as pd
import requests
import gdown
import os
import time

# --- CONFIG: Google Drive Download ---
SIMILARITY_DRIVE_ID = "YOUR_FILE_ID"  # Replace with your actual file ID
SIMILARITY_LOCAL_PATH = "similarity.pkl"

# --- Download similarity.pkl from Google Drive if not found ---
if not os.path.exists(SIMILARITY_LOCAL_PATH):
    st.info("Downloading similarity matrix...")
    gdown.download(f"https://drive.google.com/uc?id={SIMILARITY_DRIVE_ID}", SIMILARITY_LOCAL_PATH, quiet=False)

# --- Load data ---
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open(SIMILARITY_LOCAL_PATH, 'rb'))

# --- TMDb poster fetching ---
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={st.secrets['TMDB_API_KEY']}"
        response = requests.get(url, timeout=5)
        data = response.json()
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    except Exception as e:
        print(f"Poster fetch failed: {e}")
        return "https://via.placeholder.com/500x750?text=Poster+Unavailable"

# --- Movie Recommender Logic ---
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        time.sleep(0.5)
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_posters

# --- Streamlit UI ---
st.title('🎬 Movie Recommender System')

selected_movie = st.selectbox('Select a movie to get recommendations:', movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie)
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])
