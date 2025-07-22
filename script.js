async function decodeATC() {
    const atcInput = document.getElementById("atcInput").value.trim();
    const explanationOutput = document.getElementById("explanationOutput");

    if (!atcInput) {
        explanationOutput.innerHTML = "<p style='color: orange;'>Please enter an ATC phrase first.</p>";
        return;
    }

    explanationOutput.innerHTML = "<p><em>Explaining...</em> ✈️</p>";
    explanationOutput.style.color = '#555'; // Set loading text color

    try {
        // Call your Netlify Function (now Python, but the endpoint is the same)
        const response = await fetch("/.netlify/functions/decode", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ phrase: atcInput })
        });

        const data = await response.json();

        // Check if the HTTP response itself was not OK (e.g., 4xx, 5xx)
        if (!response.ok) {
            // If the function returned an error, display it
            throw new Error(data.error || `HTTP error! Status: ${response.status}`);
        }

        // Display the explanation from the AI
        explanationOutput.innerHTML = `<h3>Explanation:</h3><p>${data.explanation}</p>`;
        explanationOutput.style.color = 'black'; // Reset color on success

    } catch (error) {
        console.error('Error decoding ATC phrase:', error);
        explanationOutput.innerHTML = `<p style='color: red;'>Error: ${error.message}. Could not get an explanation.</p>`;
    }
}
