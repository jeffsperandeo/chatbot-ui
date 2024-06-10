// backend/utils/redisClient.js
const redis = require('redis');
require('dotenv').config();

const client = redis.createClient({
    url: process.env.REDIS_URL
});

client.on('error', (err) => console.log('Redis Client Error', err));

client.connect().then(() => {
    console.log('Connected to Redis');
}).catch(err => {
    console.error('Error connecting to Redis', err);
});

async function storeContext(userId, context) {
    try {
        await client.hSet(`user:${userId}:context`, JSON.stringify(context)); // Convert context to a string
        console.log('Context stored successfully for user:', userId);
    } catch (err) {
        console.error('Error storing context for user:', userId, err);
    }
}

async function getContext(userId) {
    try {
        const context = await client.hGetAll(`user:${userId}:context`);
        console.log('Context retrieved successfully for user:', userId, context);
        return context;
    } catch (err) {
        console.error('Error retrieving context for user:', userId, err);
    }
}

module.exports = { storeContext, getContext };
