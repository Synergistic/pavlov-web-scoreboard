import React, { useState, useEffect, } from 'react';
import CircularProgress from '@material-ui/core/CircularProgress';
import Typography from '@material-ui/core/Typography';
import Table from 'react-all-in-one-table';

function ServerStatus() {
  const [serverInfo, setServerInfo] = useState(undefined);
  const [playerList, setPlayerList] = useState(undefined);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (serverInfo) {
      return
    }
    setLoading(true);
    fetch('/api/server').then(res => res.json())
      .then(data => {
        setServerInfo(data);
        if (data["Scores"]) {
          setPlayerList(data["Scores"].map(p => {
            let player = p["PlayerInfo"];
            let kda = player["KDA"].split("/");
            return {
              kills: kda[0],
              deaths: kda[1],
              points: player["Score"],
              steamId: player["UniqueId"],
              name: player["PlayerName"],
              team: player["TeamId"]
            }
          }));
        }

      }).finally(() => {
        setLoading(false);
      });
  }, [serverInfo]);

  let isDesktop = window.matchMedia("(min-width: 1281px)").matches;
  const columns = [
    { dataKey: 'name', label: 'Player', width: isDesktop ? 400 : 200 },
    { dataKey: 'kills', label: isDesktop ? 'Kills' : "K", width: isDesktop ? 300 : 100 },
    { dataKey: 'deaths', label: 'Deaths', width: isDesktop ? 300 : 100 },
    { dataKey: 'points', label: 'Points', width: isDesktop ? 300 : 100 },
  ]


  return (
    <div>
      {serverInfo &&
        <div className="header">
          <Typography variant='h6' gutterBottom>{serverInfo["ServerName"]}</Typography>
          <p>Map: {serverInfo["MapLabel"]}</p>
          <p>Mode: {serverInfo["GameMode"]}</p>
          <p>Players: {serverInfo["PlayerCount"]}</p>
        </div>
      }
      {loading &&
        <CircularProgress color='secondary' />
      }
      {!loading && playerList && playerList.length > 0 &&
        <div style={{ height:  (40+(40 * playerList.length)).toString()+"px", maxHeight: '520px'}}>
          <Table
            showSearch={false}
            data={playerList}
            columns={columns}
            defaultOrderBy="kills"
          />
        </div>
      }
    </div>

  );
}
export default ServerStatus;
