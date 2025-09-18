let session_id = Math.random().toString(36).substring(2);
let currentQuestion = "";

window.onload = () => {
    fetch("/start", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({session_id: session_id})
    }).then(() => {
        askQuestion();
    });
};

function askQuestion() {
    fetch(`/question?session_id=${session_id}`)
    .then(response => response.json())
    .then(data => {
        if (data.question) {
            currentQuestion = data.question;
            addMessage("bot", data.question);
        } else {
            addMessage("bot", "Interview finished.");
            getSummary();
        }
    });
}

function sendAnswer() {
    const input = document.getElementById("input");
    const answer = input.value;
    if (!answer) return;
    
    addMessage("user", answer);
    input.value = "";
    
    fetch("/answer", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({session_id: session_id, answer: answer})
    })
    .then(response => response.json())
    .then(data => {
        addMessage("bot", data.feedback);
        askQuestion();
    });
}

function getSummary() {
    fetch(`/end?session_id=${session_id}`)
    .then(response => response.json())
    .then(data => {
        addMessage("bot", data.summary);
    });
}

function addMessage(sender, text) {
    const chat = document.getElementById("chat");
    const div = document.createElement("div");
    div.classList.add("message");
    div.classList.add(sender);
    div.innerText = text;
    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
}
