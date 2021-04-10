import React, { useState, useEffect } from 'react';
import './App.css';
import "semantic-ui-css/semantic.min.css";
import { Header, Table, Container, Button, Dimmer, Loader } from 'semantic-ui-react'

function App() {
  const [serverInfo, setServerInfo] = useState(undefined);
  const [playerList, setPlayerList] = useState(undefined);
  const [loading, setLoading] = useState(false);


  useEffect(() => {
    fetchServerData();
  }, []);

  const fetchServerData = () => {
    setLoading(true);
    fetch('/api/server').then(res => res.json())
    .then(data => {
      setServerInfo(data["ServerInfo"]);
      setPlayerList(data["Scores"]);
      setLoading(false);
    });
  }

  const renderPlayerRows = () => {
    return playerList.map(p => {
      let player = p["PlayerInfo"];
      let kda = player["KDA"].split("/");
      return (
        <Table.Row>
        <Table.Cell>{player["PlayerName"]}</Table.Cell>
        <Table.Cell>{kda[0]}</Table.Cell>
        <Table.Cell>{kda[1]}</Table.Cell>
        <Table.Cell>{kda[2]}</Table.Cell>
      </Table.Row>
      )
    })
  }
  
  return (
    <div className="App">
      <Container>
      {serverInfo && !loading &&
      <React.Fragment>
        <Header as='h2'>{serverInfo["ServerName"]}</Header>
        <p>Map: {serverInfo["MapLabel"]}</p>
        <p>Mode: {serverInfo["GameMode"]}</p>
        <p>Players: {serverInfo["PlayerCount"]}</p>
        {playerList && 
          <Table celled>
            <Table.Header>
              <Table.Row>
                <Table.HeaderCell>Player</Table.HeaderCell>
                <Table.HeaderCell>Kills</Table.HeaderCell>
                <Table.HeaderCell>Deaths</Table.HeaderCell>
                <Table.HeaderCell>Score</Table.HeaderCell>
              </Table.Row>
            </Table.Header>
            <Table.Body>
              {renderPlayerRows()}
            </Table.Body>
          </Table>}
          <Button primary onClick={() => fetchServerData()}>Refresh</Button>
        </React.Fragment>
        
      }
      {loading && 
        <Dimmer active>
        <Loader inverted>Loading</Loader>
      </Dimmer>
      }
      {/* <iframe src="https://discord.com/widget?id=827686879188877334&theme=dark" width="350" height="500" allowtransparency="true" frameborder="0" sandbox="allow-popups allow-popups-to-escape-sandbox allow-same-origin allow-scripts"></iframe> */}

      </Container>
    </div>
  );
}

export default App;
