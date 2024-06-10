import axios from 'axios';

interface Appointment {
  id: string;
  title: string;
  startTime: string;
}

const fetchAppointments = async (): Promise<Appointment[]> => {
  const token = localStorage.getItem('authToken'); // Retrieve token from local storage
  if (!token) {
    throw new Error('No authentication token found.');
  }
  const response = await axios.get('/api/appointments', {
    headers: {
      'Authorization': `Bearer ${token}`,
      'Accept': 'application/json'
    }
  });
  return response.data as Appointment[];
};

export default fetchAppointments;
