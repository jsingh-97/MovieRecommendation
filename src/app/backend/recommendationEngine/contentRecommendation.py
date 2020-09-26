from ast import literal_eval
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import numpy as np
#We are going to build a recommender based on the following metadata: the 3 top actors, the director, related genres and the movie plot keywords.
def getSimilarMovies(title):
    df1=pd.read_csv('/home/jaswinder/PycharmProjects/tmdb_5000_credits.csv')
    df2=pd.read_csv('/home/jaswinder/PycharmProjects/tmdb_5000_movies.csv')
    df1.columns = ['id', 'tittle', 'cast', 'crew']
    df2 = df2.merge(df1, on='id')
    features = ['cast', 'crew', 'keywords', 'genres']
    for feature in features:
            df2[feature] = df2[feature].apply(literal_eval)
    df2['director'] = df2['crew'].apply(get_director)

    features = ['cast', 'keywords', 'genres']
    for feature in features:
        df2[feature] = df2[feature].apply(get_list)
    #The next step would be to convert the names and keyword instances into lowercase and strip all the spaces between them. This is done so that our vectorizer doesn't count the Johnny of "Johnny Depp" and "Johnny Galecki" as the same.
    # Apply clean_data function to your features.
    features = ['cast', 'keywords', 'director', 'genres']
    for feature in features:
        df2[feature] = df2[feature].apply(clean_data)
    #We are now in a position to create our "metadata soup", which is a string that contains all the metadata that we want to feed to our vectorizer (namely actors, director and keywords).
    def create_soup(x):
        return ' '.join(x['keywords']) + ' ' + ' '.join(x['cast']) + ' ' + x['director'] + ' ' + ' '.join(x['genres'])

    df2['soup'] = df2.apply(create_soup, axis=1)
    count = CountVectorizer(stop_words='english')
    count_matrix = count.fit_transform(df2['soup'])
    # Compute the Cosine Similarity matrix based on the count_matrix
    cosine_sim2 = cosine_similarity(count_matrix, count_matrix)
    # Reset index of our main DataFrame and construct reverse mapping as before
    df2 = df2.reset_index()
    indices = pd.Series(df2.index, index=df2['title'])
    return get_recommendations(title,cosine_sim2,df2,indices)
# Get the director's name from the crew feature. If director is not listed, return NaN
def get_director(x):
    for i in x:
        if i['job'] == 'Director':
            return i['name']
    return np.nan

# Returns the list top 3 elements or entire list; whichever is more.
def get_list(x):
    if isinstance(x, list):
        names = [i['name'] for i in x]
        #Check if more than 3 elements exist. If yes, return only first three. If no, return entire list.
        if len(names) > 3:
            names = names[:3]
        return names

    #Return empty list in case of missing/malformed data
    return []
# Function to convert all strings to lower case and strip names of spaces
def clean_data(x):
    if isinstance(x, list):
        return [str.lower(i.replace(" ", "")) for i in x]
    else:
        #Check if director exists. If not, return empty string
        if isinstance(x, str):
            return str.lower(x.replace(" ", ""))
        else:
            return ''
# Function that takes in movie title as input and outputs most similar movies
def get_recommendations(title, cosine_sim,df2,indices):
    # Get the index of the movie that matches the title
    idx = indices[title]

    # Get the pairwsie similarity scores of all movies with that movie
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the movies based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the 10 most similar movies
    sim_scores = sim_scores[1:11]

    # Get the movie indices
    movie_indices = [i[0] for i in sim_scores]

    # Return the top 10 most similar movies
    return df2['title'].iloc[movie_indices]