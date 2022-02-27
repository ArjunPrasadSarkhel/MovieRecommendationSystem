# Movie Recommendation System Engine
![MovieImg](image.jpg)

## A content-based recommendation engine, which will recommend the user movies from over 9k+ movies based on similar content

### After doing some pre-processing i used stemming & used tf-idf vectorizer for vectorization and then calculated cossine similarity between all the vector points.
### The cossine similarity matrix (named as - similarity.pkl), is deployed on azure-blob storage, and it's retrieved from there, hence the app takes 5min when it's started for the first time
### Used Streamlit to build the webapp and deploy the code. **(Streamlit code - app.py)**
### I also have used docker container so it will be ready to deploy anywhere on the web.

## Video-Link 
[![Movie Recommendation System](https://img.youtube.com/vi/xWIvtKHPFbo/0.jpg)](https://www.youtube.com/watch?v=xWIvtKHPFbo "Movie Recommendation System")
