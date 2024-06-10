// backend/routes/commandRoutes.js
const express = require('express');
const { handleUserInput } = require('../services/chatService');
const router = express.Router();

router.post('/execute', async (req, res) => {
    try {
        const { input, userId, authToken } = req.body;
        const result = await handleUserInput(input, userId);
        res.json(result);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

module.exports = router;
