import flask
import os
from pavlov import PavlovRCON
import asyncio
#from flask_cors import CORS #comment this on deployment

app = flask.Flask(__name__, static_folder='../build', static_url_path='/')
#CORS(app)

def getRconInstance():
    return PavlovRCON(os.getenv("RCON_IP"), os.getenv("RCON_PORT"), os.getenv("RCON_PASS"))

async def getPlayerList():
    pavlov = getRconInstance()
    players = await pavlov.send("RefreshList")
    return players

async def getServerInfo():
    pavlov = getRconInstance()
    return await pavlov.send("ServerInfo")
    
async def getPlayerDetails(playerId):
    pavlov = getRconInstance()
    return await pavlov.send("InspectPlayer " + str(playerId))

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
    "UGC2296654393": "BattleArena",
    "UGC2406042677": "Militia"
}

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route("/api/scoreping")
def ping():
    serverInfo = getServerInfo()
    currentRoundState = serverInfo["ServerInfo"]["RoundState"]
    if int(serverInfo["ServerInfo"]["PlayerCount"].split("/")[0]) != 0:
        if currentRoundState in ["WaitingPostMatch", "LeavingMap"]:
            serverInfo["Scores"] = getPlayerStats(serverInfo)
    return serverInfo

@app.route('/api/server', methods=['GET'])
def server():
    serverInfo = getServerInfo()
    serverInfo["Scores"] = [{'PlayerInfo': {'PlayerName': 'TestMan1', 'UniqueId': '76561198018139374', 'KDA': '3/7/3', 'Score': '6', 'Cash': '20000', 'TeamId': '0'}},{'PlayerInfo': {'PlayerName': 'TestMan2', 'UniqueId': '76561197974494897', 'KDA': '7/3/7', 'Score': '14', 'Cash': '16000', 'TeamId': '1'}}]
    #serverInfo["Scores"] = getPlayerStats(serverInfo)
    return serverInfo


def getServerInfo():
    serverInfo = asyncio.run(getServerInfo())
    serverInfo["ServerInfo"]["MapId"] = serverInfo["ServerInfo"]["MapLabel"]
    try:
        serverInfo["ServerInfo"]["MapLabel"] = maps[serverInfo["ServerInfo"]["MapLabel"]]
    except:
        print("Missing map name " + serverInfo["ServerInfo"]["MapLabel"])
    return serverInfo


def getPlayerStats(serverInfo):
    players = asyncio.run(getPlayerList())
    stats = []
    for player in players['PlayerList']:
        stats.append(asyncio.run(getPlayerDetails(player['UniqueId'])))
    return stats

if __name__ == '__main__':
    app.run(debug=False)


