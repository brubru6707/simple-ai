from flask import Flask, jsonify
import google.generativeai as genai
import request
genai.configure(api_key="AIzaSyC__KT4oA-nyRESuVnRsI9PlZDsPxE_qis")
model = genai.GenerativeModel('gemini-1.5-flash')

app = Flask(__name__)

@app.route('/')
def home():
    return 'brurbu api'
    
@app.route('/api/submit_response', methods=['POST'])
def submit_question():
    # Get the question from the POST request
    data = request.get_json()
    question_text = data.get('question')

    # Validate the input
    if not question_text:
        return jsonify({'error': 'Question is required'}), 400

    ai_response = model.generate_content(question_text)
    return jsonify({'response': ai_response.text}), 200