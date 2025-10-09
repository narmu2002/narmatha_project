from django.shortcuts import render
import os
import pickle
from django.http import JsonResponse
import numpy as np
import pandas as pd

MODEL_PATH = os.path.join(os.path.dirname(__file__), "ml_models/insurance_model.pkl")
model = pickle.load(open(MODEL_PATH, "rb"))
sex_encoder = pickle.load(open("sex_encoder.pkl", "rb"))
smoker_encoder = pickle.load(open("smoker_encoder.pkl", "rb"))

from sklearn.preprocessing import LabelEncoder

def predict(request):
    if request.method == "POST":
        # 1. Get form data
        age = int(request.POST.get("age"))
        sex = request.POST.get("sex")        # 'male' or 'female'
        bmi = float(request.POST.get("bmi"))
        children = int(request.POST.get("children"))
        smoker = request.POST.get("smoker")  # 'yes' or 'no'

        # 2. Encode categorical variables manually
        sex_map = {"male": 1, "female": 0}
        smoker_map = {"yes": 1, "no": 0}

        sex_encoded = sex_map.get(sex, 0)
        smoker_encoded = smoker_map.get(smoker, 0)

        # 3. Prepare input DataFrame for the model
        input_data = pd.DataFrame([{
            "age": age,
            "sex": sex_encoded,
            "bmi": bmi,
            "children": children,
            "smoker": smoker_encoded
        }])

        # 4. Predict using the model
        prediction = model.predict(input_data)[0]

        return render(request, "result.html", {"prediction": round(prediction, 2)})

    return render(request, "predict.html")

