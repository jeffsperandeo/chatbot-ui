const {
    listRepairOrders,
    updateRepairOrder,
    listAppointments,
    listVehicles,
    // Add more service functions as needed
} = require('./tekmetricService');

async function commandHandler(parsedCommand) {
    const { action, details } = parsedCommand;

    try {
        switch (action) {
            case 'listRepairOrders':
                return await listRepairOrders();
            case 'updateRepairOrder':
                return await updateRepairOrder(details);
            case 'listAppointments':
                return await listAppointments();
            case 'listVehicles':
                return await listVehicles();
            // Add more cases as needed
            default:
                return { error: `Unknown action: ${action}` };
        }
    } catch (error) {
        console.error(`Error processing command "${action}":`, error.message);
        return { error: `Error processing command "${action}": ${error.message}` };
    }
}

module.exports = { commandHandler };
