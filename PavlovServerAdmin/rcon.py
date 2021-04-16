from pavlov import PavlovRCON
import sys, traceback

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

class Rcon:
    def __init__(self, ip, port, password):
        self.ip = ip
        self.port = port
        self.password = password
        self.rconInstance = PavlovRCON(self.ip, self.port, self.password)


    async def getServerInfo(self):
        return (await self.rconInstance.send("ServerInfo"))["ServerInfo"]

    async def getFriendlyMapName(self, mapId):
        return maps[mapId]
        # serverInfo["ServerInfo"]["MapId"] = serverInfo["ServerInfo"]["MapLabel"]
        # try:
        #     serverInfo["ServerInfo"]["MapLabel"] = maps[serverInfo["ServerInfo"]["MapLabel"]]
        # except:
        #     return serverInfo["ServerInfo"]  # make this lookup on steam

    async def getPlayerList(self):
        pList = await self.rconInstance.send("RefreshList")
        return pList["PlayerList"]
    
    async def getPlayerDetails(self, playerId):
        try :
            stats = (await self.rconInstance.send("InspectPlayer {}".format(playerId)))["PlayerInfo"]
            if not all(stat in stats for stat in ("KDA", "Score", "UniqueId", "PlayerName")):
                return None
            kda = stats["KDA"].split("/")
            return {
                'kills': kda[0],
                'deaths': kda[1],
                'points': stats["Score"],
                'steamId': stats["UniqueId"],
                'name': stats["PlayerName"]
            }
        except:
            raise Exception("Failed to get player details {}. {} {}".format(playerId, str(sys.exc_info()), traceback.format_exc()))

    async def getAllPlayerDetails(self, playerList):
        currentPlayerId = None
        playerDetailsList = []
        for player in playerList:
            try:
                currentPlayerId = player["UniqueId"]
                stats = (await self.rconInstance.send("InspectPlayer {}".format(currentPlayerId)))["PlayerInfo"]
                if not all(stat in stats for stat in ("KDA", "Score", "UniqueId", "PlayerName")):
                    return None
                kda = stats["KDA"].split("/")
                playerDetailsList.append({
                    'kills': kda[0],
                    'deaths': kda[1],
                    'points': stats["Score"],
                    'steamId': stats["UniqueId"],
                    'name': stats["PlayerName"]
                })
            except:
                playerDetailsList.append({ "exception": str(sys.exc_info()), "trace": traceback.format_exc(), "id": currentPlayerId})
        return playerDetailsList

    async def executeCommand(self, command):
        return (await self.rconInstance.send(command))



