const { searchCustomer, createVehicle, tekmetricsApi } = require('../services/tekmetricService');
const { parseCommand } = require('./commandParser');

async function handleUserInput(input, userId, authToken) {
    const parsedCommand = parseCommand(input);

    if (parsedCommand) {
        const { command, endpoint, details } = parsedCommand;
        console.log(`Parsed command: ${command}, Endpoint: ${endpoint}, Details: ${details}`);

        switch (command) {
            case "Get vehicle details for VIN":
                return await getVehicleDetails(details, authToken);
            case "Add a new vehicle with details":
                return await addNewVehicle(details, authToken);
            case "Update vehicle with ID":
                return await updateVehicle(details, authToken);
            case "List all jobs in the shop":
                return await listJobs(authToken);
            case "Change status of job ID":
                return await updateJobStatus(details, authToken);
            case "Get customer details for ID":
                return await getCustomerDetails(details, authToken);
            case "What are my appointments today?":
                return await listAppointments(authToken);
            default:
                return "Command not recognized.";
        }
    } else {
        return "I'm sorry, I don't understand that command.";
    }
}

// Define API call functions
async function getVehicleDetails(vin, authToken) {
    try {
        const response = await tekmetricsApi.get('/vehicles', {
            params: { vin },
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        return response.data;
    } catch (error) {
        return `Error fetching vehicle details: ${error.message}`;
    }
}

async function addNewVehicle(details, authToken) {
    try {
        const response = await tekmetricsApi.post('/vehicles', details, {
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        return response.data;
    } catch (error) {
        return `Error adding new vehicle: ${error.message}`;
    }
}

async function updateVehicle(details, authToken) {
    const [id, ...restDetails] = details.split(' ');
    const updateDetails = restDetails.join(' ');
    try {
        const response = await tekmetricsApi.patch(`/vehicles/${id}`, { updateDetails }, {
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        return response.data;
    } catch (error) {
        return `Error updating vehicle: ${error.message}`;
    }
}

async function listJobs(authToken) {
    try {
        const response = await tekmetricsApi.get('/jobs', {
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        return response.data;
    } catch (error) {
        return `Error listing jobs: ${error.message}`;
    }
}

async function updateJobStatus(details, authToken) {
    const [id, ...restDetails] = details.split(' ');
    const status = restDetails.join(' ');
    try {
        const response = await tekmetricsApi.patch(`/jobs/${id}`, { status }, {
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        return response.data;
    } catch (error) {
        return `Error updating job status: ${error.message}`;
    }
}

async function getCustomerDetails(id, authToken) {
    try {
        const response = await tekmetricsApi.get(`/customers/${id}`, {
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        return response.data;
    } catch (error) {
        return `Error fetching customer details: ${error.message}`;
    }
}

async function listAppointments(authToken) {
    try {
        const response = await tekmetricsApi.get('/appointments', {
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        return response.data;
    } catch (error) {
        return `Error listing appointments: ${error.message}`;
    }
}

module.exports = { handleUserInput };
