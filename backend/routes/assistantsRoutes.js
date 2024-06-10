// backend/routes/assistantsRoutes.js
const express = require('express');
const { getCustomerDetails } = require('../services/assistantsService'); // Ensure this function is correctly imported and defined
const { handleAssistantQuery } = require('../controllers/assistantsController'); // Correct path

const router = express.Router();

router.get('/customer-details', async (req, res) => {
    const { name } = req.query;
    try {
        const customer = await getCustomerDetails(name); // Ensure this function is correctly imported and defined
        if (customer) {
            res.status(200).json(customer);
        } else {
            res.status(404).json({ error: 'Customer not found' });
        }
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

router.post('/assistant-query', handleAssistantQuery);

module.exports = router;
