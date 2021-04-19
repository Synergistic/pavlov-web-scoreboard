from .steamy import SteamAPI

class PavlovMapThing:
    def __init__(self, steamApiKey):
        self.steam = SteamAPI(steamApiKey)

    def get_map(self, mapId):
        return self.steam.get_workshop_file(mapId.lower().replace("ugc", ""))

    def id_to_name(self, mapId):
        return self.get_map(mapId).title

    def rotation_to_data(self, mapRotationString):
         return [{
             "name": self.id_to_name(d[0]),
             "id": d[0],
             "gameMode": d[1]
         } for d in [d.strip().split(",") for d in self.__stripRotationStrip(mapRotationString) if d]]

    def data_to_rotation(self, mapDataSet):
        return ['MapRotation=(MapId="{}", GameMode="{}")'.format(m["id"], m["gameMode"]) for m in mapDataSet]
    
    def __stripRotationStrip(self, mapRotationString):
        return mapRotationString.replace('"',"'").replace("MapRotation=(MapId='", "").replace("', GameMode='",",").replace("')","|").split("|")