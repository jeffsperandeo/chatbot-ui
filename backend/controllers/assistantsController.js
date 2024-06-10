const { handleUserInput } = require('../services/chatService'); // Correct path

async function handleAssistantQuery(req, res) {
    try {
        const { message } = req.body;
        const response = await handleUserInput(message);
        res.status(200).json(response);
    } catch (error) {
        console.error('Error handling assistant query:', error.message);
        res.status(500).json({ error: error.message });
    }
}

module.exports = { handleAssistantQuery };
