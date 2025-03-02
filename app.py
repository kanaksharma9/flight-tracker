from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)
API_KEY = os.getenv("FLIGHT_API_KEY")
API_KEY = "b14e5d900b501861bc654e9f32f43589"
API_URL = "https://api.aviationstack.com/v1/flights"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/track', methods=['GET', 'POST'])
def track():
    flights = []
    departure = None  # Initialize variables to avoid UnboundLocalError
    arrival = None

    if request.method == 'POST':
        departure = request.form.get('departure')
        arrival = request.form.get('arrival')
        params = {"access_key": API_KEY, "dep_iata": departure, "arr_iata": arrival}
        try:
            response = requests.get(API_URL, params=params)
            response.raise_for_status()
            data = response.json()
            flights = data.get("data", [])
        except requests.exceptions.RequestException as e:
            return jsonify({"error": "Failed to fetch flight data", "details": str(e)}), 500

    return render_template('track.html', flights=flights, departure=departure, arrival=arrival)

@app.route('/map')
def map_view():
    params = {"access_key": API_KEY, "flight_status": "active"}
    flights = []
    try:
        response = requests.get(API_URL, params=params)
        response.raise_for_status()
        data = response.json()
        flights = data.get("data", [])
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Failed to fetch live flight data", "details": str(e)}), 500
    return render_template('map.html', flights=flights)


if __name__ == '__main__':
    app.run(debug=True)
