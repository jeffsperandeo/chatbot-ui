// backend/controllers/dataController.js
const { searchCustomer, createVehicle, searchVehicleByVin, listAppointments: fetchAppointments } = require('../services/tekmetricService');
const { getContext } = require('../utils/redisClient'); // Import Redis client

async function getCustomer(req, res) {
    let { search } = req.query;
    try {
        const data = await searchCustomer(search);
        res.status(200).json(data);
    } catch (error) {
        console.error('Error retrieving customer data:', error);
        res.status(500).send('Error retrieving customer data');
    }
}

async function createNewVehicle(req, res) {
    const vehicleData = req.body;
    try {
        const response = await createVehicle(vehicleData);
        res.status(201).json(response);
    } catch (error) {
        console.error('Error creating vehicle:', error);
        res.status(500).send('Error creating vehicle');
    }
}

async function getVehicleDetails(req, res) {
    const { vin } = req.query;
    try {
        const vehicles = await searchVehicleByVin(vin);
        if (vehicles && vehicles.length > 0) {
            res.status(200).json(vehicles[0]);
        } else {
            res.status(404).send('Vehicle not found');
        }
    } catch (error) {
        console.error('Error retrieving vehicle details:', error);
        res.status(500).send('Error retrieving vehicle details');
    }
}

async function listAppointments(req, res) {
    console.log('Fetching appointments...'); // Add this line
    try {
        const authToken = await getContext('authToken'); // Retrieve token from Redis
        console.log('Using authToken:', authToken); // Add this line
        const appointments = await fetchAppointments(authToken);
        console.log('Appointments fetched:', appointments); // Add this line
        res.status(200).json(appointments);
    } catch (error) {
        console.error('Error retrieving appointments:', error); // Add this line
        res.status(500).send('Error retrieving appointments');
    }
}

module.exports = { getCustomer, createNewVehicle, getVehicleDetails, listAppointments };
