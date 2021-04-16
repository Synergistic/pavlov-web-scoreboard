import mysql.connector, os, sys, traceback

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
        self.cursor = self.connection.cursor(dictionary=True)
        self.cursor.execute(query)
        result = [r for r in self.cursor]
        self.close()
        return result

    def getAllPlayers(self):
        return self.execute("SELECT steamId, name, kills, deaths, points from season0")


    def upsertPlayerRecords(self, players):
        valuesList = []
        for player in players:
            valuesList.append("({}, '{}', {}, {}, {})".format(player["steamId"], player["name"], player["kills"], player["deaths"], player["points"]))
        query = ("INSERT INTO season0 "
                "(steamId, name, kills, deaths, points) "
                "VALUES "
                "{} "
                "ON DUPLICATE KEY UPDATE "
                "kills=VALUES(kills)+kills, "
                "deaths=VALUES(deaths)+deaths, "
                "points=VALUES(points)+points, "
                "name=VALUES(name)").format(",".join(valuesList))
        try:
            self.execute(query)
        except:
            raise Exception("Failed to upsert: {} {} {}".format(player, str(sys.exc_info()), traceback.format_exc()))

    def _connect(self):
        self.connection = mysql.connector.connect(
            user=self.user, password=self.password, host=self.host, port=self.port, database=self.database)

    def _disconnect(self):
        self.connection.commit()
        self.connection.close()
        self.cursor = None
        self.connection = None
