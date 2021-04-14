import mysql.connector
import os
import json
import requests
from pavlov import PavlovRCON

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

class DbContext:
    def __init__(self):
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASS")
        self.host = os.getenv("DB_HOST")
        self.port = os.getenv("DB_PORT")
        self.database = os.getenv("DB_NAME")
        self.connection = None

    def open(self):
        if not self.is_connected():
            self._connect()

    def close(self):
        if self.is_connected():
            self._disconnect()

    def is_connected(self):
        if self.connection is not None:
            return self.connection.is_connected()
        return False

    def execute(self, query):
        if not self.is_connected():
            self._connect()
        self.cursor = self.connection.cursor()
        self.cursor.execute(query)

    def getAllPlayers(self):
        query = ("SELECT steamId, name, kills, deaths, points from season0 ")
        self.execute(query)
        results = []
        for(steamId, name, kills, deaths, points) in self.cursor:
            results.append({'steamId': steamId,'name': name,'kills': kills,'deaths': deaths,'points': points})
        return results

    def findPlayerById(self, steamId):
        query = ("SELECT steamId, name, kills, deaths, points from season0 "
                 "WHERE steamId = {}").format(steamId)
        self.execute(query)
        result = next((r for r in self.cursor if r), False)
        self.close()
        if result is None: return result
        return {
                'steamId': result[0],
                'name': result[1],
                'kills': result[2],
                'deaths': result[3],
                'points': result[4]
            }

    def insertNewPlayerRecord(self, player):
        query = ("INSERT INTO season0 "
                      "(steamId, name, kills, deaths, points) "
                      "VALUES ({}, '{}', {}, {}, {})".format(player["steamId"], player["name"], player["kills"], player["deaths"], player["points"]))
        self.execute(query)
        self.close()
        return

    def updatePlayerRecord(self, player):
        query = ("UPDATE season0 "
                         "SET kills = {}, deaths = {}, points = {} "
                         "WHERE steamId = {}").format(player["kills"], player["deaths"], player["points"], player["steamId"])
        self.execute(query)
        self.close()
        return

    def upsertPlayerRecord(self, player):
        existingRecord = self.findPlayerById(player["steamId"])
        if existingRecord is None: return self.insertNewPlayerRecord(player)
        player = self.mergePlayerRecords(player, existingRecord)
        return self.updatePlayerRecord(player)
    
    def mergePlayerRecords(self, playerDTO, existingRecord):
        playerDTO["kills"] = int(playerDTO["kills"]) + int(existingRecord["kills"])
        playerDTO["deaths"] = int(playerDTO["deaths"]) + int(existingRecord["deaths"])
        playerDTO["points"] = int(playerDTO["points"]) + int(existingRecord["points"]) 
        return playerDTO
            
    def _connect(self):
        self.connection = mysql.connector.connect(
            user=self.user, password=self.password, host=self.host, port=self.port, database=self.database)

    def _disconnect(self):
        self.connection.commit()
        self.connection.close()
        self.cursor = None
        self.connection = None

class Rcon:
    def __init__(self, ip, port, password):
        self.ip = ip
        self.port = port
        self.password = password

    async def getServerInfo(self):
        rconInstance = PavlovRCON(self.ip, self.port, self.password)
        serverInfo = await rconInstance.send("ServerInfo")
        serverInfo["ServerInfo"]["MapId"] = serverInfo["ServerInfo"]["MapLabel"]
        try:
            serverInfo["ServerInfo"]["MapLabel"] = maps[serverInfo["ServerInfo"]["MapLabel"]]
        except:
            print("Missing map name " + serverInfo["ServerInfo"]["MapLabel"])
        if int(serverInfo["ServerInfo"]["PlayerCount"].split("/")[0]) != 0:
            serverInfo["Scores"] = await getPlayerStats(serverInfo)
        return serverInfo

    async def getPlayerStats(self, serverInfo):
        rconInstance = PavlovRCON(self.ip, self.port, self.password)
        players = await rconInstance.send("RefreshList")
        stats = []
        for player in players['PlayerList']:
            stats.append(asyncio.run(rconInstance.send("InspectPlayer " + str(player['UniqueId']))))
        return stats

def parsePlayersIntoDTO(serverInfo):
    try:
        serverInfo["Scores"]
    except KeyError:
        return
    playerDTOs = []
    for playerInfo in serverInfo["Scores"]:
        player = playerInfo["PlayerInfo"]
        kda = player["KDA"].split("/")
        playerDTOs.append({
        'kills': kda[0],
        'deaths': kda[1],
        'points': player["Score"],
        'steamId': player["UniqueId"],
        'name': player["PlayerName"]
        })
    return playerDTOs

async def PingAndUpdate():
    serverInfo = await getServerData() 
    #serverInfo["Scores"] = [{'PlayerInfo': {'PlayerName': 'TestMan1', 'UniqueId': '76561198018139374', 'KDA': '3/7/3', 'Score': '6', 'Cash': '20000', 'TeamId': '0'}},{'PlayerInfo': {'PlayerName': 'TestMan2', 'UniqueId': '76561197974494897', 'KDA': '7/3/7', 'Score': '14', 'Cash': '16000', 'TeamId': '1'}}]
    #serverInfo["ServerInfo"]["RoundState"] = "WaitingPostMatch"
    currentRoundState = serverInfo["ServerInfo"]["RoundState"]
    print("currentRoundState: " + currentRoundState)
    if currentRoundState == "Ended":
        print("hit: " + currentRoundState)
        players = parsePlayersIntoDTO(serverInfo)
        if players is None: return True
        db = DbContext()
        for player in players:
            db.upsertPlayerRecord(player)
    else: return False
    return True

async def getServerData():
    server = Rcon(os.getenv("RCON_IP"), os.getenv("RCON_PORT"), os.getenv("RCON_PASS"))
    return await server.getServerInfo()