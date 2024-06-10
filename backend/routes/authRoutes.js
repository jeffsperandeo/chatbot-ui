const express = require('express');
const axios = require('axios');
const { storeContext } = require('../utils/redisClient'); // Import Redis client

const router = express.Router();

const client_id = process.env.TEKMETRICS_CLIENT_ID;
const client_secret = process.env.TEKMETRICS_CLIENT_SECRET;
const encoded_credentials = Buffer.from(`${client_id}:${client_secret}`).toString('base64');

router.post('/token', async (req, res) => {
    try {
        console.log('Requesting OAuth token with credentials:', encoded_credentials);
        const response = await axios.post('https://sandbox.tekmetric.com/api/v1/oauth/token',
            new URLSearchParams({
                grant_type: 'client_credentials'
            }),
            {
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Authorization': `Basic ${encoded_credentials}`
                }
            }
        );
        const token = response.data.access_token;
        const scope = response.data.scope;
        console.log('Token retrieved from Tekmetric API:', token);
        console.log('Token scope:', scope); // Log the scope of the token
        // Store the token in Redis
        await storeContext('authToken', token);
        console.log('Token stored in Redis:', token); // Add this line
        res.json({ token });
    } catch (error) {
        console.error('Error fetching OAuth token:', error.response ? error.response.data : error.message);
        res.status(error.response ? error.response.status : 500).send(error.response ? error.response.data : 'Error fetching OAuth token');
    }
});

module.exports = router;
