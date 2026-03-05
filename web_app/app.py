import streamlit as st
import pandas as pd
import os
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# Modular Imports
try:
    from modules.styles import apply_custom_css
    from modules.ui_components import render_header
except:
    st.error("Error: modules/ folder is missing or incomplete!")
    st.stop()

# 1. Page Config & Theme State
st.set_page_config(page_title="Movie Matcher Flex", page_icon="🎬", layout="wide")

if 'theme_mode' not in st.session_state:
    st.session_state.theme_mode = 'neon'

themes = {
    'dark': {'bg': '#0E1117', 'txt': '#FFFFFF', 'card': 'rgba(255,255,255,0.05)', 'side': '#262730'},
    'light': {'bg': '#FFFFFF', 'txt': '#1A1A1A', 'card': '#F0F2F6', 'side': '#F0F2F6'},
    'neon': {'bg': '#050505', 'txt': '#00FFFF', 'card': 'rgba(255, 255, 255, 0.08)', 'side': 'rgba(10, 20, 30, 0.95)'}
}
tm = themes[st.session_state.theme_mode]

# 2. Apply Styles & Header
apply_custom_css(tm, st.session_state.theme_mode)
render_header(tm)

# --- SMART DATA ENGINE (For 32M Rows) ---
TMDB_API_KEY = "21079b05b5c30c34238375f5c934888c"

@st.cache_data
def load_large_dataset():
    p = os.path.join(os.path.dirname(__file__), 'movies.csv')
    if os.path.exists(p):
        full_df = pd.read_csv(p)
        full_df['genres'] = full_df['genres'].fillna('')
        sample_df = full_df.head(100000) 
        return full_df, sample_df
    st.error("movies.csv not found!")
    st.stop()

full_movies, rec_movies = load_large_dataset()

# Recommendation Vectorization
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(rec_movies['genres'])

def get_poster(title):
    try:
        clean = title.split(' (')[0]
        url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={clean}"
        data = requests.get(url, timeout=3).json()
        if data.get('results'):
            path = data['results'][0].get('poster_path')
            if path: return f"https://image.tmdb.org/t/p/w500{path}"
    except: pass
    return "https://via.placeholder.com/500x750/050505/00FFFF?text=No+Poster"

def recommend(title):
    try:
        if title not in rec_movies['title'].values:
            return None
        idx = rec_movies.index[rec_movies['title'] == title].tolist()[0]
        sim = linear_kernel(tfidf_matrix[idx], tfidf_matrix).flatten()
        indices = sim.argsort()[-11:-1][::-1]
        return rec_movies.iloc[indices]
    except: return None

# --- SIDEBAR SETTINGS ---
with st.sidebar:
    st.title("⚙️ SETTINGS")
    mode_label = st.selectbox("UI Mode:", ('Neon Power', 'Dark Cinema', 'Polar Light'))
    new_mode = 'neon' if 'Neon' in mode_label else ('dark' if 'Dark' in mode_label else 'light')
    if st.session_state.theme_mode != new_mode:
        st.session_state.theme_mode = new_mode
        st.rerun()
    st.markdown("---")
    
    # Updated Label & Clean Search Box
    query = st.text_input(
        label="Search for a Movie:", 
        value="", 
        placeholder="Type your next movie suggestion..."
    )

# --- MAIN UI LOGIC ---
if query: # Sirf tabhi processing hogi jab user kuch type karega
    choices = full_movies[full_movies['title'].str.contains(query, case=False, na=False)]['title'].unique()

    if len(choices) > 0:
        selected = st.selectbox("Select exact movie:", choices[:100])
        if st.button("🚀 Match My Taste"):
            results = recommend(selected)
            if results is not None:
                st.markdown(f"### Recommendations for: **{selected}**")
                cols = st.columns(5)
                for i, (idx, row) in enumerate(results.iterrows()):
                    rank_css = f"rank-{i+1}" if i < 3 else ""
                    with cols[i % 5]:
                        st.markdown(f'<div class="movie-card {rank_css}">', unsafe_allow_html=True)
                        st.image(get_poster(row['title']), use_container_width=True)
                        st.markdown(f'<div class="movie-title-text">{row["title"]}</div>', unsafe_allow_html=True)
                        yt = f"https://www.youtube.com/results?search_query={row['title'].replace(' ', '+')}+trailer"
                        st.link_button("📺 Trailer", yt, use_container_width=True)
                        st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.warning("This movie is in our 32M database, but too rare for recommendations. Try a popular title!")
    else:
        st.warning("No matches found in 32M records!")
else:
    # Landing message jab search khali ho
    st.info("👈 Please enter a movie name in the sidebar search to get started!")