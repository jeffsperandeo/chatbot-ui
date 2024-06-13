// backend/utils/axiosConfig.js
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

module.exports = tekmetricsApi;
