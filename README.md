# 🎬 Movie Recommender System

This is a content-based movie recommender system built using Streamlit and deployed on Streamlit Cloud. It recommends similar movies based on a selected title using a precomputed similarity matrix and fetches movie posters from the TMDb API.

## 🚀 Features
- Content-based movie recommendations
- Real-time poster fetch using TMDb API
- Streamlit-powered interactive UI
- Google Drive integration for large file hosting

## 🛠 Tech Stack
- Python
- Pandas, Scikit-learn
- Streamlit
- TMDb API
- Google Drive + gdown for large files

## 🧩 Files
- `app.py`: Main application
- `movie_dict.pkl`: Dictionary of movies
- `similarity.pkl`: Precomputed similarity matrix (hosted on Google Drive)
- `requirements.txt`: Python dependencies

## 🔐 Setup

1. Upload `similarity.pkl` to Google Drive
2. Make it shareable and get the file ID from the link
   - Example: `https://drive.google.com/file/d/1AbCDeFgHiJkl/view?usp=sharing`
   - File ID: `1AbCDeFgHiJkl`
3. Paste that into `SIMILARITY_DRIVE_ID` in `app.py`
4. In Streamlit Cloud, go to **App Settings → Secrets** and add:
```toml
TMDB_API_KEY = "your_tmdb_api_key_here"
```

## ✅ Deployment on Streamlit Cloud
1. Push all files to a public GitHub repository
2. Visit [streamlit.io/cloud](https://streamlit.io/cloud)
3. Click “New App” → Select repo → Deploy

Enjoy exploring movies! 🎥🍿
