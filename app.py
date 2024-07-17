from flask import Flask, request, jsonify, render_template
import pandas as pd
import joblib

# Path to the pre-trained model
model_path = 'C:\\Users\\Ahmed\\Desktop\\pricess_prediction_model.pkl'

# Initialize Flask application
app = Flask(__name__)

# Load the pre-trained model pipeline
model_pipeline = joblib.load(model_path)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/calculator')
def calculator():
    return render_template('calculator.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json

    # Set default values and ensure correct types
    defaults = {
        'baths': 0,
        'bedrooms': 0,
        'area_size': 0.0,
        'property_type': 'Unknown',
        'city': 'Unknown',
        'province_name': 'Unknown',
        'location': 'Unknown',
        'Area Type': 'Unknown'
    }
    
    # Update defaults with provided data, using defaults for missing keys
    data = {key: data.get(key, defaults[key]) for key in defaults}

    try:
        data['baths'] = int(data['baths'])
        data['bedrooms'] = int(data['bedrooms'])
        data['Area Size'] = float(data['area_size'])
    except ValueError as e:
        return jsonify({'error': 'Invalid input data types'}), 400

    # Define expected columns for prediction
    expected_columns = [
        'property_type', 'city', 'province_name', 'location',
        'baths', 'bedrooms', 'Area Type', 'Area Size'
    ]
    
    # Create DataFrame from the input data
    df = pd.DataFrame([data])

    # Ensure columns are in the correct order
    df = df.reindex(columns=expected_columns)

    # Print DataFrame for debugging
    print(df.head())
    
    try:
        # Predict the house price
        prediction = model_pipeline.predict(df)
        price = float(prediction[0])
        return jsonify({'price': f'PKR {price:,.2f}'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
