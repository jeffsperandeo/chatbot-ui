import axios from 'axios';

export const fetchAppointments = async () => {
    const token = localStorage.getItem('authToken'); // Retrieve token from local storage
    console.log('Token retrieved from local storage:', token);
    if (!token) {
        throw new Error('No authentication token found.');
    }
    const response = await axios.get('/api/appointments', {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });
    return response.data;
};
