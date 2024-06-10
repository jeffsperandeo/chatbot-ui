// backend/services/tekmetricService.js
const axios = require('axios');
require('dotenv').config();

const apiUrl = process.env.TEKMETRIC_API_URL;
const apiKey = process.env.TEKMETRIC_API_KEY;

const tekmetricsApi = axios.create({
    baseURL: apiUrl,
    headers: {
        'Authorization': `Bearer ${apiKey}`,
        'Content-Type': 'application/json'
    }
});

async function searchCustomer(query) {
    try {
        const response = await tekmetricsApi.get('/customers', {
            params: {
                shop: 238,
                search: query,
                page: 0,
                size: 100
            }
        });
        console.log('Response from /customers endpoint:', response.data);
        return response.data;
    } catch (error) {
        console.error('Error searching customer:', error);
        throw error;
    }
}

async function createVehicle(vehicleData) {
    try {
        const response = await tekmetricsApi.post('/vehicles', vehicleData);
        console.log('Response from /vehicles endpoint:', response.data);
        return response.data;
    } catch (error) {
        console.error('Error creating vehicle:', error);
        throw error;
    }
}

async function fetchAppointments() {
    try {
        const response = await tekmetricsApi.get('/appointments', {
            params: {
                shop: 238,
                page: 0,
                size: 100
            }
        });
        console.log('Response from /appointments endpoint:', response.data);
        return response.data;
    } catch (error) {
        console.error('Error fetching appointments:', error);
        throw error;
    }
}

module.exports = { tekmetricsApi, searchCustomer, createVehicle, fetchAppointments };
