from .rcon import Rcon
from .database import DbContext
import os, asyncio, sys, traceback

class Poller:
    def __init__(self, ipAddress, rconPort, rconPass, logger):
        self.__poll_save_stats_run = False
        self.__poll_player_stats_run = False
        self.__server_info_current = None
        self.__players_to_save = {}
        self.__main_loop_in_seconds = 5
        self.__data_scrape_in_seconds = 30
        self.__rconConnection = Rcon(ipAddress, rconPort, rconPass)
        self.logger = logger

    async def getCoroutine(self):
        return await self.poll_server_info()

    async def poll_server_info(self):
        while(True):
            try:
                self.__server_info_current = await self.__rconConnection.getServerInfo()
                playerCount = int(self.__server_info_current["PlayerCount"].split("/")[0])
                roundEnding = self.__server_info_current["RoundState"] == "Ended"
                if roundEnding and (self.__players_to_save or (playerCount > 0)):
                    self.__poll_player_stats_run = False
                    self.logger("SERVER-POLL: Round ended and we have data to capture/store.")
                    self.__poll_save_stats_run = True
                    asyncio.create_task(self.poll_save_stats())
                else:
                    if self.__poll_player_stats_run is False and playerCount > 0:
                        self.logger("SERVER-POLL: I see players, starting stat tracker.")
                        self.__poll_player_stats_run = True
                        asyncio.create_task(self.poll_player_stats())
                    if self.__poll_player_stats_run and playerCount == 0: 
                        self.logger("SERVER-POLL: No active players, stopping stat tracker.")
                        self.__poll_player_stats_run = False
            
                    if self.__poll_save_stats_run and (not self.__players_to_save and (playerCount == 0)): 
                        self.logger("SERVER-POLL: No captured player data and no active players, stopping stat saver.")
                        self.__poll_save_stats_run = False
            except:
                self.logger("{} {}".format(sys.exc_info(),traceback.format_exc()))
            await asyncio.sleep(self.__main_loop_in_seconds)

    async def poll_save_stats(self):
        while(self.__poll_save_stats_run):
            if self.__server_info_current["RoundState"] == "Ended":
                self.logger("SAVE-POLL: Round end detected, pulling most recent data.")
                for player in (await self.__rconConnection.getAllPlayerDetails(await self.__rconConnection.getPlayerList())):
                    if "steamId" in player:
                        self.__players_to_save[player["steamId"]] = player
                self.logger("SAVE-POLL: Sending data to database. {}".format(self.__players_to_save.values()))
                DbContext().upsertPlayerRecords(self.__players_to_save.values())
                self.__players_to_save = {}
                self.__poll_save_stats_run = False
                self.logger("SAVE-POLL: Turning off.")
            await asyncio.sleep(self.__main_loop_in_seconds - 1)

    async def poll_player_stats(self):
        while(self.__poll_player_stats_run):
            self.logger("PLAYER-POLL: Polling.")
            if self.__server_info_current["RoundState"] != "Ended":
                for player in (await self.__rconConnection.getAllPlayerDetails(await self.__rconConnection.getPlayerList())):
                    if "steamId" in player:
                        self.__players_to_save[player["steamId"]] = player
                self.logger("PLAYER-POLL: Round on-going, updating player data. {}".format(self.__players_to_save))
                await asyncio.sleep(self.__data_scrape_in_seconds)