const axios = require('axios');

async function testChatEndpoint() {
    const testCases = [
        {
            message: 'Create a new vehicle with details {"customerId": 1, "year": 2020, "make": "Toyota", "model": "Camry", "vin": "1234567890"}',
            userId: 'testUser1',
            authToken: 'your_token_here',
        },
        {
            message: 'Update vehicle details 1 with {"color": "red"}',
            userId: 'testUser2',
            authToken: 'your_token_here',
        },
        {
            message: 'Get vehicle details 1',
            userId: 'testUser3',
            authToken: 'your_token_here',
        },
        {
            message: 'List all vehicles',
            userId: 'testUser4',
            authToken: 'your_token_here',
        },
        {
            message: 'Create a new customer with details {"shopId": 1, "firstName": "John", "lastName": "Doe"}',
            userId: 'testUser5',
            authToken: 'your_token_here',
        },
        {
            message: 'Update customer details 1 with {"email": "john.doe@example.com"}',
            userId: 'testUser6',
            authToken: 'your_token_here',
        },
        {
            message: 'Get customer details 1',
            userId: 'testUser7',
            authToken: 'your_token_here',
        },
        {
            message: 'List all customers',
            userId: 'testUser8',
            authToken: 'your_token_here',
        },
        {
            message: 'Create a repair order with details {"shopId": 1, "customerId": 1, "vehicleId": 1}',
            userId: 'testUser9',
            authToken: 'your_token_here',
        },
        {
            message: 'Update repair order 1 with {"keyTag": "A1"}',
            userId: 'testUser10',
            authToken: 'your_token_here',
        },
        {
            message: 'Get repair order details 1',
            userId: 'testUser11',
            authToken: 'your_token_here',
        },
        {
            message: 'List all repair orders',
            userId: 'testUser12',
            authToken: 'your_token_here',
        },
        {
            message: 'Get job details 1',
            userId: 'testUser13',
            authToken: 'your_token_here',
        },
        {
            message: 'Update job 1 with {"name": "Oil Change"}',
            userId: 'testUser14',
            authToken: 'your_token_here',
        },
        {
            message: 'List all jobs',
            userId: 'testUser15',
            authToken: 'your_token_here',
        },
        {
            message: 'Create an appointment with details {"shopId": 1, "customerId": 1, "vehicleId": 1, "startTime": "2023-01-01T10:00:00Z", "endTime": "2023-01-01T11:00:00Z"}',
            userId: 'testUser16',
            authToken: 'your_token_here',
        },
        {
            message: 'Update appointment 1 with {"description": "Annual Service"}',
            userId: 'testUser17',
            authToken: 'your_token_here',
        },
        {
            message: 'Get appointment details 1',
            userId: 'testUser18',
            authToken: 'your_token_here',
        },
        {
            message: 'List all appointments',
            userId: 'testUser19',
            authToken: 'your_token_here',
        },
        {
            message: 'List all employees',
            userId: 'testUser20',
            authToken: 'your_token_here',
        },
    ];

    for (const testCase of testCases) {
        try {
            const response = await axios.post('http://localhost:3002/chat/message', testCase);
            console.log(`Response for message "${testCase.message}":`, response.data);
        } catch (error) {
            console.error(`Error for message "${testCase.message}":`, error.response ? error.response.data : error.message);
        }
    }
}

testChatEndpoint();
