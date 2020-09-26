from demographicRecommendation import getMoviesList as getList;
from contentRecommendation import getSimilarMovies as getSimilarList;
from flask import jsonify
class geeks:
    def __init__(self, name):
        self.name = name

def getMoviesList():
     result=getList();
     list=[]
     for obj in result:
          list.append(geeks(obj[0]))
     res=[movie.name for movie in list];
     return jsonify(res);


def getSimilarMoviesList(title):
    result = getSimilarList(title);
    list = []
    for obj in result:
        list.append(geeks(obj))
    res = [movie.name for movie in list];
    return jsonify(res);