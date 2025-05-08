import streamlit as st
import pickle
import pandas as pd
import requests
import os
import gdown
import time

# --------------------- CONFIG ---------------------
SIMILARITY_URL = "https://drive.google.com/file/d/1ERS0_K6jY4kGPBk3gTv702dQ81q4Uj9a/view?usp=sharing"  # Replace with your file ID

# --------------------- API FETCH ---------------------
session = requests.Session()
adapter = requests.adapters.HTTPAdapter(max_retries=3)
session.mount('https://', adapter)

def fetch_poster(movie_id):
    try:
        api_key = st.secrets["TMDB_API_KEY"]
        url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=d1f5d1d413d3243d3e2f123ddde1395f'
        response = session.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    except Exception as e:
        print(f"Error fetching poster for movie ID {movie_id}: {e}")
        return "https://via.placeholder.com/500x750?text=Poster+Unavailable"

# --------------------- RECOMMENDER ---------------------
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        time.sleep(0.5)  # avoid API overload
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

# --------------------- CACHING & FILE HANDLING ---------------------
@st.cache_resource
def load_similarity():
    file_path = "similarity.pkl"
    if not os.path.exists(file_path):
        with st.spinner('Downloading similarity matrix...'):
            gdown.download(SIMILARITY_URL, file_path, quiet=False)
    with open(file_path, 'rb') as f:
        return pickle.load(f)

# --------------------- LOAD PICKLES ---------------------
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = load_similarity()

# --------------------- UI ---------------------
st.title('🎬 Movie Recommender System')

selected_movie_name = st.selectbox(
    'Select a movie to get recommendations:',
    movies['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.text(names[idx])
            st.image(posters[idx])
