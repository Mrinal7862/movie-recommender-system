import streamlit as st
import pickle
import joblib
import pandas as pd
import requests

@st.cache_data
def fetch_poster(movie_id):

    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            return "https://via.placeholder.com/500x750?text=No+Image"

        data = response.json()
        # st.text(data)

        if data['poster_path'] is None:
            return "https://via.placeholder.com/500x750?text=No+Image"

        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

    except:
        return "https://via.placeholder.com/500x750?text=No+Image"

def recommend(movie):
    # Find the index of the movie entered by the user
    movie_index = movies[movies['title'] == movie].index[0]

    # Get similarity scores of this movie with all other movies
    distances = simmilarity[movie_index]

    # enumerate -> attaches movie index with similarity score
    # list() -> converts enumerate object into list for sorting
    # sorted() -> sorts movies based on similarity score
    # reverse=True -> highest similarity first
    # [1:6] -> skip the first movie (itself) and return next top 5 movies
    movies_list = sorted(list(enumerate(distances)), key=lambda x: x[1], reverse=True)[1:6]

    recommend_movies = []
    recommend_movies_posters = []
    # Loop through recommended movies and print their titles
    for i in movies_list:

        recommend_movies.append(movies.iloc[i[0]].title)
        # fetch_poster from API
        movie_id = movies.iloc[i[0]].id

        recommend_movies_posters.append(fetch_poster(movie_id))
    return recommend_movies, recommend_movies_posters

API_KEY = "58c93265b79557c40094ca92af0dc8db"
movies_dict = pickle.load(open('moviesDict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

simmilarity = joblib.load('simillarity.pkl')

st.title("Movie Recommendation System")

selected_Movie_Name = st.selectbox(
    "How would You Like to be Contracted ?",
    movies['title'].values
)

if st.button("Recommend"):
    names, posters = recommend(selected_Movie_Name)

    cols= st.columns(5)

    for i in range(5):
        with cols[i]:
            st.image(posters[i], use_container_width=True)
            st.caption(names[i])


