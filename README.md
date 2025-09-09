# Flask Gemini Chatbot (split files)


A minimal Flask chatbot that uses the Gemini API via the official Google Gen AI Python SDK.


Key points
- Uses `google-genai` Python SDK to call `client.models.generate_content(...)` to generate replies.
- Auth via `GEMINI_API_KEY` environment variable (or pass an API key into `genai.Client()`). citeturn0search0turn0search2


Quick start
1. Create and activate a virtualenv.
2. Copy files from this scaffold.
3. Install dependencies: `pip install -r requirements.txt`.
4. Create a `.env` file or export `GEMINI_API_KEY` and `FLASK_SECRET_KEY`.
5. Run `python run.py` and open http://127.0.0.1:5000


Notes
- For chat-style workflows you can also use the SDK `client.chats.create(...)` API (structured chat sessions). See the SDK docs. citeturn0search4