import axios from "axios"

export async function sendCommand(input: string) {
  try {
    const token = localStorage.getItem("authToken") // Retrieve token from local storage
    console.log("Token retrieved from local storage:", token)
    if (!token) {
      throw new Error("No authentication token found.")
    }
    const response = await axios.post(
      "http://localhost:3002/commands/execute",
      { input },
      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    )
    return response.data
  } catch (error) {
    console.error("Error executing command:", error)
    return { error: "Failed to execute command" }
  }
}
