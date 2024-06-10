// backend/testCommandHandler.js

const { parseCommand } = require('./utils/commandParser');
const { commandHandler } = require('./commandHandler');

const testCommands = [
    'list all repair orders',
    'update repair order 1127105 with {"customerConcerns": [{"id": 8241, "concern": "NOISE WHEN TURNING LEFT", "techComment": "Replaced left CV joint, noise resolved"}, {"id": 8242, "concern": "CHECK TPMS SENSOR", "techComment": "Replaced faulty sensor, light off"}]}',
    'list all appointments',
    'list all vehicles',
];

testCommands.forEach(async (command) => {
    const parsedCommand = parseCommand(command);
    console.log(`Parsed command for "${command}":`, parsedCommand);
    const response = await commandHandler(parsedCommand);
    console.log(`Response for command "${command}":`, response);
});