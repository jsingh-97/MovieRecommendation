from demographicRecommendation import getMoviesList as getList;
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