// backend/services/chatService.js

const { parseCommand } = require('../utils/commandParser');
const {
    searchVehicleByVin,
    addNewVehicle,
    updateVehicle,
    listJobs,
    updateJobStatus,
    getCustomerDetails,
    searchCustomerByName,
    listAppointments
} = require('../services/tekmetricService');

async function handleUserInput(input, userId) {
    const parsedCommand = parseCommand(input);
    if (!parsedCommand) {
        console.error('Command not recognized:', input);
        return "Command not recognized.";
    }

    const { command, action, details } = parsedCommand;
    console.log(`Processing command: ${command} with details: ${details}`);

    try {
        let response;
        switch (action) {
            case "getVehicleDetails":
                response = await searchVehicleByVin(details);
                break;
            case "createVehicle":
                response = await addNewVehicle(JSON.parse(details));
                break;
            case "updateVehicle":
                response = await updateVehicle(details);
                break;
            case "listJobs":
                response = await listJobs();
                break;
            case "updateJob":
                response = await updateJobStatus(details);
                break;
            case "getCustomerDetails":
                response = await getCustomerDetails(details);
                break;
            case "searchCustomerByName":
                response = await searchCustomerByName(details);
                break;
            case "listAppointments":
                response = await listAppointments();
                break;
            default:
                console.error('Action not recognized:', action);
                response = "Action not recognized.";
        }

        // Ensure response is plain text or JSON
        if (typeof response !== 'string') {
            response = JSON.stringify(response, null, 2);
        }

        console.log(`Response: ${response}`);
        return response;
    } catch (error) {
        console.error(`Error processing command "${command}":`, error.message);
        return `Error processing command "${command}": ${error.message}`;
    }
}

module.exports = { handleUserInput };
