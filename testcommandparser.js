// testCommandParser.js
const { parseCommand } = require('./backend/utils/commandParser');

const testInputs = [
    "Get vehicle details for VIN WBA5R1C53KAK07369",
    "Add a new vehicle with details {\"make\":\"Toyota\",\"model\":\"Camry\"}",
    "Update vehicle with ID 12345",
    "List all jobs in the shop",
    "Change status of job ID 67890 to completed",
    "Get customer details for Jeff Sperandeo",
    "What are my appointments today?"
];

testInputs.forEach(input => {
    const parsed = parseCommand(input);
    console.log(`Input: "${input}"`);
    console.log("Parsed:", parsed);
});
