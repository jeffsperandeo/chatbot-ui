// testCommandExecutor.js

const { handleExecuteCommand } = require('./components/messages/commandExecutor');

async function testHandleExecuteCommand() {
  const input = 'get vehicle details WBA5R1C53KAK07369';
  const setResponseMessage = (message) => {
    console.log('Response Message:', message);
  };

  await handleExecuteCommand(input, setResponseMessage);
}

testHandleExecuteCommand();
