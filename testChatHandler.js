const { handleUserInput } = require('./backend/utils/chatHandler');

async function test() {
    const commands = [
        'Get vehicle details for VIN 12345',
        'Add a new vehicle with details {"make": "Toyota", "model": "Camry", "year": 2020}',
        'Update vehicle with ID 1 to color red',
        'List all jobs in the shop',
        'Change status of job ID 2 to completed',
        'Get customer details for ID 5424529',
        'What are my appointments today?'
    ];

    for (const command of commands) {
        console.log(`\nCommand: "${command}"`);
        try {
            const result = await handleUserInput(command);
            console.log('Result:', result);
        } catch (error) {
            console.error('Error:', error.message);
        }
        console.log('-------------------');
    }
}

test();
