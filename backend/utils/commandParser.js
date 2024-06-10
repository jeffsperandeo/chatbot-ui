// backend/utils/commandParser.js
function parseCommand(input) {
    const commandMappings = {
        "Get vehicle details for VIN": "GET /tekmetrics/vehicles",
        "Add a new vehicle with details": "POST /tekmetrics/vehicles",
        "Update vehicle with ID": "PATCH /tekmetrics/vehicles/{id}",
        "List all jobs in the shop": "GET /tekmetrics/jobs",
        "Change status of job ID": "PATCH /tekmetrics/jobs/{id}",
        "Get customer details for ID": "GET /tekmetrics/customers",
        "What are my appointments today?": "GET /tekmetrics/appointments"
    };

    for (const [command, endpoint] of Object.entries(commandMappings)) {
        if (input.startsWith(command)) {
            console.log(`Command recognized: ${command}`); // Add this line
            return { command, endpoint, details: input.replace(command, '').trim() };
        }
    }

    console.log(`Command not recognized: ${input}`); // Add this line
    return null;
}

module.exports = { parseCommand };
