from flask import Flask, request, jsonify, render_template_string, redirect, url_for
import requests
from datetime import datetime, timedelta
import logging
import base64
import os
from dotenv import load_dotenv
from difflib import SequenceMatcher

app = Flask(__name__)

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Environment variables
TEKMETRIC_API_URL = os.getenv('TEKMETRIC_API_URL', 'https://sandbox.tekmetric.com/api/v1')
SHOP_ID = os.getenv('SHOP_ID')
CLIENT_ID = os.getenv('TEKMETRICS_CLIENT_ID')
CLIENT_SECRET = os.getenv('TEKMETRICS_CLIENT_SECRET')
TOKEN_URL = f'{TEKMETRIC_API_URL}/oauth/token'

# CSS for styling
css_styles = '''
<style>
    body {
        font-family: Arial, sans-serif;
        background-color: #f8f9fa;
        color: #343a40;
        margin: 0;
        padding: 0;
    }
    header {
        background-color: #007bff;
        color: white;
        padding: 1em;
        text-align: center;
    }
    h1, h2, p {
        margin: 0.5em 0;
    }
    form, .content {
        max-width: 800px;
        margin: 2em auto;
        padding: 1em;
        background: white;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    }
    label {
        display: block;
        margin-bottom: 0.5em;
        font-weight: bold;
    }
    input[type="text"], input[type="date"] {
        width: 100%;
        padding: 0.5em;
        margin-bottom: 1em;
        border: 1px solid #ced4da;
        border-radius: 0.25em;
    }
    input[type="submit"], .button {
        display: inline-block;
        padding: 0.5em 1em;
        color: white;
        background-color: #007bff;
        border: none;
        border-radius: 0.25em;
        text-decoration: none;
        cursor: pointer;
    }
    input[type="submit"]:hover, .button:hover {
        background-color: #0056b3;
    }
    ul {
        list-style-type: none;
        padding: 0;
    }
    li {
        background: #f1f3f5;
        margin-bottom: 0.5em;
        padding: 0.5em;
        border-radius: 0.25em;
    }
</style>
'''

# HTML template for the form
form_template = '''
<!DOCTYPE html>
<html>
<head>
    <title>Tekmetric Search</title>
    ''' + css_styles + '''
</head>
<body>
    <header>
        <h1>Tekmetric Search</h1>
    </header>
    <div class="content">
        <form action="/search_customer" method="post">
            <label for="customerName">Customer Name:</label>
            <input type="text" id="customerName" name="customerName" placeholder="Enter customer name" required>
            <input type="submit" value="Search">
        </form>
        <form action="/search_vehicle" method="post">
            <label for="vehicleMake">Vehicle Make:</label>
            <input type="text" id="vehicleMake" name="vehicleMake" placeholder="Enter vehicle make">
            <label for="vehicleModel">Vehicle Model:</label>
            <input type="text" id="vehicleModel" name="vehicleModel" placeholder="Enter vehicle model">
            <label for="vehicleYear">Vehicle Year:</label>
            <input type="text" id="vehicleYear" name="vehicleYear" placeholder="Enter vehicle year">
            <label for="vehicleColor">Vehicle Color:</label>
            <input type="text" id="vehicleColor" name="vehicleColor" placeholder="Enter vehicle color">
            <input type="submit" value="Search">
        </form>
        <form action="/search_appointments" method="post">
            <label for="startDate">Start Date:</label>
            <input type="date" id="startDate" name="startDate" value="{{ default_start_date }}">
            <label for="endDate">End Date:</label>
            <input type="date" id="endDate" name="endDate" value="{{ default_end_date }}">
            <input type="submit" value="Search Appointments">
        </form>
        {% if customers %}
            <h2>Customer Matches:</h2>
            <ul>
                {% for customer in customers %}
                    <li>
                        <a href="/profile/{{ customer['id'] }}">{{ customer['firstName'] }} {{ customer['lastName'] }}</a> - 
                        ID: {{ customer['id'] }} - 
                        Email: {{ customer['email'] }} - 
                        Birthday: {{ customer['birthday'] }} - 
                        Vehicles: 
                        {% for vehicle in customer['vehicles'] %}
                            <a href="/vehicle_profile/{{ vehicle['id'] }}">{{ vehicle['year'] }} {{ vehicle['make'] }} {{ vehicle['model'] }} {{ vehicle['subModel'] }}</a> (VIN: <a href="/vehicle_profile/{{ vehicle['id'] }}">{{ vehicle['vin'] }}</a>){% if not loop.last %}, {% endif %}
                        {% endfor %}
                    </li>
                {% endfor %}
            </ul>
        {% endif %}
        {% if vehicles %}
            <h2>Vehicle Matches:</h2>
            <ul>
                {% for vehicle in vehicles %}
                    <li>
                        <a href="/vehicle_profile/{{ vehicle['id'] }}">{{ vehicle['year'] }} {{ vehicle['make'] }} {{ vehicle['model'] }} {{ vehicle['subModel'] }}</a> - 
                        Color: {{ vehicle['color'] }} - 
                        VIN: <a href="/vehicle_profile/{{ vehicle['id'] }}">{{ vehicle['vin'] }}</a> - 
                        License Plate: {{ vehicle['licensePlate'] }} - 
                        State: {{ vehicle['state'] }} - 
                        Customer ID: {{ vehicle['customerId'] }}
                    </li>
                {% endfor %}
            </ul>
        {% endif %}
        {% if appointments %}
            <h2>Appointments:</h2>
            <ul>
                {% for appointment in appointments %}
                    <li>
                        <a href="/appointment/{{ appointment['id'] }}">{{ appointment['id'] }}</a>: {{ appointment['startTime'] }} - {{ appointment['endTime'] }}: {{ appointment['description'] }} - Customer: {{ appointment['customerName'] }} - Vehicle: {{ appointment['vehicleInfo'] }}
                    </li>
                {% endfor %}
            </ul>
        {% endif %}
    </div>
</body>
</html>
'''

# HTML template for the customer profile
profile_template = '''
<!DOCTYPE html>
<html>
<head>
    <title>Customer Profile: {{ customer['firstName'] }} {{ customer['lastName'] }}</title>
    ''' + css_styles + '''
</head>
<body>
    <header>
        <h1>Customer Profile</h1>
        <a href="/" class="button">Home</a>
    </header>
    <div class="content">
        <h2>{{ customer['firstName'] }} {{ customer['lastName'] }}</h2>
        <p><strong>ID:</strong> {{ customer['id'] }}</p>
        <p><strong>Email:</strong> {{ customer['email'] }}</p>
        <p><strong>Birthday:</strong> {{ customer['birthday'] }}</p>
        <p><strong>Type:</strong> {{ customer['customerType']['name'] }}</p>
        <p><strong>Notes:</strong> {{ customer['notes'] }}</p>
        <p><strong>Address:</strong> {{ customer['address']['fullAddress'] }}</p>
        
        <h2>Vehicles</h2>
        <ul>
            {% for vehicle in vehicles %}
                <li>
                    {{ vehicle['year'] }} {{ vehicle['make'] }} {{ vehicle['model'] }} - {{ vehicle['subModel'] }}<br>
                    VIN: <a href="/vehicle_profile/{{ vehicle['id'] }}">{{ vehicle['vin'] }}</a><br>
                    License Plate: {{ vehicle['licensePlate'] }}<br>
                    State: {{ vehicle['state'] }}<br>
                    Drive Type: {{ vehicle['driveType'] }}<br>
                    Transmission: {{ vehicle['transmission'] }}<br>
                    Body Type: {{ vehicle['bodyType'] }}<br>
                    Engine: {{ vehicle['engine'] }}<br>
                    Color: {{ vehicle['color'] }}<br>
                    Notes: {{ vehicle['notes'] }}
                </li>
            {% endfor %}
        </ul>

        <h2>Service Dates</h2>
        <ul>
            {% for appointment in appointments %}
                <li>{{ appointment['startTime'] }} - {{ appointment['description'] }}</li>
            {% endfor %}
        </ul>

        <h2>Repair Orders</h2>
        <ul>
            {% for order in repair_orders %}
                <li>
                    <strong>Order #{{ order['repairOrderNumber'] }}:</strong> {{ order['repairOrderStatus']['name'] }}<br>
                    Amount Paid: {{ order['amountPaid'] }}<br>
                    Labor Sales: {{ order['laborSales'] }}<br>
                    Parts Sales: {{ order['partsSales'] }}<br>
                    Sublet Sales: {{ order['subletSales'] }}<br>
                    Fees: {{ order['feeTotal'] }}<br>
                    Discounts: {{ order['discountTotal'] }}<br>
                    Total Sales: {{ order['totalSales'] }}<br>
                    Jobs:
                    <ul>
                        {% for job in order['jobs'] %}
                            <li>{{ job['name'] }} - {{ job['note'] }}</li>
                        {% endfor %}
                    </ul>
                    Customer Concerns:
                    <ul>
                        {% for concern in order['customerConcerns'] %}
                            <li>{{ concern['concern'] }}</li>
                        {% endfor %}
                    </ul>
                </li>
            {% endfor %}
        </ul>

        <form action="/search_customer" method="post">
            <label for="customerName">Search Another Customer:</label>
            <input type="text" id="customerName" name="customerName" placeholder="Enter customer name" required>
            <input type="submit" value="Search">
        </form>
    </div>
</body>
</html>
'''

# HTML template for the appointment profile
appointment_profile_template = '''
<!DOCTYPE html>
<html>
<head>
    <title>Appointment Profile: {{ appointment['id'] }}</title>
    ''' + css_styles + '''
</head>
<body>
    <header>
        <h1>Appointment Profile</h1>
        <a href="/" class="button">Home</a>
    </header>
    <div class="content">
        <h2>Appointment ID: {{ appointment['id'] }}</h2>
        <p><strong>Shop ID:</strong> {{ appointment['shopId'] }}</p>
        <p><strong>Customer:</strong> <a href="/profile/{{ appointment['customerId'] }}">{{ appointment['customerName'] }}</a></p>
        <p><strong>Vehicle:</strong> <a href="/vehicle_profile/{{ appointment['vehicleId'] }}">{{ appointment['vehicleInfo'] }}</a> (VIN: <a href="/vehicle_profile/{{ appointment['vehicleId'] }}">{{ appointment['vehicleVin'] }}</a>)</p>
        <p><strong>Start Time:</strong> {{ appointment['startTime'] }}</p>
        <p><strong>End Time:</strong> {{ appointment['endTime'] }}</p>
        <p><strong>Description:</strong> {{ appointment['description'] }}</p>
        <p><strong>Created Date:</strong> {{ appointment['createdDate'] }}</p>
        <p><strong>Updated Date:</strong> {{ appointment['updatedDate'] }}</p>
    </div>
</body>
</html>
'''

# HTML template for the vehicle profile
vehicle_profile_template = '''
<!DOCTYPE html>
<html>
<head>
    <title>Vehicle Profile: {{ vehicle['year'] }} {{ vehicle['make'] }} {{ vehicle['model'] }}</title>
    ''' + css_styles + '''
</head>
<body>
    <header>
        <h1>Vehicle Profile</h1>
        <a href="/" class="button">Home</a>
    </header>
    <div class="content">
        <h2>{{ vehicle['year'] }} {{ vehicle['make'] }} {{ vehicle['model'] }}</h2>
        <p><strong>VIN:</strong> {{ vehicle['vin'] }}</p>
        <p><strong>Color:</strong> {{ vehicle['color'] }}</p>
        <p><strong>Drive Type:</strong> {{ vehicle['driveType'] }}</p>
        <p><strong>Body Type:</strong> {{ vehicle['bodyType'] }}</p>
        <p><strong>Engine:</strong> {{ vehicle['engine'] }}</p>
        <p><strong>Transmission:</strong> {{ vehicle['transmission'] }}</p>
        <p><strong>Notes:</strong> {{ vehicle['notes'] }}</p>

        <h2>Owner Information</h2>
        <p><strong>Owner:</strong> <a href="/profile/{{ customer['id'] }}">{{ customer['firstName'] }} {{ customer['lastName'] }}</a></p>
        <p><strong>Address:</strong> {{ customer['address']['fullAddress'] }}</p>
        
        <h2>Repair Orders</h2>
        <ul>
            {% for order in repair_orders %}
                <li>
                    <strong>Order #{{ order['repairOrderNumber'] }}:</strong> {{ order['repairOrderStatus']['name'] }}<br>
                    Amount Paid: {{ order['amountPaid'] }}<br>
                    Labor Sales: {{ order['laborSales'] }}<br>
                    Parts Sales: {{ order['partsSales'] }}<br>
                    Sublet Sales: {{ order['subletSales'] }}<br>
                    Fees: {{ order['feeTotal'] }}<br>
                    Discounts: {{ order['discountTotal'] }}<br>
                    Total Sales: {{ order['totalSales'] }}<br>
                    Jobs:
                    <ul>
                        {% for job in order['jobs'] %}
                            <li>{{ job['name'] }} - {{ job['note'] }}</li>
                        {% endfor %}
                    </ul>
                    Customer Concerns:
                    <ul>
                        {% for concern in order['customerConcerns'] %}
                            <li>{{ concern['concern'] }}</li>
                        {% endfor %}
                    </ul>
                </li>
            {% endfor %}
        </ul>
    </div>
</body>
</html>
'''

def get_access_token():
    auth_header = f'{CLIENT_ID}:{CLIENT_SECRET}'.encode('ascii')
    base64_bytes = base64.b64encode(auth_header)
    base64_auth = base64_bytes.decode('ascii')

    headers = {
        'Authorization': f'Basic {base64_auth}',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
    }
    data = {
        'grant_type': 'client_credentials'
    }

    logging.debug(f'Authorization Header: Basic {base64_auth}')
    response = requests.post(TOKEN_URL, headers=headers, data=data)
    logging.debug(f'Token response: {response.text}')

    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        logging.error('Failed to obtain access token')
        return None

def get_customer_details(access_token, customer_id):
    customer_details_url = f'{TEKMETRIC_API_URL}/customers/{customer_id}?shop={SHOP_ID}'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    customer_response = requests.get(customer_details_url, headers=headers)
    logging.debug(f'Customer details response: {customer_response.text}')
    
    if customer_response.status_code == 200:
        return customer_response.json()
    else:
        return None

def get_vehicle_details(access_token, vehicle_id):
    vehicle_details_url = f'{TEKMETRIC_API_URL}/vehicles/{vehicle_id}?shop={SHOP_ID}'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    vehicle_response = requests.get(vehicle_details_url, headers=headers)
    logging.debug(f'Vehicle details response: {vehicle_response.text}')
    
    if vehicle_response.status_code == 200:
        return vehicle_response.json()
    else:
        return None

@app.route('/')
def index():
    default_date = datetime.today().strftime('%Y-%m-%d')
    return render_template_string(form_template, default_start_date=default_date, default_end_date=default_date)

@app.route('/search_customer', methods=['POST'])
def search_customer():
    customer_name = request.form.get('customerName')

    # Get access token
    access_token = get_access_token()
    if not access_token:
        return jsonify({"error": "Failed to obtain access token"}), 500
    
    # Split the customer name into potential first and last names
    name_parts = customer_name.split()
    
    def search_customer(query):
        customer_search_url = f'{TEKMETRIC_API_URL}/customers?shop={SHOP_ID}&search={query}&page=0&size=100'
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        response = requests.get(customer_search_url, headers=headers)
        logging.debug(f'Customer search response for {query}: {response.text}')
        if response.status_code == 200:
            return response.json().get('content', [])
        else:
            return []

    def match_score(customer_name, query):
        return SequenceMatcher(None, customer_name.lower(), query.lower()).ratio()

    customers = []
    if len(name_parts) == 2:
        first_name, last_name = name_parts
        customers = search_customer(first_name) + search_customer(last_name)
    else:
        customers = search_customer(customer_name)

    # Deduplicate customers based on ID
    seen_ids = set()
    unique_customers = []
    for customer in customers:
        if customer['id'] not in seen_ids:
            seen_ids.add(customer['id'])
            unique_customers.append(customer)

    # Sort customers based on match score
    unique_customers.sort(key=lambda x: max(match_score(x['firstName'], customer_name), match_score(x['lastName'], customer_name)), reverse=True)
    
    # Extract customer details and their vehicles
    for customer in unique_customers:
        customer['vehicles'] = get_customer_vehicles(access_token, customer['id'])

    return render_template_string(form_template, customers=unique_customers)

@app.route('/search_vehicle', methods=['POST'])
def search_vehicle():
    vehicle_make = request.form.get('vehicleMake', '')
    vehicle_model = request.form.get('vehicleModel', '')
    vehicle_year = request.form.get('vehicleYear', '')
    vehicle_color = request.form.get('vehicleColor', '')

    # Get access token
    access_token = get_access_token()
    if not access_token:
        return jsonify({"error": "Failed to obtain access token"}), 500
    
    # Construct search query
    search_query = f'{vehicle_year} {vehicle_make} {vehicle_model} {vehicle_color}'.strip()
    
    vehicle_search_url = f'{TEKMETRIC_API_URL}/vehicles?shop={SHOP_ID}&search={search_query}&page=0&size=25'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(vehicle_search_url, headers=headers)
    logging.debug(f'Vehicle search response for {search_query}: {response.text}')
    if response.status_code == 200:
        vehicles = response.json().get('content', [])
    else:
        vehicles = []

    return render_template_string(form_template, vehicles=vehicles)

@app.route('/search_appointments', methods=['POST'])
def search_appointments():
    start_date = request.form.get('startDate', '')
    end_date = request.form.get('endDate', '')

    # Use current date as default if no dates are provided
    if not start_date and not end_date:
        start_date = datetime.today().strftime('%Y-%m-%d')
        end_date = start_date
    elif start_date and not end_date:
        end_date = start_date
    elif not start_date and end_date:
        start_date = end_date

    # Convert date to ISO format with timezone for API compatibility
    start_date_iso = f"{start_date}T00:00:00Z"
    end_date_iso = f"{end_date}T23:59:59Z"

    # Get access token
    access_token = get_access_token()
    if not access_token:
        return jsonify({"error": "Failed to obtain access token"}), 500

    appointments_url = f'{TEKMETRIC_API_URL}/appointments?shop={SHOP_ID}&start={start_date_iso}&end={end_date_iso}'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(appointments_url, headers=headers)
    logging.debug(f'Appointments search response for {start_date} to {end_date}: {response.text}')
    if response.status_code == 200:
        appointments = response.json().get('content', [])
    else:
        appointments = []

    # Add customer names and vehicle info to appointments
    for appointment in appointments:
        customer = get_customer_details(access_token, appointment['customerId'])
        vehicle = get_vehicle_details(access_token, appointment['vehicleId'])
        appointment['customerName'] = f"{customer['firstName']} {customer['lastName']}" if customer else "Unknown Customer"
        appointment['vehicleInfo'] = f"{vehicle['year']} {vehicle['make']} {vehicle['model']}" if vehicle else "Unknown Vehicle"
        appointment['vehicleVin'] = vehicle['vin'] if vehicle else "Unknown VIN"

    return render_template_string(form_template, appointments=appointments)

@app.route('/appointment/<int:appointment_id>')
def appointment(appointment_id):
    access_token = get_access_token()
    if not access_token:
        return jsonify({"error": "Failed to obtain access token"}), 500

    appointment_details_url = f'{TEKMETRIC_API_URL}/appointments/{appointment_id}?shop={SHOP_ID}'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    appointment_response = requests.get(appointment_details_url, headers=headers)
    logging.debug(f'Appointment details response: {appointment_response.text}')

    if appointment_response.status_code != 200:
        return jsonify({"error": "Failed to retrieve appointment details"}), appointment_response.status_code

    appointment = appointment_response.json()

    customer = get_customer_details(access_token, appointment['customerId'])
    vehicle = get_vehicle_details(access_token, appointment['vehicleId'])
    appointment['customerName'] = f"{customer['firstName']} {customer['lastName']}" if customer else "Unknown Customer"
    appointment['vehicleInfo'] = f"{vehicle['year']} {vehicle['make']} {vehicle['model']}" if vehicle else "Unknown Vehicle"
    appointment['vehicleVin'] = vehicle['vin'] if vehicle else "Unknown VIN"

    return render_template_string(appointment_profile_template, appointment=appointment)

def get_customer_vehicles(access_token, customer_id):
    customer_vehicles_url = f'{TEKMETRIC_API_URL}/vehicles?shop={SHOP_ID}&customerId={customer_id}'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(customer_vehicles_url, headers=headers)
    logging.debug(f'Customer vehicles response: {response.text}')
    if response.status_code == 200:
        return response.json().get('content', [])
    else:
        return []

@app.route('/profile/<int:customer_id>')
def profile(customer_id):
    access_token = get_access_token()
    if not access_token:
        return jsonify({"error": "Failed to obtain access token"}), 500

    customer_details_url = f'{TEKMETRIC_API_URL}/customers/{customer_id}?shop={SHOP_ID}'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    customer_response = requests.get(customer_details_url, headers=headers)
    logging.debug(f'Customer details response: {customer_response.text}')

    if customer_response.status_code != 200:
        return jsonify({"error": "Failed to retrieve customer details"}), customer_response.status_code

    customer = customer_response.json()

    vehicles = get_customer_vehicles(access_token, customer_id)

    service_dates_url = f'{TEKMETRIC_API_URL}/appointments?shop={SHOP_ID}&customerId={customer_id}'
    appointments_response = requests.get(service_dates_url, headers=headers)
    logging.debug(f'Service dates response: {appointments_response.text}')
    appointments = appointments_response.json().get('content', []) if appointments_response.status_code == 200 else []

    repair_orders_url = f'{TEKMETRIC_API_URL}/repair-orders?shop={SHOP_ID}&customerId={customer_id}'
    repair_orders_response = requests.get(repair_orders_url, headers=headers)
    logging.debug(f'Repair orders response: {repair_orders_response.text}')
    repair_orders = repair_orders_response.json().get('content', []) if repair_orders_response.status_code == 200 else []

    return render_template_string(profile_template, customer=customer, vehicles=vehicles, appointments=appointments, repair_orders=repair_orders)

@app.route('/vehicle_profile/<int:vehicle_id>')
def vehicle_profile(vehicle_id):
    access_token = get_access_token()
    if not access_token:
        return jsonify({"error": "Failed to obtain access token"}), 500

    vehicle_details_url = f'{TEKMETRIC_API_URL}/vehicles/{vehicle_id}?shop={SHOP_ID}'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    vehicle_response = requests.get(vehicle_details_url, headers=headers)
    logging.debug(f'Vehicle details response: {vehicle_response.text}')

    if vehicle_response.status_code != 200:
        return jsonify({"error": "Failed to retrieve vehicle details"}), vehicle_response.status_code

    vehicle = vehicle_response.json()

    customer_details_url = f'{TEKMETRIC_API_URL}/customers/{vehicle["customerId"]}?shop={SHOP_ID}'
    customer_response = requests.get(customer_details_url, headers=headers)
    logging.debug(f'Customer details response: {customer_response.text}')
    if customer_response.status_code != 200:
        return jsonify({"error": "Failed to retrieve customer details"}), customer_response.status_code

    customer = customer_response.json() if customer_response.status_code == 200 else None

    repair_orders_url = f'{TEKMETRIC_API_URL}/repair-orders?shop={SHOP_ID}&vehicleId={vehicle_id}'
    repair_orders_response = requests.get(repair_orders_url, headers=headers)
    logging.debug(f'Repair orders response: {repair_orders_response.text}')
    repair_orders = repair_orders_response.json().get('content', []) if repair_orders_response.status_code == 200 else []

    return render_template_string(vehicle_profile_template, vehicle=vehicle, customer=customer, repair_orders=repair_orders)

if __name__ == '__main__':
    app.run(debug=True)
