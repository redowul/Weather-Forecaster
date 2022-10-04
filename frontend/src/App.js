import React from "react";
import "./App.css";
import Shortener from "./forecaster/Forecaster";

function App() {
    return (
        <div className="App">
            <div className="App-header">A Weather Forecasting Application.</div>
            <Shortener />
        </div>
    );
}

export default App;
