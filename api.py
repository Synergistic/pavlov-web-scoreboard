import flask
import asyncio
from pavlovServer import DbContext, PingAndUpdate, getServerData
#from flask_cors import CORS #comment this on deployment

app = flask.Flask(__name__, static_folder='./build', static_url_path='/')
#CORS(app)

@app.route('/')
def index():
    return app.send_static_file('index.html')
    
@app.errorhandler(404)
def not_found(e):
    return app.send_static_file('index.html')

@app.route("/api/leaderboard/update")
def ping():
    return flask.jsonify(asyncio.run(PingAndUpdate()))
    
@app.route("/api/leaderboard/get")
def getleaderboard():
    return flask.jsonify(DbContext().getAllPlayers())

@app.route('/api/server', methods=['GET'])
def server():
    return asyncio.run(getServerData())

if __name__ == '__main__':
    app.run(debug=True)


