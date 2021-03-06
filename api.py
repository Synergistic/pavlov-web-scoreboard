import flask
import asyncio
import json
import PavlovServerAdmin
import PavlovMapRotationManager

#from flask_cors import CORS #comment this on deployment

app = flask.Flask(__name__, static_folder='./build', static_url_path='/')
#CORS(app)

@app.route('/')
def index():
    return app.send_static_file('index.html')
    
@app.errorhandler(404)
def not_found(e):
    return app.send_static_file('index.html')
    
@app.route("/api/leaderboard/get")
def getleaderboard():
    return flask.jsonify(asyncio.run(PavlovServerAdmin.getLeaderboard()))

@app.route('/api/server', methods=['GET'])
def server():
    serverInfo = asyncio.run(PavlovServerAdmin.getServerInfo())
    maps = PavlovMapRotationManager.PavlovMapThing("CA018752ED6629094BDA16F895479268")
    if("ugc" in serverInfo["MapLabel"].lower()):
        serverInfo["MapLabel"] = maps.get_map(serverInfo["MapLabel"]).title
    return flask.jsonify(serverInfo)

@app.route('/api/map/fromId', methods=['GET'])
def map_fromId():
    maps = PavlovMapRotationManager.PavlovMapThing("CA018752ED6629094BDA16F895479268")
    return flask.jsonify([maps.get_map(i).title for i in flask.request.args["id"].split(",")])

@app.route('/api/map/fromRotation', methods=['GET'])
def map_fromRotation():
    maps = PavlovMapRotationManager.PavlovMapThing("CA018752ED6629094BDA16F895479268")
    return flask.jsonify(maps.rotation_to_data(flask.request.args["rotation"]))

@app.route('/api/map/rotationFromData', methods=['POST'])
def map_rotationFromData():
    maps = PavlovMapRotationManager.PavlovMapThing("CA018752ED6629094BDA16F895479268")
    return flask.jsonify(maps.data_to_rotation(flask.request.json))

if __name__ == '__main__':
    app.run(debug=False)


