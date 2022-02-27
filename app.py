import pandas as pd
import streamlit as st
import pickle
import requests
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__

##beautification
st.set_page_config(page_title='Movie Recommendation System', page_icon='🎥')
#tmdb api key
tmdb_api = '4c4144be60c056038b35c57b23b5d9ac'


def run_func(name, movie_name_by_user, similarity, movies):
    # Use a breakpoint in the code line below to debug your script.

    def fetch_poster(movie_id, api_key):
        response = requests.get(
            'https://api.themoviedb.org/3/movie/{}?api_key={}&language=en-US'.format(movie_id, api_key))

        data = response.json()

        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

    def recommend(movie, df):
        movie_index = df[df['original_title'] == movie].index[0]
        distances = similarity[movie_index]
        # sorting array
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

        recommended_movies = []
        recommended_movies_posters = []
        for movies in movies_list:
            movie_id = df.iloc[movies[0]].id
            recommended_movies.append(df.iloc[movies[0]].original_title)
            # fetching poster from TMBD Api
            recommended_movies_posters.append(fetch_poster(movie_id, tmdb_api))

        return recommended_movies, recommended_movies_posters


    def recommend_return(movie_name_by_user):
        if st.button('Recommend'):
            names, poster = recommend(movie_name_by_user, movies)

            col1, col2, col3 = st.columns(3)
            with col1:
                st.text(names[0])
                st.image(poster[0], width=150)
            with col2:
                st.text(names[1])
                st.image(poster[1], width=150)
            with col3:
                st.text(names[2])
                st.image(poster[2], width=150)
            with col1:
                st.text(names[3])
                st.image(poster[3], width=200)
            with col3:
                st.text(names[4])
                st.image(poster[4], width=200)

    recommend_return(selected_movie_name)

if __name__ == '__main__':
    st.title("Movie Recommendation System")
    #movies
    movie_dict = pickle.load(open('movies.pkl', 'rb'))
    movies = pd.DataFrame(movie_dict)

    #loading similarity matrix
    @st.cache
    def get_similarity_matrix(blob_name):
        connection_string = 'DefaultEndpointsProtocol=https;AccountName=arjunprasadsarkhel;AccountKey=V0FuvezEvjBVwZo7X0o2hq+v9lgNasyKQH/VKOoQRqaoURORgMPWhM9HbQj+7Sx5J7wvkLBOtd5k+ASttj4qkg==;EndpointSuffix=core.windows.net'
        container_name = 'movierecommendation'
        blob_client = BlobClient.from_connection_string(connection_string, container_name, blob_name)
        downloader = blob_client.download_blob(0)

        # Load to pickle
        b = downloader.readall()
        weights = pickle.loads(b)

        return weights

    #get similarity matrix
    similarity = get_similarity_matrix(blob_name='similarity.pkl')

    selected_movie_name = st.selectbox(
        'Please select a movie',
        movies.original_title.values)

    run_func('PyCharm', selected_movie_name, similarity, movies)
