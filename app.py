# Import Modules(Flask, Pandas, Pickle)
from flask import Flask, render_template, request
import pandas as pd
import pickle

# Load model, encoders, and scaler
with open('best_model.pkl', 'rb') as model_file:
    loaded_model = pickle.load(model_file)
with open('encoder.pkl', 'rb') as encoders_file:
    encoders = pickle.load(encoders_file)
with open('scaler.pkl', 'rb') as scaler_file:
    scaler_data = pickle.load(scaler_file)

app = Flask(__name__)

def make_prediction(input_data):
    input_df = pd.DataFrame([input_data])

    for col, encoder in encoders.items():
        input_df[col] = encoder.transform(input_df[col])

    numerical_cols = ['tenure', 'MonthlyCharges', 'TotalCharges']
    input_df[numerical_cols] = scaler_data.transform(input_df[numerical_cols])

    prediction = loaded_model.predict(input_df)[0]
    probability = loaded_model.predict_proba(input_df)[0, 1]
    return "Churn" if prediction == 1 else "No Churn", probability

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    probability = None
    error_message = None
    
    if request.method == 'POST':
        try:
            # Extract and validate input data
            tenure = int(request.form['tenure'])
            monthly_charges = float(request.form['MonthlyCharges'])
            total_charges = float(request.form['TotalCharges'])
            
            # Input validation
            if tenure <= 0:
                error_message = "Tenure must be greater than 0 months"
            elif monthly_charges <= 0:
                error_message = "Monthly charges must be greater than 0"
            elif total_charges < 0:
                error_message = "Total charges cannot be negative"
            elif monthly_charges > 1000000:
                error_message = "Monthly charges seem too high (max: $1000000)"
            elif tenure > 120:
                error_message = "Tenure seems too high (max: 120 months)"
            
            if error_message is None:
                input_data = {
                    'gender': request.form['gender'],
                    'SeniorCitizen': int(request.form['SeniorCitizen']),
                    'Partner': request.form['Partner'],
                    'Dependents': request.form['Dependents'],
                    'tenure': tenure,
                    'PhoneService': request.form['PhoneService'],
                    'MultipleLines': request.form['MultipleLines'],
                    'InternetService': request.form['InternetService'],
                    'OnlineSecurity': request.form['OnlineSecurity'],
                    'OnlineBackup': request.form['OnlineBackup'],
                    'DeviceProtection': request.form['DeviceProtection'],
                    'TechSupport': request.form['TechSupport'],
                    'StreamingTV': request.form['StreamingTV'],
                    'StreamingMovies': request.form['StreamingMovies'],
                    'Contract': request.form['Contract'],
                    'PaperlessBilling': request.form['PaperlessBilling'],
                    'PaymentMethod': request.form['PaymentMethod'],
                    'MonthlyCharges': monthly_charges,
                    'TotalCharges': total_charges,
                }

                prediction, probability = make_prediction(input_data)
                
        except ValueError:
            error_message = "Please enter valid numeric values for tenure and charges"
        except Exception as e:
            error_message = f"An error occurred: {str(e)}"

    return render_template('index.html', prediction=prediction, probability=probability, error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)