async function decodeATC() {
  const inputText = document.getElementById("atcInput").value.trim();
  const outputDiv = document.getElementById("explanationOutput");

  if (!inputText) {
    outputDiv.innerHTML = "<p>Please enter an ATC phrase first.</p>";
    return;
  }

  outputDiv.innerHTML = "<p><em>Explaining...</em> ✈️</p>";

  try {
    const response = await fetch("/.netlify/functions/decode", {
      method: "POST",
      body: JSON.stringify({ phrase: inputText })
    });

    const data = await response.json();
    outputDiv.innerHTML = `<p><strong>Explanation:</strong><br>${data.explanation}</p>`;
  } catch (error) {
    outputDiv.innerHTML = `<p>Error: ${error.message}</p>`;
  }
}
