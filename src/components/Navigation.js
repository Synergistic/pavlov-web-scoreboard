import React from 'react';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';
import Drawer from '@material-ui/core/Drawer';
import Toolbar from '@material-ui/core/Toolbar';
import {
  withRouter
} from "react-router-dom";

function Navigation(props) {
  const navigate = (page) => {
    props.toggleDrawer()
    props.history.push(page)
  }
  const getLinks = () => (<List>
    <ListItem button onClick={() => navigate("/")}>
      <ListItemText primary={"Home"} />
    </ListItem>
    <ListItem button onClick={() => navigate("/server")}>
      <ListItemText primary={"Server Status"} />
    </ListItem>
    <ListItem button onClick={() => navigate("/leaderboard")}>
      <ListItemText primary={"Leaderboard"} />
    </ListItem>
    <ListItem button onClick={() => navigate("/maps")}>
      <ListItemText primary={"MapRotation Helper"} />
    </ListItem>
  </List>)

  return (
    <React.Fragment>
      <Drawer
        className={"drawer mobile"}
        variant="temporary"
        anchor="left"
        open={props.open}
        classes={{ paper: "drawer" }}
      >
        <Toolbar />
        {getLinks()}
      </Drawer>
      <Drawer
        className={"drawer desktop"}
        variant="persistent"
        anchor="left"
        open={true}
        classes={{ paper: "drawer" }}
      >
        <Toolbar />
        <List>
          {getLinks()}
        </List>
      </Drawer>
    </React.Fragment>

  );
}

export default withRouter(Navigation);
