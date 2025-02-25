import os
from flask import Flask, request, jsonify, render_template
import util as util

app = Flask(__name__, static_folder='client', template_folder='client')

# Load the model artifacts when the server starts
util.load_saved_artifacts()

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

    try:
        estimated_price = util.get_estimated_price(location, total_sqft, bhk, bath)
        response = jsonify({'estimated_price': estimated_price})
    except Exception as e:
        response = jsonify({'error': 'Model error', 'message': str(e)})

    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


if __name__ == "__main__":
    print("Starting Python Flask Server For Home Price Prediction...")
    port = int(os.environ.get("PORT", 5000))  # Use dynamic port for Render
    app.run(host='0.0.0.0', port=port, debug=True)
