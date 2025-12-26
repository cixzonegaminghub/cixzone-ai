from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI()

AI_NAME = "CIXZONE AI"
AI_CREATOR = "Joseph Octavian Lyimo"
AI_MISSION = "Africa First Intelligent Web Assistant"

class ChatRequest(BaseModel):
    message: str

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>CIXZONE AI</title>
        <style>
            body { font-family: Arial; background:#0f172a; color:white; }
            .chat { max-width:600px; margin:auto; margin-top:50px; }
            input, button { padding:10px; width:100%; margin-top:10px; }
            .box { background:#020617; padding:15px; border-radius:8px; }
        </style>
    </head>
    <body>
        <div class="chat">
            <h2>🤖 CIXZONE AI</h2>
            <div id="response" class="box">Karibu! Mimi ni CIXZONE AI 🇹🇿</div>
            <input id="msg" placeholder="Andika ujumbe wako..." />
            <button onclick="send()">Tuma</button>
        </div>

        <script>
            async function send() {
                let msg = document.getElementById("msg").value;
                let res = await fetch("/chat", {
                    method:"POST",
                    headers:{ "Content-Type":"application/json" },
                    body: JSON.stringify({message: msg})
                });
                let data = await res.json();
                document.getElementById("response").innerText = data.reply;
            }
        </script>
    </body>
    </html>
    """

@app.post("/chat")
def chat(req: ChatRequest):
    user = req.message.lower()

    if "creator" in user or "nani alikutengeneza" in user:
        reply = f"Nimetengenezwa na {AI_CREATOR}."
    elif "mission" in user or "lengo" in user:
        reply = AI_MISSION
    elif "jina lako" in user:
        reply = f"Mimi ni {AI_NAME}."
    else:
        reply = f"Nimekupata. Umesema: '{req.message}'. Niko hapa kukusaidia."

    return {"reply": reply}
