// backend/server.js
const express = require('express');
const bodyParser = require('body-parser');
const { createProxyMiddleware } = require('http-proxy-middleware');
const authRoutes = require('./routes/authRoutes'); // Ensure this path is correct
const dataRoutes = require('./routes/dataRoutes');
const assistantsRoutes = require('./routes/assistantsRoutes');
const chatRoutes = require('./routes/chatRoutes');
const commandRoutes = require('./routes/commandRoutes');
const { storeContext, getContext } = require('./utils/redisClient');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3002;

app.use(bodyParser.json());
app.use('/api/auth', authRoutes); // Ensure this line exists and points to authRoutes
app.use('/api', dataRoutes); // Ensure this line exists and points to dataRoutes
app.use('/assistants', assistantsRoutes);
app.use('/chat', chatRoutes);
app.use('/command', commandRoutes);

// Proxy for FastAPI backend
app.use('/chatfusion', createProxyMiddleware({
    target: 'http://localhost:8000',
    changeOrigin: true,
}));

// Redis context management routes
app.post('/store-context', async (req, res) => {
    const { userId, context } = req.body;
    try {
        await storeContext(userId, context);
        res.status(200).send('Context stored successfully');
    } catch (err) {
        res.status(500).send('Error storing context');
    }
});

app.get('/get-context/:userId', async (req, res) => {
    const userId = req.params.userId;
    try {
        const context = await getContext(userId);
        res.status(200).json(context);
    } catch (err) {
        res.status(500).send('Error retrieving context');
    }
});

// Test route for checking Redis storage
app.post('/test-store-context', async (req, res) => {
    const { userId, context } = req.body;
    try {
        await storeContext(userId, context);
        res.status(200).send('Context stored successfully');
    } catch (err) {
        res.status(500).send('Error storing context');
    }
});

// Test route for checking Redis retrieval
app.get('/test-get-context/:userId', async (req, res) => {
    const userId = req.params.userId;
    try {
        const context = await getContext(userId);
        res.status(200).json(context);
    } catch (err) {
        res.status(500).send('Error retrieving context');
    }
});

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
