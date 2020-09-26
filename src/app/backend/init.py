from recommendationEngine.index import *;

from routes.v1 import getMoviesList as getTopMovies;
from routes.v1 import getSimilarMoviesList as getSimilarMovies;
import flask
from flask import Flask, request
app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/v1/popular', methods=['GET'])
def init():
    response=getTopMovies();
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
    return  response;
@app.route('/v1/similar', methods=['GET'])
def similarMovies():
    title=request.args['title']
    response=getSimilarMovies(title);
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
    return  response;


app.run()