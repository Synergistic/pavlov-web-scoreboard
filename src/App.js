import React from 'react';
import './App.css';
import Leaderboard from './components/Leaderboard';
import ServerStatus from './components/ServerStatus';
import Navigation from './components/Navigation';
import AppBar from '@material-ui/core/AppBar';
import Typography from '@material-ui/core/Typography';
import Container from '@material-ui/core/Container';
import Toolbar from '@material-ui/core/Toolbar';
import IconButton from '@material-ui/core/IconButton';
import MenuIcon from '@material-ui/icons/Menu';
import clsx from 'clsx';
import {
  BrowserRouter as Router,
  Switch,
  Route,
} from "react-router-dom";
import MapHelper from './components/MapHelper';

function App(props) {
  const [open, setOpen] = React.useState(false);
  return (
    <Router>
      <div className="App">
        <AppBar
          position="fixed"
          className={clsx("appBar", open && "appBarshift")}
        >
          <Toolbar>
            <IconButton
              color="inherit"
              aria-label="open drawer"
              onClick={() => setOpen(!open)}
              edge="start"
              className={clsx("menuButton mobile")}
            >
              <MenuIcon />
            </IconButton>
            <Typography variant="h6" noWrap>
              VR Together
          </Typography>
          </Toolbar>
        </AppBar>
        <Navigation toggleDrawer={() => setOpen(!open)} open={open} />
        <Toolbar />
        <Switch>
          <Route path="/leaderboard">
            <Container>
              <Leaderboard />
            </Container>
          </Route>
          <Route path="/server">
            <Container>
              <ServerStatus />
            </Container>
          </Route>
          <Route path="/maps">
            <Container>
              <MapHelper />
            </Container>
          </Route>
          <Route path="/">
            <Container>
              <Typography style={{ marginBottom: '36px' }} className="header" variant='h4'>VR-Together</Typography>
              <iframe src="https://discord.com/widget?id=827686879188877334&theme=dark" width="350" height="500" allowtransparency="true" frameborder="0" sandbox="allow-popups allow-popups-to-escape-sandbox allow-same-origin allow-scripts"></iframe>
            </Container>
          </Route>
        </Switch>
      </div>
    </Router>
  );
}

export default App;
