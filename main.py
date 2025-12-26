from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import openai
import os

app = FastAPI()

# ========== CONFIG ==========
openai.api_key = os.getenv("OPENAI_API_KEY")

SYSTEM_PROMPT = """
Wewe ni CIXZONE AI.
Umetengenezwa na Joseph Octavian Lyimo.
Lengo lako ni kusaidia Afrika, hasa Tanzania.
Unajibu kwa akili, kwa heshima, na kwa lugha ya mtumiaji.
Unamkumbuka creator wako na unamheshimu.
"""

conversation_memory = []

# ========== AI FUNCTION ==========
def ask_ai(user_message):
    conversation_memory.append({"role": "user", "content": user_message})

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages += conversation_memory[-10:]  # memory ya mazungumzo ya mwisho

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    ai_reply = response.choices[0].message.content
    conversation_memory.append({"role": "assistant", "content": ai_reply})
    return ai_reply

# ========== WEB UI ==========
@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <html>
    <head>
        <title>CIXZONE AI</title>
        <style>
            body {
                background: #0b0f1a;
                color: white;
                font-family: Arial;
                text-align: center;
                padding-top: 80px;
            }
            input {
                width: 70%;
                padding: 12px;
                font-size: 16px;
            }
            button {
                padding: 12px 20px;
                margin-top: 10px;
                font-size: 16px;
                cursor: pointer;
            }
            #reply {
                margin-top: 30px;
                font-size: 18px;
            }
        </style>
    </head>
    <body>
        <h1>🤖 CIXZONE AI</h1>
        <input id="msg" placeholder="Andika ujumbe..." />
        <br>
        <button onclick="send()">Tuma</button>
        <div id="reply"></div>

        <script>
            async function send() {
                const msg = document.getElementById("msg").value;
                const res = await fetch("/chat", {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify({message: msg})
                });
                const data = await res.json();
                document.getElementById("reply").innerText = data.reply;
            }
        </script>
    </body>
    </html>
    """

# ========== CHAT ENDPOINT ==========
@app.post("/chat")
async def chat(req: Request):
    data = await req.json()
    user_message = data["message"]
    reply = ask_ai(user_message)
    return {"reply": reply}
