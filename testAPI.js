const axios = require('./backend/utils/axiosConfig'); // Adjust path if needed

async function testConnection() {
    console.log('Starting API Connection Test...');
    try {
        const response = await axios.get('/customers', { params: { shop: 238, search: 'Jeff', page: 0, size: 100 } });
        console.log('API Connection Test Successful:', response.data);
    } catch (error) {
        console.error('API Connection Test Failed:', error.response ? error.response.data : error.message);
    }
    console.log('API Connection Test Completed.');
}

testConnection();
