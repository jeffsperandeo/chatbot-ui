// backend/utils/axiosConfig.js
const axios = require('axios');
require('dotenv').config();

const apiUrl = 'http://127.0.0.1:5000'; // Flask app URL

const tekmetricsApi = axios.create({
    baseURL: apiUrl,
    headers: {
        'Content-Type': 'application/json'
    }
});

module.exports = tekmetricsApi;
