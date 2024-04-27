from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    """
    Render the index page of the BMI calculator.
    
    Returns:
        str: Rendered HTML content of the index page.
    """
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate_bmi():
    """
    Calculate the BMI based on user input and return the result as JSON.
    
    Returns:
        dict: JSON object containing the calculated BMI result.
    """
    try:
        height = float(request.form['height'])
        weight = float(request.form['weight'])
        bmi = calculate_bmi_value(height, weight)
        category = determine_bmi_category(bmi)
        ideal_weight_range = calculate_ideal_weight_range(height)
        weight_difference = calculate_weight_difference(weight, ideal_weight_range)
        return jsonify({
            'bmi': bmi,
            'category': category,
            'ideal_weight_range': ideal_weight_range,
            'weight_difference': weight_difference
        })
    except KeyError:
        return jsonify({'error': 'Missing parameters'}), 400
    except ValueError:
        return jsonify({'error': 'Invalid input data'}), 400

def calculate_bmi_value(height, weight):
    """
    Calculate the BMI value based on height and weight.
    
    Args:
        height (float): Height in meters.
        weight (float): Weight in kilograms.
    
    Returns:
        float: Calculated BMI value.
    """
    bmi = weight / (height ** 2)
    return round(bmi, 2)

def determine_bmi_category(bmi):
    """
    Determine the BMI category based on the calculated BMI value.
    
    Args:
        bmi (float): Calculated BMI value.
    
    Returns:
        str: BMI category (e.g., 'Underweight', 'Normal', 'Overweight', 'Obese').
    """
    if bmi < 18.5:
        return 'Underweight'
    elif 18.5 <= bmi < 25:
        return 'Normal'
    elif 25 <= bmi < 30:
        return 'Overweight'
    else:
        return 'Obese'

def calculate_ideal_weight_range(height):
    """
    Calculate the ideal weight range based on height.
    
    Args:
        height (float): Height in meters.
    
    Returns:
        tuple: Ideal weight range (lower_bound, upper_bound) in kilograms.
    """
    lower_bound = 18.5 * (height ** 2)
    upper_bound = 24.9 * (height ** 2)
    return round(lower_bound, 2), round(upper_bound, 2)

def calculate_weight_difference(weight, ideal_weight_range):
    """
    Calculate the difference between the current weight and the ideal weight range.
    
    Args:
        weight (float): Current weight in kilograms.
        ideal_weight_range (tuple): Ideal weight range (lower_bound, upper_bound) in kilograms.
    
    Returns:
        float: Difference between the current weight and the ideal weight range.
    """
    lower_bound, upper_bound = ideal_weight_range
    if weight < lower_bound:
        return round(lower_bound - weight, 2)
    elif weight > upper_bound:
        return round(weight - upper_bound, 2)
    else:
        return 0

if __name__ == '__main__':
    app.run(debug=True)
