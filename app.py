import pickle
import streamlit as st
import requests

API_KEY = "f93f31255b05a68c5a9c6700095e5c93"

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print("TMDB Error:", e)
        return "https://via.placeholder.com/300x450.png?text=Error"

    data = response.json()
    poster_path = data.get("poster_path")

    if not poster_path:
        return "https://via.placeholder.com/300x450.png?text=No+Poster"

    return f"https://image.tmdb.org/t/p/w500{poster_path}"


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    recommended_movie_names = []
    recommended_movie_posters = []

    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters


# -------------------- UI --------------------
st.title("🎬 Movie Recommender System")
st.write("Select a movie & get top 5 recommended movies based on similarity.")

# Load pickle files
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movie_list = movies['title'].values

selected_movie = st.selectbox(
    "Type or select a movie:",
    movie_list
)

if st.button("Show Recommendations"):
    names, posters = recommend(selected_movie)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.subheader(names[0])
        st.image(posters[0])

    with col2:
        st.subheader(names[1])
        st.image(posters[1])

    with col3:
        st.subheader(names[2])
        st.image(posters[2])

    with col4:
        st.subheader(names[3])
        st.image(posters[3])

    with col5:
        st.subheader(names[4])
        st.image(posters[4])
