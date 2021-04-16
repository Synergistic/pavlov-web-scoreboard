from .rcon import Rcon
from .database import DbContext
import os, asyncio, sys, traceback

async def getLeaderboard():
    return DbContext().getAllPlayers()

async def getServerInfo():
    rconInstance = Rcon(os.getenv("RCON_IP"), os.getenv("RCON_PORT"), os.getenv("RCON_PASS"))
    return await rconInstance.getServerInfo()