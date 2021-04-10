import asyncio
from pavlov import PavlovRCON
import os 

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