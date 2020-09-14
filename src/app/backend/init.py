from recommendationEngine.index import *;
from routes.v1 import getMoviesList as getTopMovies;
import flask

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/v1/popular', methods=['GET'])
def init():
    response=getTopMovies();
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
    return  response;
app.run()