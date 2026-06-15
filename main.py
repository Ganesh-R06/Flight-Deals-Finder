import requests_cache
import requests
from pprint import pprint
from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import find_cheapest_flight
from notification_manager import NotificationManager

def get_gbp_to_inr_rate():
    try:
        url = "https://api.exchangerate-api.com/v4/latest/GBP"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data["rates"]["INR"]
    except Exception as e:
        print(f"Error fetching exchange rate: {e}")
        return 127.62

requests_cache.install_cache(
    "flight_cache",
    urls_expire_after={
        "*.sheety.co*": requests_cache.DO_NOT_CACHE,
        "*": 3600,
    }
)
data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
flight_search = FlightSearch()
notification_manager = NotificationManager()

customer_data = data_manager.get_customer_emails()
customer_emails = [column["enterYourEmail?"] for column in customer_data]

tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=(6 * 30))
starting_point= "BLR"

live_inr_rate = get_gbp_to_inr_rate()

for destination in sheet_data:
    pprint(f"Getting flights for {destination['city']}...")

    flights = flight_search.check_flights(starting_point,destination["iataCode"],from_time=tomorrow,to_time=six_month_from_today)

    cheapest_flight = find_cheapest_flight(data=flights, return_date=six_month_from_today.strftime("%Y-%m-%d"))

    pprint(f"{destination['city']}: GBP {cheapest_flight.price}")
    pprint(f"Flight Price: {cheapest_flight.price}")
    pprint(f"Sheet Price: {destination['lowestPrice']}")

    if cheapest_flight.price != "N/A" and cheapest_flight.price <= destination["lowestPrice"]:
        pprint(f"Lower price flight found to {destination['city']}!")

        # Convert the GBP price to INR
        price_in_inr = round(cheapest_flight.price * live_inr_rate, 2)

        data_manager.update_lowest_price(destination["id"], cheapest_flight.price)

        message = (f"Low price alert! Only ₹{price_in_inr} INR (GBP {cheapest_flight.price}) to fly "
                   f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, "
                   f"on {cheapest_flight.out_date} until {cheapest_flight.return_date}.")

        notification_manager.send_emails(emails=customer_emails, message_body=message)
