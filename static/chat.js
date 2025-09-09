window.onload = function() {
      const messages = document.getElementById('messages');
      const greet = document.createElement('div');
      greet.className = 'message bot';
      greet.textContent = "Hello! I'm Help Bot. How can I assist you today?";
      messages.appendChild(greet);
    };

    async function sendMessage() {
      const input = document.getElementById('userInput');
      const messages = document.getElementById('messages');
      const text = input.value.trim();
      if (!text) return;

      // Add user message
      const userMsg = document.createElement('div');
      userMsg.className = 'message user';
      userMsg.textContent = text;
      messages.appendChild(userMsg);
      input.value = "";

      // Add typing indicator
      const typing = document.createElement('div');
      typing.className = 'message bot';
      typing.innerHTML = `
        <div class="typing-indicator">
          <div class="typing-dot"></div>
          <div class="typing-dot"></div>
          <div class="typing-dot"></div>
        </div>`;
      messages.appendChild(typing);
      messages.scrollTop = messages.scrollHeight;

      // Send request to backend
      const response = await fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text })
      });
      const data = await response.json();

      // Remove typing indicator
      messages.removeChild(typing);

      // Add bot response
      const botMsg = document.createElement('div');
      botMsg.className = 'message bot';
      // Use marked to render markdown
      botMsg.innerHTML = marked.parse(data.reply || data.error || "No response from AI.");
      messages.appendChild(botMsg);
      messages.scrollTop = messages.scrollHeight;
    }

    // Allow Enter key to send
    document.getElementById("userInput")
      .addEventListener("keypress", function(event) {
        if (event.key === "Enter") {
          sendMessage();
        }
      });