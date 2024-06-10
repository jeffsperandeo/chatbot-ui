import React, { useState } from "react"
import axios from "axios"

const ChatGPTAssistant: React.FC = () => {
  const [input, setInput] = useState("")
  const [output, setOutput] = useState("")

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInput(e.target.value)
  }

  const handleSubmit = async () => {
    try {
      const token = localStorage.getItem("authToken") // Retrieve token from local storage
      console.log("Token retrieved from local storage:", token)
      if (!token) {
        throw new Error("No authentication token found.")
      }
      const response = await axios.post(
        "/command",
        { command: input },
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      )
      setOutput(JSON.stringify(response.data, null, 2))
    } catch (error) {
      console.error("Error handling command:", error)
      setOutput("Error processing your request.")
    }
  }

  return (
    <div className="chat-gpt-assistant">
      <p>ChatGPT Assistant</p>
      <input
        type="text"
        value={input}
        onChange={handleInputChange}
        placeholder="Enter your command"
      />
      <button onClick={handleSubmit}>Submit</button>
      {output && <pre>{output}</pre>}
    </div>
  )
}

export default ChatGPTAssistant
