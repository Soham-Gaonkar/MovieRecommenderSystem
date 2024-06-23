import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_title):
    print("movie_title:",movie_title)
    response = requests.get(f'https://www.omdbapi.com/?s={movie_title}&apikey=ba59b9dc')
    data = response.json()
    print(data['Search'])
    Search = data['Search'][0]
    return Search['Poster']
def recommend(movie):

    movie_index = movies[movies['title'] == movie].index[0]
    distances= similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse =True,key = lambda x:x[1])[1:6]
    recommended_movies= []
    recommended_movies_poster =[]

    for i in movies_list:
        movie_id = i[0]
        movie_title = movies.iloc[movie_id].title
        # fetch poster from API
        # API Key :  http://www.omdbapi.com/?i=tt3896198&apikey=ba59b9dc
        recommended_movies.append(movie_title)
        recommended_movies_poster.append(fetch_poster(movie_title))
    return recommended_movies , recommended_movies_poster


similarity = pickle.load(open('C:/Users/Soham/PycharmProjects/Movie-Recommender-System/venv/similarity.pkl','rb'))


movies_dict = pickle.load(open('C:/Users/Soham/PycharmProjects/Movie-Recommender-System/venv/movies_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

st.title('Movie Recommender System')


selected_movie_name = st.selectbox('Choose',
movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    i=0
    for col in st.columns(5):
        with col:
            st.text(names[i])
            st.image(posters[i])
        i+=1


