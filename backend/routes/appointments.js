import axios from 'axios';

export const fetchAppointments = async (token) => {
    try {
        const response = await axios.get('/api/appointments', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        return response.data;
    } catch (error) {
        console.error('Error fetching appointments:', error.message);
        throw error;
    }
};
