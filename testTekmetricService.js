// tests/testtekmetricservice.js
const { searchCustomerByName } = require('../backend/services/tekmetricService');

async function test() {
    try {
        const result = await searchCustomerByName('Jeff Sperandeo');
        console.log('Result:', JSON.stringify(result, null, 2));
    } catch (error) {
        console.error('Error:', error.message);
    }
}

test();
