from flask import Blueprint, render_template, request, session, current_app, jsonify
from .gemini_client import GeminiClient


bp = Blueprint('chat', __name__)




def ensure_history():
    if 'history' not in session:
        session['history'] = []
    return session['history']




@bp.route('/')
def index():
    return render_template('index.html')




@bp.route('/history')
def get_history():
    hist = ensure_history()
    return jsonify({'history': hist[-40:]})




@bp.route('/chat', methods=['POST'])
def chat():
    data = request.get_json(force=True)
    if not data or 'message' not in data:
        return jsonify({'error': 'No message provided.'}), 400


    user_message = data['message'].strip()
    if not user_message:
        return jsonify({'error': 'Empty message.'}), 400


    hist = ensure_history()
    hist.append({'who': 'You', 'text': user_message})
    session.modified = True


    # Build a simple text prompt combining recent history + system instruction
    system = (
    "You are Help Bot, a friendly, empathetic, and helpful assistant. "
    "Always answer with warmth, encouragement, and a touch of emotion. "
    "Format your answers using Markdown for clarity (lists, bold, etc). "
    "If you don't know, say you don't know. Do not hallucinate.")


    # include last N turns to provide context
    context_turns = hist[-10:]
    parts = [f"System: {system}"]
    for t in context_turns:
        parts.append(f"{t['who']}: {t['text']}")
    parts.append(f"You: {user_message}")
    parts.append("Assistant:")


    prompt = "\n\n".join(parts)


    # Create Gemini client wrapper
    api_key = current_app.config.get('GEMINI_API_KEY')
    model = current_app.config.get('GEMINI_MODEL')
    gc = GeminiClient(api_key=api_key, model=model)


    try:
        reply = gc.generate_text(prompt)
        print("Gemini reply:", repr(reply))  # Debug print
    except Exception as e:
        err = f"Gemini API error: {e}"
        print("Gemini error:", err)          # Debug print
        hist.append({'who': 'Bot', 'text': err})
        session.modified = True
        return jsonify({'error': err}), 500


    hist.append({'who': 'Bot', 'text': reply})
    session.modified = True
    return jsonify({'reply': reply})