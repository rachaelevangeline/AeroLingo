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
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: inputText })
      });
  
      const data = await response.json();
      const explanation = data.explanation || "No explanation found.";
      outputDiv.innerHTML = `<p><strong>Explanation:</strong><br>${explanation}</p>`;
    } catch (error) {
      outputDiv.innerHTML = `<p>Error: ${error.message}</p>`;
    }
  }
  