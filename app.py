import streamlit as st
import pickle as pkl

movies = pkl.load(open("movies.pkl", "rb"))
similarity = pkl.load(open("similarity.pkl", "rb"))

# -------------------------
# Page Config
# -------------------------
st.set_page_config(
    page_title="Movie Recommender System",
    page_icon="🎬",
    layout="wide"
)

# -------------------------
# FIXED CSS (VISIBLE + CLEAN)
# -------------------------
st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(135deg, #ffe4ec, #ffd6e0);
}

/* Title */
.main-title {
    text-align: center;
    font-size: 50px;
    font-weight: 700;
    color: #1f1f1f;
    font-family: 'Segoe UI', sans-serif;
}

/* Subtitle */
.sub-text {
    text-align: center;
    font-size: 20px;
    color: #333;
    margin-bottom: 25px;
}

/* Selectbox container */
div[data-baseweb="select"] > div {
    background-color: white !important;
    color: black !important;
    border-radius: 20px;
    border: 4px solid #ff8fab;
}

/* Dropdown text */
div[data-baseweb="select"] * {
    color: black !important;
}

/* Button */
.stButton>button {
    background-color: #ff5c8a;
    color: white;
    border-radius: 15px;
    height: 3em;
    width: 180px;
    font-size: 20px;
    border: none;
    display: block;
    margin: 20px auto;
}

.stButton>button:hover {
    background-color: #ff2e63;
}

/* Cards */
.movie-card {
    background: linear-gradient(135deg, #ff5c8a, #ff2e63);
    padding: 14px 20px;
    border-radius: 999px; /* pill shape */
    text-align: center;
    font-weight: 600;
    color: white;
    font-size: 15px;
    transition: all 0.3s ease;
    box-shadow: 0 6px 15px rgba(255, 46, 99, 0.3);
    cursor: pointer;
}

/* Hover effect 🔥 */
.movie-card:hover {
    transform: translateY(-5px) scale(1.05);
    box-shadow: 0 12px 25px rgba(255, 46, 99, 0.5);
    background: linear-gradient(135deg, #ff2e63, #ff5c8a);
}
.movie-card {
    animation: fadeInUp 0.6s ease;
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(15px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}
.select-title {
    font-size: 24px;
    font-weight: 700;
    color: #1f1f1f;
    margin-bottom: 8px;
    font-family: 'Segoe UI', sans-serif;
}

</style>
""", unsafe_allow_html=True)

# -------------------------
# Title
# -------------------------
st.markdown('<div class="main-title">🎬 Movie Recommender</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-text">Pick a movie and get similar recommendations</div>', unsafe_allow_html=True)

# -------------------------
# Recommendation Function
# -------------------------
def recommend(movie):
    movie = movie.lower().strip()
    titles = movies['title'].str.lower().str.strip()

    if movie not in titles.values:
        return []

    movie_index = titles[titles == movie].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    return [movies.iloc[i[0]].title for i in movies_list]

# -------------------------
# Selectbox (FIXED VISIBILITY)
# -------------------------
st.markdown('<div class="select-title">Select a movie</div>', unsafe_allow_html=True)
selected_movie = st.selectbox(
    "",
    movies['title'].sort_values().unique(),
    index=None,
    placeholder="CHOOSE YOUR VIBE ",
    label_visibility="collapsed"
)

# -------------------------
# Button + Output
# -------------------------
if st.button("Recommend"):
    if not selected_movie:
        st.warning("Pick something first 👀")
    else:
        recommendations = recommend(selected_movie)

        if recommendations:
            st.markdown('<h3 style="text-align:center; color: black; margin-top:20px;">✨ You might enjoy</h3>', unsafe_allow_html=True)

            cols = st.columns(5)
            for i, movie in enumerate(recommendations):
                with cols[i]:
                    st.markdown(f'<div class="movie-card">{movie}</div>', unsafe_allow_html=True)
        else:
            st.error("That one’s elusive… try another movie 🎬")