const express = require('express');
const { handleUserInput } = require('../utils/chatHandler');
const router = express.Router();

router.post('/message', async (req, res) => {
    try {
        const { message, userId, authToken } = req.body; // Ensure authToken is included in the request body
        const response = await handleUserInput(message, userId, authToken); // Pass authToken to handleUserInput
        res.status(200).json(response);
    } catch (error) {
        console.error('Error handling chat message:', error.message);
        res.status(500).json({ error: error.message });
    }
});

module.exports = router;
