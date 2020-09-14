# Before getting started with this -
#
# we need a metric to score or rate movie
# Calculate the score for every movie
# Sort the scores and recommend the best rated movie to the users.
# We can use the average ratings of the movie as the score but using this won't be fair enough since a movie with 8.9 average rating and only 3 votes cannot be considered better than the movie with 7.8 as as average rating but 40 votes. So, I'll be using IMDB's weighted rating (wr) which is given as :-
#
# where,
#
# v is the number of votes for the movie;
# m is the minimum votes required to be listed in the chart;
# R is the average rating of the movie; And
# C is the mean vote across the whole report
import pandas as pd
import numpy as np
from flask import request, jsonify
import json
def getMoviesList():
    #This can be downloaded from here and save in your Project root folder
    #https://www.kaggle.com/tmdb/tmdb-movie-metadata?select=tmdb_5000_credits.csv
    df1=pd.read_csv('/home/jaswinder/PycharmProjects/tmdb_5000_credits.csv')
    #https://www.kaggle.com/tmdb/tmdb-movie-metadata?select=tmdb_5000_movies.csv
    df2=pd.read_csv('/home/jaswinder/PycharmProjects/tmdb_5000_movies.csv')
    df1.columns = ['id','tittle','cast','crew']
    # merging df2 and df1 dataset into df2 at movie id (id is primary key in both these tables )
    df2= df2.merge(df1,on='id')
    # C is the mean of all the vote_averages in the dataset
    C= df2['vote_average'].mean()
    #  m is the minimum votes required to be listed in the chart we will use 90 percentile i.e it should have more votes than 90% movies on the list
    m= df2['vote_count'].quantile(0.9)
    q_movies = df2.copy().loc[df2['vote_count'] >= m]
    def weighted_rating(x, m=m, C=C):
        v = x['vote_count']
        R = x['vote_average']
        # Calculation based on the IMDB formula
        return (v/(v+m) * R) + (m/(m+v) * C)
    # Define a new feature 'score' and calculate its value with `weighted_rating()`
    q_movies['score'] = q_movies.apply(weighted_rating, axis=1)
    #Sort movies based on score calculated above
    q_movies = q_movies.sort_values('score', ascending=False)
    #Print the top 15 movies
    result=q_movies[['title', 'vote_count', 'vote_average', 'score','homepage']].head(20)

    return result.values.tolist();