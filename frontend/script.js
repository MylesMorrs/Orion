const chatBox = document.getElementById("chat-box");
const input = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");
const voiceBtn = document.getElementById("voice-btn");

sendBtn.addEventListener("click", sendMessage);
voiceBtn.addEventListener("click", listenVoice);

function addMessage(sender, text) {
    const p = document.createElement("p");
    p.classList.add(sender);
    p.textContent = text;
    chatBox.appendChild(p);
    chatBox.scrollTop = chatBox.scrollHeight;
}

async function sendMessage() {
    const text = input.value.trim();
    if (!text) return;

    addMessage("user", text);
    input.value = "";

    const res = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text })
    });

    const data = await res.json();
    if (data.reply) {
        addMessage("ai", data.reply);
    } else {
        addMessage("ai", "Error: " + data.error);
    }
}

async function listenVoice() {
    addMessage("ai", "🎤 Listening...");
    const res = await fetch("http://127.0.0.1:8000/listen");
    const data = await res.json();

    if (data.heard) {
        addMessage("user", data.heard);
        input.value = data.heard;
        sendMessage();
    } else {
        addMessage("ai", "Error: " + data.error);
    }
}
