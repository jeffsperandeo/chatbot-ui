const axios = require('../utils/axiosConfig'); // Ensure this path is correct

async function getCustomerDetails(customerName) {
    try {
        const response = await axios.get('/customers', {
            params: {
                shop: 238,
                search: customerName,
                page: 0,
                size: 100
            }
        });
        console.log('Response from /customers endpoint:', response.data);
        const customers = response.data.content;
        const customer = customers.find(c => c.firstName === 'Jeff' && c.lastName === 'Sperandeo');
        return customer;
    } catch (error) {
        console.error('Error fetching customer details:', error.message);
        throw error;
    }
}

module.exports = { getCustomerDetails };
