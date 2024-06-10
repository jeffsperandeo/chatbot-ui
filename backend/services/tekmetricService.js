const axios = require('axios');
require('dotenv').config();

const apiUrl = process.env.TEKMETRIC_API_URL;

const tekmetricsApi = axios.create({
    baseURL: apiUrl,
    headers: {
        'Content-Type': 'application/json'
    }
});

async function getCustomerDetails(query) {
    try {
        const response = await tekmetricsApi.get('/customers', {
            params: {
                shop: 238,
                search: query,
                page: 0,
                size: 100
            }
        });
        console.log(`Raw response from Tekmetric API: ${JSON.stringify(response.data, null, 2)}`);
        return response.data.content;
    } catch (error) {
        console.error('Error fetching customer details:', error.message);
        throw error;
    }
}

async function createNewVehicle(vehicleData) {
    try {
        const response = await tekmetricsApi.post('/vehicles', vehicleData);
        console.log(`Vehicle created: ${JSON.stringify(response.data, null, 2)}`);
        return response.data;
    } catch (error) {
        console.error('Error creating vehicle:', error.message);
        throw error;
    }
}

async function listAppointments(authToken) {
    try {
        console.log('Using authToken:', authToken); // Add this line
        const response = await tekmetricsApi.get('/appointments', {
            headers: { 'Authorization': `Bearer ${authToken}` },
            params: { shop: 238 }
        });
        console.log(`Appointments response: ${JSON.stringify(response.data, null, 2)}`); // Add this line
        return response.data;
    } catch (error) {
        console.error('Error fetching appointments:', error.message); // Add this line
        console.error('Error details:', error.response ? error.response.data : error.message); // Add this line
        throw error;
    }
}

module.exports = { getCustomerDetails, createNewVehicle, listAppointments };
