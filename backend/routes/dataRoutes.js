// backend/routes/dataRoutes.js
const express = require('express');
const { getCustomer, createNewVehicle, getVehicleDetails, listAppointments } = require('../controllers/dataController');

const router = express.Router();

router.get('/customer-details', getCustomer);
router.post('/vehicles', createNewVehicle);
router.get('/vehicle-details', getVehicleDetails);
router.get('/appointments', async (req, res) => {
    try {
        await listAppointments(req, res);
    } catch (error) {
        console.error('Error fetching appointments:', error.message);
        res.status(500).json({ error: error.message });
    }
});

module.exports = router;
