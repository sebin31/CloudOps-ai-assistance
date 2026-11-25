
const API_URL = "http://127.0.0.1:8000/chat";

const chatBox = document.getElementById("chat-box");
const chatForm = document.getElementById("chat-form");
const userInput = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");
const clearBtn = document.getElementById("clear-btn");

let messages = [];
let isSending = false;

// Keep the original welcome screen for New Chat
const welcomeScreen = chatBox.innerHTML;


// Display a message
function addMessage(role, content) {

    const welcome = document.getElementById("welcome");

    if (welcome) {
        welcome.remove();
    }

    const messageDiv = document.createElement("div");
    messageDiv.className = `message ${role}`;

    const contentDiv = document.createElement("div");
    contentDiv.className = "message-content";

    // Display text safely without interpreting HTML
    contentDiv.textContent = content;

    messageDiv.appendChild(contentDiv);
    chatBox.appendChild(messageDiv);

    chatBox.scrollTop = chatBox.scrollHeight;

    return contentDiv;
}


// Send a message to FastAPI
async function sendMessage() {

    const message = userInput.value.trim();

    if (!message || isSending) {
        return;
    }

    // Backend accepts a maximum of 30 messages
    if (messages.length >= 30) {
        addMessage(
            "assistant",
            "This conversation is full. Please click New Chat to continue."
        );
        return;
    }

    isSending = true;

    messages.push({
        role: "user",
        content: message
    });

    addMessage("user", message);

    userInput.value = "";

    sendBtn.disabled = true;
    clearBtn.disabled = true;
    userInput.disabled = true;
    sendBtn.textContent = "Thinking...";

    const loadingMessage = addMessage(
        "assistant",
        "Thinking..."
    );

    try {

        const response = await fetch(API_URL, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                messages: messages
            })

        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.detail || "Unable to get an AI response."
            );
        }

        const reply = data.reply;

        loadingMessage.textContent = reply;

        messages.push({
            role: "assistant",
            content: reply
        });

    } catch (error) {

        loadingMessage.textContent =
            "Sorry, something went wrong: " + error.message;

        // Remove failed request from conversation history
        messages.pop();

        console.error("Chat error:", error);

    } finally {

        isSending = false;

        sendBtn.disabled = false;
        clearBtn.disabled = false;
        userInput.disabled = false;

        sendBtn.textContent = "Send ↑";

        userInput.focus();

    }
}


// Submit message
chatForm.addEventListener("submit", (event) => {

    event.preventDefault();

    sendMessage();

});


// Suggested questions
document.querySelectorAll(".suggestion").forEach(button => {

    button.addEventListener("click", () => {

        userInput.value = button.dataset.question;

        chatForm.requestSubmit();

    });

});


// Start a new conversation
clearBtn.addEventListener("click", () => {

    if (isSending) {
        return;
    }

    messages = [];

    chatBox.innerHTML = welcomeScreen;

    // Reattach events to the restored suggestion buttons
    document.querySelectorAll(".suggestion").forEach(button => {

        button.addEventListener("click", () => {

            userInput.value = button.dataset.question;

            chatForm.requestSubmit();

        });

    });

    userInput.focus();

});
