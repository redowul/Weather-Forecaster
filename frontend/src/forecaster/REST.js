import React from "react";
import axios from "axios";

function getWeatherForecast(address, city, state, zipcode, apiKey, setTemperatures) {
    axios
        .post("http://127.0.0.1:8000/forecast", {
            address: address,
            city: city,
            state: state,
            zipcode: zipcode,
            apiKey: apiKey
        })
        .then(function (response) {
            if (response.status === 200) {
                setTemperatures(
                    Object.entries(response.data).map(([key, value]) => (
                        <div key={key}>
                            <b>{key}</b> <br></br>
                            <i>Minimum temperature:</i> <b>{value.temp_min}</b> degrees fahrenheit<br></br>
                            <i>Maximum temperature:</i> <b>{value.temp_max}</b> degrees fahrenheit<br></br>
                        </div>
                    ))
                );
            }
        })
        .catch(function (error) {
            setTemperatures(<div>{error.response.data.error}</div>);
        });
}
export default getWeatherForecast;
