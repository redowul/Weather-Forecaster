from django.test import TestCase
import censusgeocode as cg
import requests


class Forms(TestCase):
    def test_form_input(self):
        street_address = "1600 Pennsylvania Avenue NW"
        city = "Washington"
        state = "DC"
        zipcode = "20500"

        self.assertNotEqual(street_address, None)
        self.assertNotEqual(city, None)
        self.assertNotEqual(state, None)
        self.assertNotEqual(zipcode, None)


class Census(TestCase):
    def test_census(self):
        address = "1600 Pennsylvania Avenue NW, Washington, DC 20500"
        location = cg.onelineaddress(address)
        longitude, latitude = (
            location[0]["coordinates"]["x"],
            location[0]["coordinates"]["y"],
        )
        self.assertNotEqual(longitude, None)
        self.assertNotEqual(latitude, None)

        address = "Not a real address"
        location = cg.onelineaddress(address)
        self.assertEqual(location, [])


class Weather(TestCase):
    def test_weather(self):
        api_key = "b1b15e88fa797225412429c1c50c122a1"  # Mock (invalid / fake) OpenWeatherMap API key
        longitude, latitude = -77.0369, 38.8977
        url = f"http://api.openweathermap.org/data/2.5/forecast?lat={str(latitude)}&lon={str(longitude)}&appid={api_key}&units=imperial"
        response = requests.request("GET", url)
        self.assertEqual(response.status_code, 401)

        list = [
            {
                "main": {
                    "temp": 48.65,
                    "feels_like": 44.64,
                    "temp_min": 47.97,
                    "temp_max": 48.65,
                    "pressure": 1021,
                    "sea_level": 1021,
                    "grnd_level": 1012,
                    "humidity": 73,
                    "temp_kf": 0.38,
                },
                "dt_txt": "2022-10-04 06:00:00",
            },
            {
                "main": {
                    "temp": 47.93,
                    "feels_like": 43.84,
                    "temp_min": 46.51,
                    "temp_max": 47.93,
                    "pressure": 1021,
                    "sea_level": 1021,
                    "grnd_level": 1011,
                    "humidity": 72,
                    "temp_kf": 0.79,
                },
                "dt_txt": "2022-10-04 09:00:00",
            },
            {
                "main": {
                    "temp": 50.76,
                    "feels_like": 49.86,
                    "temp_min": 50.76,
                    "temp_max": 51.84,
                    "pressure": 1017,
                    "sea_level": 1017,
                    "grnd_level": 1006,
                    "humidity": 92,
                    "temp_kf": 0,
                },
                "dt_txt": "2022-10-05 06:00:00",
            },
        ]

        output = {}
        for snapshot in list:
            date = snapshot.get("dt_txt").split(" ")[0]
            temp_min = snapshot.get("main").get("temp_min")
            temp_max = snapshot.get("main").get("temp_max")
            if date not in output:
                if len(output) < 5:  # 5 day limit
                    output[date] = {}
                    output[date]["temp_min"] = temp_min
                    output[date]["temp_max"] = temp_max
                else:
                    break
            else:
                output[date]["temp_min"] = min(output[date]["temp_min"], temp_min)
                output[date]["temp_max"] = max(output[date]["temp_max"], temp_max)

        self.assertEqual(
            output,
            {
                "2022-10-04": {
                    "temp_min": 46.51,
                    "temp_max": 48.65,
                },
                "2022-10-05": {
                    "temp_min": 50.76,
                    "temp_max": 51.84,
                },
            },
        )
