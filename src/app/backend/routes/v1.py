from recommendationEngine.index import getMoviesList as getPopularMovies;
from recommendationEngine.index import  getSimilarMoviesList as getSimilarMovies;
def getMoviesList():
    return getPopularMovies();
def getSimilarMoviesList(title):
    return getSimilarMovies(title);
