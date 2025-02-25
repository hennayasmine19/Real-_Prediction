import pickle
import json
import numpy as np
import os

__locations = None
__data_columns = None
__model = None

def get_estimated_price(location, sqft, bhk, bath):
    if __model is None:
        raise Exception("Model is not loaded. Please load the artifacts first.")
    
    try:
        loc_index = next((i for i, loc in enumerate(__data_columns) if loc.lower() == location.lower()), -1)
    except:
        loc_index = -1

    x = np.zeros(len(__data_columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk
    if loc_index >= 0:
        x[loc_index] = 1

    return round(__model.predict([x])[0], 2)

def get_location_names():
    if __locations is None:
        return []
    return __locations

def load_saved_artifacts():
    global __data_columns, __locations, __model
    print("Loading artifacts...")
    try:
        # Dynamically find the base directory on Render
        base_dir = os.path.join(os.getcwd(), "artifacts")
        columns_path = os.path.join(base_dir, "columns.json")
        model_path = os.path.join(base_dir, "Real_Estate_Prediction.pickle")

        with open(columns_path, 'r') as f:
            __data_columns = json.load(f)['data_columns']
            __locations = __data_columns[3:]
            print("Columns and locations loaded successfully.")

        with open(model_path, 'rb') as f:
            __model = pickle.load(f)
            print("Model loaded successfully.")
    except FileNotFoundError as e:
        print(f"Error loading artifacts: {e}")

if __name__ == '__main__':
    load_saved_artifacts()
    print(get_location_names())
    print(get_estimated_price('1st Phase JP Nagar', 1000, 3, 3))
    print(get_estimated_price('1st Phase JP Nagar', 1000, 2, 2))
    print(get_estimated_price('Kalhalli', 1000, 2, 2))
    print(get_estimated_price('Ejipura', 1000, 2, 2))
