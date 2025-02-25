import os
from flask import Flask, request, jsonify, render_template
import util as util

app = Flask(__name__, static_folder='client', template_folder='client')

@app.route('/')
def home():
    return render_template('app.html')

@app.route('/get_location_names')
def get_location_names():
    response = jsonify({
        'locations': util.get_location_names()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/predict_home_price', methods=['GET', 'POST'])
def predict_home_price():
    try:
        total_sqft = float(request.form['total_sqft'])
        location = request.form['location']
        bhk = int(request.form['bhk'])
        bath = int(request.form['bath'])
    except (KeyError, ValueError) as e:
        return jsonify({'error': 'Invalid input data', 'message': str(e)}), 400

    response = jsonify({
        'estimated_price': util.get_estimated_price(location, total_sqft, bhk, bath)
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


if __name__ == "__main__":
    print("Starting Python Flask Server For Home Price Prediction...")
    util.load_saved_artifacts()
    port = int(os.environ.get("PORT", 5000))  # Use dynamic port from Vercel
    app.run(host='0.0.0.0', port=port, debug=True)
