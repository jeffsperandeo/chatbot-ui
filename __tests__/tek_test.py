import requests

def query_assistant(user_id, message):
    url = 'http://localhost:3002/assistants/assistant-query'  # Ensure this URL is correct
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'userId': user_id,
        'message': message
    }

    response = requests.post(url, json=data)
    if response.status_code == 200:
        try:
            return response.json()
        except requests.exceptions.JSONDecodeError:
            return {'error': 'Invalid JSON response'}
    else:
        return {'error': response.text}

# Example usage
user_id = 'user123'
message = 'Get vehicle details for VIN 1HGBH41JXMN109186'

response = query_assistant(user_id, message)
print(response)
