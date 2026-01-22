from django.shortcuts import render
import pickle
import numpy as np
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

model_path = os.path.join(BASE_DIR, "model.pkl")
scaler_path = os.path.join(BASE_DIR, "scaler (1).pkl")

model = pickle.load(open(model_path, "rb"))
scaler = pickle.load(open(scaler_path, "rb"))


def home(request):
    prediction = None
    probability = None

    if request.method == "POST":
        try:
            # Collect input data (ORDER MUST MATCH TRAINING)
            data = [
                float(request.POST.get("Account_length")),
                float(request.POST.get("International_plan")),
                float(request.POST.get("Voice_mail_plan")),
                float(request.POST.get("Number_vmail_messages")),
                float(request.POST.get("Total_day_minutes")),
                float(request.POST.get("Total_day_calls")),
                float(request.POST.get("Total_eve_minutes")),
                float(request.POST.get("Total_eve_calls")),
                float(request.POST.get("Total_night_minutes")),
                float(request.POST.get("Total_night_calls")),
                float(request.POST.get("Total_intl_minutes")),
                float(request.POST.get("Total_intl_calls")),
                float(request.POST.get("Customer_service_calls"))
            ]

            # Convert to numpy array and scale
            data = np.array(data).reshape(1, -1)
            data = scaler.transform(data)

            # Prediction
            result = model.predict(data)[0]
            prob = model.predict_proba(data)[0][1] * 100  # churn probability %

            prediction = "High Churn Risk" if result == 1 else "Low Churn Risk"
            probability = round(prob, 2)

        except Exception as e:
            prediction = "Error in input values"
            probability = None

    return render(
        request,
        "index.html",
        {
            "prediction": prediction,
            "probability": probability
        }
    )
