import React, { Component } from "react";
import { Route, Switch } from "react-router-dom";

import AppStateProvider from "./providers/AppStateProvider";

import Home from "./pages/Home";
import NotFound from "./pages/NotFound";
import Loading from "./pages/Loading";
import Editor from "./pages/Editor";

import "./App.css";

const electron = window.require('electron');
const { ipcRenderer } = electron;

class App extends Component {
  componentDidMount() {
		ipcRenderer.on('background open alert', (event, args) => {
			console.log(args);
		});
		ipcRenderer.send('start background', {
		});
	}

  render() {
    return (
      <>
        <AppStateProvider>
          <Switch>
            <Route path="/" exact={true} component={Home} />
            <Route path="/loading" component={Loading} />
            <Route path="/notfound" component={NotFound} />
            <Route path="/editor" component={Editor} />
          </Switch>
        </AppStateProvider>
      </>
    );
  };
};

export default App;
