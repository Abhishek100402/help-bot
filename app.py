# app.py
import os
from flask import Flask, request, jsonify, render_template_string, session
from google import genai
from dotenv import load_dotenv

# Load .env if present (optional)
load_dotenv()
def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get("FLASK_SECRET_KEY", "change-this-secret-for-prod")

    @app.route("/")
    def index():
        return "Hello from Flask factory!"

    return app
# ---------- Config ----------
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("Set GEMINI_API_KEY (or GOOGLE_API_KEY) in your environment. See docs: https://ai.google.dev/gemini-api/docs/api-key")

MODEL_NAME = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")  # change if you prefer another Gemini model
MAX_HISTORY = 8  # keep last N turns in session to build context

# Flask
app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "change-this-secret-for-prod")

# GenAI client (explicit api_key usage is supported)
client = genai.Client(api_key=GEMINI_API_KEY)

# Simple HTML UI (for quick testing)
INDEX_HTML = """
<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Help bot (Flask)</title>
    <style>
      body { font-family: Arial, sans-serif; padding: 20px; max-width:800px; margin:auto; }
      #messages { border:1px solid #ddd; padding:12px; height:400px; overflow:auto; margin-bottom:12px; }
      .user { color: #0b57d0; margin-bottom:8px; }
      .bot { color: #333; margin-bottom:8px; }
      textarea { width:100%; height:80px }
      button { padding:8px 12px; }
    </style>
  </head>
  <body>
    <h2>Gemini Chatbot (Flask)</h2>
    <div id="messages"></div>
    <textarea id="msg" placeholder="Type your message..."></textarea><br>
    <button onclick="send()">Send</button>
    <script>
      async function send(){
        const t = document.getElementById('msg').value.trim();
        if(!t) return;
        append('You', t, 'user');
        document.getElementById('msg').value = '';
        const resp = await fetch('/chat', {
          method: 'POST',
          headers: {'Content-Type':'application/json'},
          body: JSON.stringify({message: t})
        });
        const j = await resp.json();
        if(j.error) append('Error', j.error, 'bot');
        else append('Bot', j.reply, 'bot');
      }
      function append(who, text, cls){
        const m = document.getElementById('messages');
        const d = document.createElement('div');
        d.className = cls;
        d.innerHTML = '<b>' + who + ':</b> ' + text.replace(/\\n/g,'<br>');
        m.appendChild(d); m.scrollTop = m.scrollHeight;
      }
      // load history
      (async ()=>{
        const r = await fetch('/history');
        const j = await r.json();
        j.history.forEach(h => append(h.who, h.text, h.who=='You' ? 'user' : 'bot'));
      })();
    </script>
  </body>
</html>
"""

# ---------- Helpers ----------
def ensure_history():
    if 'history' not in session:
        session['history'] = []  # list of dicts: {'who': 'You'|'Bot', 'text': '...'}
    return session['history']

def build_prompt(user_message: str):
    """
    Build a single text prompt from the saved session history + current user message.
    We format as alternating lines: User: ... \n Assistant: ...
    This is a simple approach — you can also use client.chats.create(...) for structured chat sessions.
    """
    history = ensure_history()
    # Start with an optional system instruction to define assistant behaviour:
    system = ("You are a helpful assistant. Be concise and answer clearly. "
              "If the user asks for code examples, provide runnable snippets. "
              "Do not hallucinate; if unsure, ask for clarification.")
    parts = [f"System: {system}"]
    # include last few turns
    for turn in history[-(MAX_HISTORY*2):]:
        who = turn['who']
        text = turn['text']
        parts.append(f"{who}: {text}")
    parts.append(f"You: {user_message}")
    parts.append("Assistant:")
    return "\n\n".join(parts)

# ---------- Routes ----------
@app.route('/')
def index():
    return render_template_string(INDEX_HTML)

@app.route('/history')
def get_history():
    hist = ensure_history()
    # return last 20 turns
    return jsonify({'history': hist[-40:]})

@app.route('/chat', methods=['POST'])
def chat():
    payload = request.get_json(force=True)
    if not payload or 'message' not in payload:
        return jsonify({'error': 'No message provided.'}), 400
    user_message = payload['message'].strip()
    if not user_message:
        return jsonify({'error': 'Empty message.'}), 400

    # save user's message
    hist = ensure_history()
    hist.append({'who': 'You', 'text': user_message})
    session.modified = True

    # build prompt and call Gemini
    prompt = build_prompt(user_message)

    try:
        # Simple usage: generate_content with a single text prompt (docs show this pattern).
        # Official example: client.models.generate_content(model="gemini-2.5-flash", contents="...").
        resp = client.models.generate_content(model=MODEL_NAME, contents=prompt)
        # .text holds the model text output in examples; convert to string safely
        reply_text = getattr(resp, "text", None) or str(resp)
    except Exception as e:
        err = f"API error: {e}"
        # store assistant error message (optional)
        hist.append({'who': 'Bot', 'text': err})
        session.modified = True
        return jsonify({'error': err}), 500

    # save assistant reply
    hist.append({'who': 'Bot', 'text': reply_text})
    session.modified = True

    return jsonify({'reply': reply_text})

if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get("PORT", 5000)))

