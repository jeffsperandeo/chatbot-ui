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

async function storeContext(key, value) {
    try {
        await client.set(key, value);
        console.log('Context stored successfully:', key, value);
    } catch (err) {
        console.error('Error storing context:', key, err);
    }
}

async function getContext(key) {
    try {
        const value = await client.get(key);
        console.log('Context retrieved successfully:', key, value);
        return value;
    } catch (err) {
        console.error('Error retrieving context:', key, err);
    }
}

module.exports = { storeContext, getContext };
