import React, { FC, useEffect, useState } from "react"
import { fetchAppointments } from "../api/appointments"

interface Appointment {
  id: string
  title: string
  startTime: string
}

const Appointments: FC = () => {
  const [appointments, setAppointments] = useState<Appointment[]>([])
  const [error, setError] = useState<string>("")
  const [loading, setLoading] = useState<boolean>(true)

  const token = localStorage.getItem("authToken") // Retrieve token from local storage
  console.log("Token retrieved from local storage:", token)

  useEffect(() => {
    const getAppointments = async () => {
      setLoading(true)
      try {
        const data = await fetchAppointments()
        setAppointments(data)
      } catch (err) {
        setError("Failed to fetch appointments.")
      } finally {
        setLoading(false)
      }
    }

    if (token) {
      getAppointments()
    } else {
      setError("No authentication token found.")
      setLoading(false)
    }
  }, [token])

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
