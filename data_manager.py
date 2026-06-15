import os
import requests

sheety_endpoint = "https://api.sheety.co/f4b7c83a26773b93b98ac4cf6aaca0a0/flightDeals/prices"
sheety_endpoint_user = "https://api.sheety.co/f4b7c83a26773b93b98ac4cf6aaca0a0/flightDeals/users"

headers = {
    "Authorization": os.environ["SHEETY_AUTH"]
}


class DataManager:
    def __init__(self):
        self.destination_data = {}
        self.customer_data = {}

    def get_destination_data(self):
        response = requests.get(sheety_endpoint, headers=headers)
        response.raise_for_status()
        response1 = response.json()
        return response1["prices"]

    def update_lowest_price(self, row_id, new_price):
        new_data = {
            "price": {
                "lowestPrice": new_price
            }
        }

        requests.put(
            url=f"{sheety_endpoint}/{row_id}",
            json=new_data,
            headers=headers
        )

    def get_customer_emails(self):
        response = requests.get(
            url=sheety_endpoint_user,
            headers=headers
        )

        data = response.json()
        self.customer_data = data["users"]
        return self.customer_data
