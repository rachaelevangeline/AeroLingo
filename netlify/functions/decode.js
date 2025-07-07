// decode.js – Netlify function using OpenAI API securely

export async function handler(event) {
  const input = JSON.parse(event.body);
  const phrase = input.phrase;

  const OPENAI_API_KEY = process.env.OPENAI_API_KEY;

  try {
    const response = await fetch("https://api.openai.com/v1/chat/completions", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${OPENAI_API_KEY}`
      },
      body: JSON.stringify({
        model: "gpt-3.5-turbo",
        messages: [
          {
            role: "system",
            content: "You are an expert aviation instructor. Explain any ATC or pilot phrase in simple, beginner-friendly English."
          },
          {
            role: "user",
            content: phrase
          }
        ]
      })
    });

    const data = await response.json();

    return {
      statusCode: 200,
      body: JSON.stringify({ explanation: data.choices?.[0]?.message?.content || "No explanation found." })
    };
  } catch (err) {
    return {
      statusCode: 500,
      body: JSON.stringify({ error: err.message })
    };
  }
}
