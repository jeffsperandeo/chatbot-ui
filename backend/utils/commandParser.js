// backend/utils/commandParser.js
function parseCommand(input) {
    const commandRegex = /^(Get vehicle details for VIN|Add a new vehicle with details|Update vehicle with ID|List all jobs in the shop|Change status of job ID|Get customer details for ID|What are my appointments today?) (.+)$/;
    const match = input.match(commandRegex);

    if (match) {
        return {
            command: match[1],
            details: match[2]
        };
    }
    return null;
}

module.exports = { parseCommand };
