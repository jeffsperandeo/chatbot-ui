// components/messages/commandExecutor.js

const { parseCommand } = require("../../backend/utils/commandParser");

async function handleExecuteCommand(messageContent, setResponseMessage) {
  const parsedCommand = parseCommand(messageContent);

  if (!parsedCommand) {
    console.error('Command not recognized:', messageContent);
    setResponseMessage("Command not recognized.");
    return;
  }

  const { action, details } = parsedCommand;
  console.log(`Processing command: ${action} with details: ${details}`);

  // Fallback response from AI
  const fallbackResponse = `
Sure, let's get the details for the ${details}.

${details} Specifications:

Make: BMW
Model: 330i
Trim: Base
Year: 2019
VIN: WBA5R1C53KAK07369

Engine and Performance:
Engine Type: 2.0L TwinPower Turbo Inline-4 Gas
Horsepower: 255 hp @ 5,000-6,500 rpm
Torque: 295 lb-ft @ 1,550-4,400 rpm
Transmission: 8-speed automatic
Drivetrain: Rear-Wheel Drive (RWD)
0-60 mph: Approximately 5.6 seconds

Dimensions:
Wheelbase: 112.2 inches
Length: 185.7 inches
Width: 71.9 inches
Height: 56.8 inches
Curb Weight: Around 3,582 lbs

Fuel Economy:
City: 26 mpg
Highway: 36 mpg
Combined: 30 mpg
Fuel Tank Capacity: 15.6 gallons

Interior Features:
Seating Capacity: 5
Upholstery: SensaTec (synthetic leather)
Infotainment System: iDrive 6.0 with an 8.8-inch touchscreen
Audio System: 10-speaker HiFi sound system
Climate Control: Dual-zone automatic climate control
Other Features: Apple CarPlay, navigation, Bluetooth connectivity, and a rearview camera

Safety Features:
Standard Safety: Forward collision warning, automatic emergency braking, lane departure warning, and a driver attention monitor
Optional Safety: Adaptive cruise control, blind-spot monitoring, and a surround-view camera system

Exterior Features:
Wheels: 18-inch alloy wheels
Lighting: LED headlights and taillights
Sunroof: Standard power moonroof

Maintenance and Service Recommendations:
For a 2019 BMW 330i Base, regular maintenance is crucial to ensure optimal performance and longevity. Here are some general service recommendations:
Oil Changes: Every 10,000 miles or 12 months, whichever comes first.
Brake Inspection: Every 10,000 miles.
Tire Rotation and Balance: Every 10,000 miles.
Coolant Check: Every 30,000 miles.
Transmission Fluid: Check every 30,000 miles.
Spark Plugs: Replace every 60,000 miles.
Air Filters: Replace every 20,000 miles.

For specific service history or detailed diagnostics, you might want to check the vehicle's service records or consult with a certified BMW technician.

Let me know if there's anything else you'd like to know or if you need assistance with something else!
`;

  setResponseMessage(fallbackResponse);

  try {
    const authToken = 'your_token_here'; // Replace with the actual method to retrieve the token
    const response = await fetch('/command/execute', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        input: messageContent,
        userId: 'your_user_id_here', // Replace with the actual user ID
        authToken: authToken,
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const contentType = response.headers.get('content-type');
    if (contentType && contentType.includes('application/json')) {
      const data = await response.json();
      setResponseMessage(data);
    } else {
      const text = await response.text();
      throw new Error(`Unexpected response format: ${text}`);
    }
  } catch (error) {
    console.error(`Error processing command "${action}":`, error.message);
    setResponseMessage(`Error processing command "${action}": ${error.message}`);
  }
}

module.exports = { handleExecuteCommand };
