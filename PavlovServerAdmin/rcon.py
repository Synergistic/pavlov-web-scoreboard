from pavlov import PavlovRCON
import sys, traceback

class Rcon:
    def __init__(self, ip, port, password):
        self.ip = ip
        self.port = port
        self.password = password
        self.rconInstance = PavlovRCON(self.ip, self.port, self.password)


    async def getServerInfo(self):
        try:
            return (await self.rconInstance.send("ServerInfo"))["ServerInfo"]
        except:
            return None

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



