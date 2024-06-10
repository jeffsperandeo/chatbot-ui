const axios = require('axios');

async function testGetVehicleDetails() {
    const url = 'http://localhost:3002/chat/message';
    const message = 'Get vehicle details for VIN 3KPF24AD2ME331480';
    const userId = 'your_user_id'; // Replace with your actual user ID
    const authToken = 'your_auth_token'; // Replace with your actual auth token

    try {
        const response = await axios.post(url, {
            message,
            userId,
            authToken
        });
        console.log('Response:', response.data);
    } catch (error) {
        console.error('Error:', error.message);
    }
}

testGetVehicleDetails();
