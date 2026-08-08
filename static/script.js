function formatBotText(text) {
    // Convert simple markdown (**bold**) to <strong>, but escape everything
    // else first so no other HTML/script can be injected (XSS-safe).
    let escaped = text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;");
    return escaped.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");
}

function addMessage(text, className, allowFormatting) {
    let chatbox = document.getElementById("chatbox");
    let div = document.createElement("div");
    div.className = className;
    if (allowFormatting) {
        div.innerHTML = formatBotText(text); // safe: input is escaped above
    } else {
        div.textContent = text; // safe: prevents XSS (no raw HTML injection)
    }
    chatbox.appendChild(div);
    chatbox.scrollTop = chatbox.scrollHeight;
    return div;
}

function sendMessage(){

    let input = document.getElementById("userInput");
    let sendBtn = document.querySelector(".input-area button");
    let msg = input.value.trim();

    if(msg === "") return;

    // user message
    addMessage(msg, "user");
    input.value="";
    input.disabled = true;
    sendBtn.disabled = true;

    // typing indicator
    let typingDiv = addMessage("Typing...", "bot");
    typingDiv.id = "typing";

    fetch("/get", {
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({message:msg})
    })
    .then(res=>res.json())
    .then(data=>{
        document.getElementById("typing").remove();
        addMessage(data.reply, "bot", true);
    })
    .catch(err=>{
        document.getElementById("typing").remove();
        addMessage("⚠️ Something went wrong. Please try again.", "bot");
        console.error(err);
    })
    .finally(()=>{
        input.disabled = false;
        sendBtn.disabled = false;
        input.focus();
    });
}

function handleKey(event){
    if(event.key === "Enter"){
        sendMessage();
    }
}