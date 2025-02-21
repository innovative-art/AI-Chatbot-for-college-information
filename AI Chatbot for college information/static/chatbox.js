document.getElementById('send-btn').addEventListener('click', sendMessage);

function sendMessage() {
    const userInput = document.getElementById('user-input').value.trim();
    if (userInput !== "") {
        // Send the user's query to the backend
        fetch('/ask', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query: userInput })
        })
        .then(response => response.json())
        .then(data => {
            // Display user and bot messages
            displayMessage("User", userInput);
            displayMessage("Bot", data.response);
        })
        .catch(() => {
            displayMessage("Bot", "Oops! Something went wrong. Please try again.");
        });
    }
    // Clear the input field
    document.getElementById('user-input').value = '';
}

function displayMessage(sender, message) {
    const chatMessages = document.getElementById('chat-messages');
    const messageElement = document.createElement('div');

    // Add classes based on the sender (User or Bot)
    messageElement.classList.add('message');
    messageElement.classList.add(sender === "User" ? 'user-message' : 'bot-message');

    // Set the message content
    messageElement.innerHTML = `<strong>${sender}:</strong> ${message}`;

    // Append the message element to the chat container
    chatMessages.appendChild(messageElement);

    // Scroll to the latest message
    chatMessages.scrollTop = chatMessages.scrollHeight;
}
