const axios = require('axios');
require('dotenv').config();

const apiUrl = process.env.TEKMETRIC_API_URL;
const authToken = process.env.TEKMETRIC_API_KEY; // Use the actual token

async function testAppointments() {
    try {
        const response = await axios.get(`${apiUrl}/appointments`, {
            headers: {
                'Authorization': `Bearer ${authToken}`,
                'Content-Type': 'application/json'
            },
            params: { shop: 238 }
        });
        console.log('Appointments:', response.data);
    } catch (error) {
        console.error('Error fetching appointments:', error.response ? error.response.data : error.message);
    }
}

testAppointments();
