import React, { useState } from "react";
import getWeatherForecast from "./REST.js";
import "./Forecaster.css";

function Forecaster() {
    const [address, setAddress] = useInput({
        type: "text",
        placeholder: "Street Address (1600 Pennsylvania Avenue NW)"
    });
    const [city, setCity] = useInput({ type: "text", placeholder: "Town or City (Washington)" });
    const [state, setState] = useInput({ type: "text", placeholder: "State (DC)" });
    const [zipcode, setZipcode] = useInput({ type: "text", placeholder: "Zipcode (20500)" });
    const [apiKey, setApiKey] = useInput({
        type: "text",
        placeholder: "Api key (Get one at home.openweathermap.org/api_keys)"
    });
    const [temperatures, setTemperatures] = useState();

    return (
        <div className="Body">
            Enter an address to get a weather forecast
            {setAddress}
            {setCity}
            {setState}
            {setZipcode}
            {setApiKey}
            <div
                className="submit-button"
                onClick={function () {
                    getWeatherForecast(address, city, state, zipcode, apiKey, setTemperatures);
                }}>
                Submit
            </div>
            {temperatures}
        </div>
    );
}

function useInput({ type, placeholder }) {
    const [value, setValue] = useState("");
    const input = (
        <input
            value={value}
            className="text-box"
            placeholder={placeholder}
            onChange={(e) => setValue(e.target.value)}
            type={type}
        />
    );
    return [value, input];
}

export default Forecaster;
