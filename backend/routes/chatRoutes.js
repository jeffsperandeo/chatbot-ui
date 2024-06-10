// backend/routes/chatRoutes.js
const express = require('express');
const { handleUserInput } = require('../utils/chatHandler');
const { getContext } = require('../utils/redisClient'); // Import Redis client
const router = express.Router();

router.post('/message', async (req, res) => {
    try {
        const { message, userId } = req.body; // Ensure authToken is included in the request body
        const token = await getContext('authToken'); // Retrieve token from Redis
        if (!token) {
            throw new Error('No authentication token found.');
        }
        const response = await handleUserInput(message, userId, token); // Pass authToken to handleUserInput
        res.status(200).json(response);
    } catch (error) {
        console.error('Error handling chat message:', error.message);
        res.status(500).json({ error: error.message });
    }
});

module.exports = router;
