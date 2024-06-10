// backend/routes/chat.js

const { handleUserInput } = require('../services/commandHandler');
const { OpenAIStream, StreamingTextResponse } = require('ai');

export async function POST(request) {
  const json = await request.json();
  const { chatSettings, messages, userId } = json;

  const lastMessage = messages[messages.length - 1].content;

  // Check for commands and handle them
  const commandResponse = await handleUserInput(lastMessage, userId);
  if (commandResponse) {
    return new Response(JSON.stringify({ message: commandResponse }), { status: 200 });
  }

  // If no command, proceed with OpenAI chat completion
  const response = await openai.chat.completions.create({
    model: chatSettings.model,
    messages,
    temperature: chatSettings.temperature,
    max_tokens: 4096,
    stream: true,
  });

  const stream = OpenAIStream(response);
  return new StreamingTextResponse(stream);
}
