# app.py
from flask import Flask, request, jsonify, send_from_directory, session # Import session
from backend.model_service import generate_questions_with_context 
import os
from flask_cors import CORS


app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)
# Dictionary to store conversation history for each session
# In a real app, use a proper session management or database
conversation_histories = {}

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

@app.route('/generate-question', methods=['POST'])
def generate_question_route():
    user_input = request.json.get('product_description')
    if not user_input:
        return jsonify({"error": "Product description is required"}), 400

    # Get a unique session ID for the user
    # For simplicity, we'll use a fixed ID for now, or you can use Flask's session
    session_id = 'default_user_session' # Using a simple fixed ID for now
    # Or, if you configure Flask sessions properly: session_id = session.sid

    # Retrieve history for this session, or initialize it
    history = conversation_histories.get(session_id, [])

    try:
        # Call the modified model service function with history
        question_text, updated_history = generate_questions_with_context(user_input, history)

        # Update the conversation history for this session
        conversation_histories[session_id] = updated_history

        question_json = {
            "question": {
                "text": question_text,
                "type": "text"
            }
        }
        return jsonify(question_json)

    except Exception as e:
        print(f"Error in generate_question_route: {e}")
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=False)