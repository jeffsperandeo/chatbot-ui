import requests
import json

# Configuration
BASE_URL = 'http://localhost:3002'
AUTH_URL = f'{BASE_URL}/api/auth/token'
APPOINTMENTS_URL = f'{BASE_URL}/api/appointments'
AUTH_HEADER = 'Authorization'
TOKEN_STORAGE_FILE = 'auth_token.json'

# Function to authenticate and store the token
def authenticate():
    try:
        response = requests.post(AUTH_URL, data={
            'grant_type': 'client_credentials'
        }, headers={
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Basic UlQ4WUpta1FCcXFRLVJuWDpzaGQ1U2xmcjFkdWNFbkJFcW1oUk5tYlo='
        })
        response.raise_for_status()
        token = response.json().get('token')
        print(f'Token retrieved from authentication: {token}')
        store_token(token)
        return token
    except requests.RequestException as e:
        print(f'Error during authentication: {e}')
        raise

# Function to store the token in a file (simulating local storage)
def store_token(token):
    with open(TOKEN_STORAGE_FILE, 'w') as f:
        json.dump({'authToken': token}, f)
    print(f'Token stored in {TOKEN_STORAGE_FILE}')

# Function to retrieve the token from the file
def retrieve_token():
    try:
        with open(TOKEN_STORAGE_FILE, 'r') as f:
            data = json.load(f)
            token = data.get('authToken')
            print(f'Token retrieved from storage: {token}')
            return token
    except FileNotFoundError:
        print(f'No token found in {TOKEN_STORAGE_FILE}')
        return None

# Function to make a request with the token
def fetch_appointments(token):
    try:
        response = requests.get(APPOINTMENTS_URL, headers={
            AUTH_HEADER: f'Bearer {token}'
        })
        response.raise_for_status()
        print(f'Appointments: {response.json()}')
    except requests.RequestException as e:
        print(f'Error fetching appointments: {e}')
        raise

# Main function to run the test
def main():
    # Authenticate and store the token
    token = authenticate()

    # Retrieve the token from storage
    retrieved_token = retrieve_token()

    # Fetch appointments with the retrieved token
    if retrieved_token:
        fetch_appointments(retrieved_token)
    else:
        print('No valid token found to fetch appointments.')

if __name__ == '__main__':
    main()
