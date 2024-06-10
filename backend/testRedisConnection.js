// testRedisConnections.js
const redis = require('redis');
require('dotenv').config();

const client = redis.createClient({
    url: process.env.REDIS_URL
});

client.on('error', (err) => console.log('Redis Client Error', err));

client.connect().then(async () => {
    console.log('Connected to Redis server');

    try {
        // Set a key
        await client.set('test_key', 'Hello, Redis!');
        console.log('Key set: test_key');

        // Get the key
        const value = await client.get('test_key');
        console.log('Key retrieved: test_key ->', value);

        // Check if key exists
        const exists = await client.exists('test_key');
        console.log('Key exists:', exists ? 'Yes' : 'No');

        // Delete the key
        await client.del('test_key');
        console.log('Key deleted: test_key');

        // Check if key exists after deletion
        const existsAfterDeletion = await client.exists('test_key');
        console.log('Key exists after deletion:', existsAfterDeletion ? 'Yes' : 'No');
    } catch (error) {
        console.error('Error interacting with Redis:', error);
    } finally {
        client.quit();
    }
});
