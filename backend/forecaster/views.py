from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.http import HttpResponse
import json
import requests
import censusgeocode as cg
from .errors import generate_error


@csrf_exempt
@api_view(["POST"])
def get_forecast(request):
    if request.method == "POST":
        data = json.loads(request.body)
        street_address = str(data.get("address")) if data else None
        city = str(data.get("city")) if data else None
        state = str(data.get("state")) if data else None
        zipcode = str(data.get("zipcode")) if data else None
        api_key = str(data.get("apiKey")) if data else None

        if (
            len(street_address) > 0
            and len(city) > 0
            and len(state) > 0
            and len(zipcode) > 0
        ):
            address = f"{street_address}, {city}, {state} {zipcode}"
            location = cg.onelineaddress(address)
            if location:
                longitude, latitude = (
                    location[0]["coordinates"]["x"],
                    location[0]["coordinates"]["y"],
                )
            else:
                # Sometimes the user's address input could be valid, but record of the address might not exist in the census database yet. (Newly developed properties could cause this, for example.)
                # In that case, we'll attempt to grab the general weather data of the town or city the address is (presumably) located in instead.
                url = f"https://api.openweathermap.org/data/2.5/weather?q={city},{state},{zipcode}&appid={api_key}"
                response = requests.request("GET", url)
                if response.status_code == 200:
                    longitude, latitude = (
                        response.json()["coord"]["lon"],
                        response.json()["coord"]["lat"],
                    )
                else:
                    match (response.status_code):
                        case 401:
                            return generate_error({"error": "Invalid API key."}, 401)
                        case 404:
                            return generate_error({"error": "Invalid address."}, 404)
                        case _:
                            return generate_error(
                                {"error": "An unknown error occurred."}, 500
                            )
            url = f"http://api.openweathermap.org/data/2.5/forecast?lat={str(latitude)}&lon={str(longitude)}&appid={api_key}&units=imperial"
            response = requests.request("GET", url)
            if response.status_code == 200:
                response_data = response.json().get("list")
                output = {}
                for snapshot in response_data:
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
                        output[date]["temp_min"] = min(
                            output[date]["temp_min"], temp_min
                        )
                        output[date]["temp_max"] = max(
                            output[date]["temp_max"], temp_max
                        )
                return HttpResponse(json.dumps(output), content_type="application/json")
            else:
                return generate_error({"error": "Invalid API key."}, 400)
        else:
            return generate_error({"error": "Invalid address."}, 400)
