import React, { useEffect, useState } from "react"
import fetchAppointments from "./appointments" // Correct import statement

interface Appointment {
  id: string
  title: string
  startTime: string
}

const Appointments: React.FC = () => {
  const [appointments, setAppointments] = useState<Appointment[]>([])
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState<boolean>(true)

  useEffect(() => {
    const getAppointments = async () => {
      try {
        const data: Appointment[] = await fetchAppointments()
        setAppointments(data)
      } catch (err) {
        setError("Error fetching appointments")
        console.error("Error fetching appointments:", err)
      } finally {
        setLoading(false)
      }
    }

    getAppointments()
  }, [])

  if (loading) {
    return <div>Loading...</div>
  }

  if (error) {
    return <div>{error}</div>
  }

  return (
    <div>
      <h2>Appointments</h2>
      <ul>
        {appointments.map(appointment => (
          <li key={appointment.id}>
            {appointment.title} -{" "}
            {new Date(appointment.startTime).toLocaleString()}
          </li>
        ))}
      </ul>
    </div>
  )
}

export default Appointments
