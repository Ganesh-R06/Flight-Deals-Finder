import os
import requests

SERPAPI_ENDPOINT = "https://serpapi.com/search?engine=google_flights"


class FlightSearch:
    def __init__(self):
        self.myapikey = os.environ["SERPAPI_API_KEY"]

    def check_flights(
        self,
        starting_point,
        destination_city_code,
        from_time,
        to_time,
        is_direct=True
    ):
        query = {
            "engine": "google_flights",
            "departure_id": starting_point,
            "arrival_id": destination_city_code,
            "outbound_date": from_time.strftime("%Y-%m-%d"),
            "return_date": to_time.strftime("%Y-%m-%d"),
            "type": "1",
            "adults": "1",
            "currency": "GBP",
            "api_key": self.myapikey,
        }

        if is_direct:
            query["stops"] = "1"

        response = requests.get(url=SERPAPI_ENDPOINT, params=query)

        if response.status_code != 200:
            print(f"check_flights() response code: {response.status_code}")
            return None

        data = response.json()

        if "error" in data:
            print(f"API error: {data['error']}")
            return None

        return data
