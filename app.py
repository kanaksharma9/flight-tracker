from flask import Flask, jsonify
import requests

app = Flask(__name__)

def get_flights(arrival, departure):
    url = "https://api.aviationstack.com/v1/flights?access_key=b14e5d900b501861bc654e9f32f43589"

    try:
        response = requests.get(url)
        if response.status_code != 200:
            return {"error": "API request failed", "status_code": response.status_code}
        
        data = response.json()
        if "data" not in data:
            return {"error": "Invalid API response"}

        flights_list = []

        for i in data["data"]:
            departure_airport = i.get("departure", {}).get("airport", "Unknown")
            arrival_airport = i.get("arrival", {}).get("airport", "Unknown")
            airline_name = i.get("airline", {}).get("name", "Unknown Airline")
            flight_date_dep = i.get("departure", {}).get("scheduled", "Unknown")
            flight_date_arr = i.get("arrival", {}).get("scheduled", "Unknown")

            if departure_airport == departure and arrival_airport == arrival:
                flights_list.append({
                    "airline": airline_name,
                    "departure_time": flight_date_dep,
                    "arrival_time": flight_date_arr
                })

        if not flights_list:
            return {"error": "No matching flights found"}

        return flights_list

    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}

@app.route('/')
def hello():
    departure = input('Enter your departure Airport:\n')
    arrival = input("Enter your arrival airport:\n")

    flights = get_flights(arrival, departure)  

    return jsonify(flights)

if __name__ == '__main__':
    app.run(debug=True)
