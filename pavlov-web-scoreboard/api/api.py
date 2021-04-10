import flask
import rcon
import asyncio
from flask_cors import CORS #comment this on deployment

app = flask.Flask(__name__, static_folder='../build', static_url_path='/')
CORS(app)

maps = {
    "UGC1758245796": "Nuke Town 2025",
    "UGC1675848285": "aim_usp",
    "UGC2367805592": "Bridge Crossing",
    "UGC1710753557": "Snow",
    "UGC1884572674": "MW2 Terminal",
    "UGC2363287266": "Avalanche DoD:S",
    "UGC1984149656": "McDonalds",
    "UGC2152454678": "The Gulag",
    "UGC1675848538": "gg_deagle5",
    "UGC2201914075": "Crackhouse 1.6",
    "UGC2249948962": "BattleWar",
    "UGC1080743206": "Office HQ",
    "UGC2262552543": "WarZone",
    "UGC2365826826": "dod_flash",
    "UGC2321123745": "BattleWar 2",
    "UGC2296654393": "BattleArena"
}

@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/server', methods=['GET'])
def server():
    serverInfo = asyncio.run(rcon.getServerInfo())
    serverInfo["ServerInfo"]["MapId"] = serverInfo["ServerInfo"]["MapLabel"]
    serverInfo["ServerInfo"]["MapLabel"] = maps[serverInfo["ServerInfo"]["MapLabel"]]
    if int(serverInfo["ServerInfo"]["PlayerCount"].split("/")[0]) != 0:
        players = asyncio.run(rcon.getPlayerList())
        serverInfo["Scores"] = []
        for player in players['PlayerList']:
            serverInfo["Scores"].append(asyncio.run(rcon.getPlayerDetails(player['UniqueId'])))
    else:
        serverInfo["Scores"] = [{'PlayerInfo': {'PlayerName': 'Boozus_Newyorkus-TTV', 'UniqueId': '76561198018139374', 'KDA': '3/7/3', 'Score': '6', 'Cash': '20000', 'TeamId': '0'}},
{'PlayerInfo': {'PlayerName': 'Pistoleiro', 'UniqueId': '76561197974494897', 'KDA': '7/3/7', 'Score': '14', 'Cash': '16000', 'TeamId': '1'}}]

    return serverInfo


app.run(host='0.0.0.0', debug=False, port=80)

