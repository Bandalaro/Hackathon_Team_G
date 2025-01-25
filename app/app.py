from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

# Movie and seat data (you can replace this with a database in production)
movies = [
    {"name": "Gravity", "language": "English", "time": "7:00 PM", "date": "2025-01-25"},
    {"name": "The Hobbit", "language": "English", "time": "9:00 PM", "date": "2025-01-25"},
    {"name": "Thor", "language": "Hindi", "time": "6:00 PM", "date": "2025-01-25"},
    {"name": "The Hunger Games", "language": "English", "time": "8:30 PM", "date": "2025-01-25"}
]

seats = [False] * 50  # False means available, True means booked

seat_prices = {
    "economy": 150,
    "gold": 250,
    "vip": 450
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/movies', methods=['GET'])
def get_movies():
    return jsonify(movies)

@app.route('/seats', methods=['GET'])
def get_seats():
    return jsonify({"seats": seats})

@app.route('/book', methods=['POST'])
def book_seats():
    data = request.json
    selected_seats = data.get('selected_seats', [])
    total_price = 0

    for index in selected_seats:
        if index < 0 or index >= len(seats) or seats[index]:
            return jsonify({"error": "Invalid or already booked seat."}), 400

        seats[index] = True

        # Determine seat category based on index
        if index <= 19:
            total_price += seat_prices["economy"]
        elif index <= 39:
            total_price += seat_prices["gold"]
        else:
            total_price += seat_prices["vip"]

    return jsonify({"message": "Booking confirmed!", "total_price": total_price})

@app.route('/analysis/revenue', methods=['GET'])
def get_revenue():
    total_revenue = 0
    economy_count = sum(1 for i in range(20) if seats[i])
    gold_count = sum(1 for i in range(20, 40) if seats[i])
    vip_count = sum(1 for i in range(40, 50) if seats[i])

    total_revenue = (economy_count * seat_prices["economy"] +
                     gold_count * seat_prices["gold"] +
                     vip_count * seat_prices["vip"])

    return jsonify({
        "total_revenue": total_revenue,
        "economy_seats_booked": economy_count,
        "gold_seats_booked": gold_count,
        "vip_seats_booked": vip_count
    })

@app.route('/analysis/occupancy', methods=['GET'])
def get_occupancy():
    total_seats = len(seats)
    booked_seats = sum(1 for seat in seats if seat)
    occupancy_rate = (booked_seats / total_seats) * 100

    return jsonify({
        "total_seats": total_seats,
        "booked_seats": booked_seats,
        "occupancy_rate": occupancy_rate
    })

if __name__ == '__main__':
    app.run(debug=True)
