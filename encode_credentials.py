import base64

client_id = 'your_client_id'
client_secret = 'your_client_secret'

credentials = f"{client_id}:{client_secret}"
encoded_credentials = base64.b64encode(credentials.encode()).decode()

print(f"Encoded Credentials: {encoded_credentials}")
