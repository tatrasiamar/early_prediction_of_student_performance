from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def home(request):
    return render(request,'home.html')

import joblib
import numpy as np

# Load the trained model
model = joblib.load(r"./prediction/random_forest/random_forest_model.joblib")

def handle_missing_values(data):
    # Replace missing values with a default value or use imputation techniques
    for key, value in data.items():
        if value is None or value == '':
            data[key] = 0  # Replace missing values with 0 for demonstration purposes
    return data

def predict(request):
    if request.method == 'POST':
        # Retrieve form data
        course = request.POST.get('course')
        daytime_attendance = 1
        previous_qualification = 2
        educational_special_needs = 2
        gender = request.POST.get('gender')
        scholarship_holder = request.POST.get('scholarship_holder')
        curricular_units_1st_sem_credited = request.POST.get('curricular_units_1st_sem_credited')
        curricular_units_1st_sem_enrolled = request.POST.get('curricular_units_1st_sem_enrolled')
        curricular_units_1st_sem_evaluations = request.POST.get('curricular_units_1st_sem_evaluations')
        curricular_units_1st_sem_approved = request.POST.get('curricular_units_1st_sem_approved')
        curricular_units_1st_sem_grade = request.POST.get('curricular_units_1st_sem_grade')
        curricular_units_1st_sem_without_evaluations = request.POST.get('curricular_units_1st_sem_without_evaluations')
        curricular_units_2nd_sem_credited = request.POST.get('curricular_units_2nd_sem_credited')
        curricular_units_2nd_sem_enrolled = request.POST.get('curricular_units_2nd_sem_enrolled')
        curricular_units_2nd_sem_evaluations = request.POST.get('curricular_units_2nd_sem_evaluations')
        curricular_units_2nd_sem_approved = request.POST.get('curricular_units_2nd_sem_approved')
        curricular_units_2nd_sem_grade = request.POST.get('curricular_units_2nd_sem_grade')
        curricular_units_2nd_sem_without_evaluations = request.POST.get('curricular_units_2nd_sem_without_evaluations')

        # Create a dictionary of form data
        data = {
            'course': course,
            'daytime_attendance': daytime_attendance,
            'previous_qualification': previous_qualification,
            'educational_special_needs': educational_special_needs,
            'gender': gender,
            'scholarship_holder': scholarship_holder,
            'curricular_units_1st_sem_credited': curricular_units_1st_sem_credited,
            'curricular_units_1st_sem_enrolled': curricular_units_1st_sem_enrolled,
            'curricular_units_1st_sem_evaluations': curricular_units_1st_sem_evaluations,
            'curricular_units_1st_sem_approved': curricular_units_1st_sem_approved,
            'curricular_units_1st_sem_grade': curricular_units_1st_sem_grade,
            'curricular_units_1st_sem_without_evaluations': curricular_units_1st_sem_without_evaluations,
            'curricular_units_2nd_sem_credited': curricular_units_2nd_sem_credited,
            'curricular_units_2nd_sem_enrolled': curricular_units_2nd_sem_enrolled,
            'curricular_units_2nd_sem_evaluations': curricular_units_2nd_sem_evaluations,
            'curricular_units_2nd_sem_approved': curricular_units_2nd_sem_approved,
            'curricular_units_2nd_sem_grade': curricular_units_2nd_sem_grade,
            'curricular_units_2nd_sem_without_evaluations': curricular_units_2nd_sem_without_evaluations
        }

        # Handle missing values
        data = handle_missing_values(data)

        # Encode categorical variables
        gender_encoded = 1 if data['gender'] == 'female' else 0
        # Add other encoding logic for categorical variables
        
        # Perform prediction using the loaded model
        prediction = model.predict([[
            data['course'], data['daytime_attendance'], data['previous_qualification'], data['educational_special_needs'],
            gender_encoded, data['scholarship_holder'], data['curricular_units_1st_sem_credited'],
            data['curricular_units_1st_sem_enrolled'], data['curricular_units_1st_sem_evaluations'],
            data['curricular_units_1st_sem_approved'], data['curricular_units_1st_sem_grade'],
            data['curricular_units_1st_sem_without_evaluations'], data['curricular_units_2nd_sem_credited'],
            data['curricular_units_2nd_sem_enrolled'], data['curricular_units_2nd_sem_evaluations'],
            data['curricular_units_2nd_sem_approved'], data['curricular_units_2nd_sem_grade'],
            data['curricular_units_2nd_sem_without_evaluations']
        ]])

        # Map prediction result to human-readable format
        prediction_result = []
        if prediction[0] == 0:
            prediction_result.append("dropout")
            prediction_result.append("graduate")
        elif prediction[0] == 1:
            prediction_result.append("intermediate")
            prediction_result.append("dropout")
        else:
            prediction_result.append("graduate")
            prediction_result.append("intermediate")

        # Pass the prediction result to the results.html template
        return render(request, 'results.html', {'prediction_resultone': prediction_result[0],'prediction_resulttwo':prediction_result[1]})
    else:
        return render(request, 'index.html')  # Render the form page if it's a GET request
