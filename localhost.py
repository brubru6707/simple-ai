from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

db = SQLAlchemy(app)

class AI_Query(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(100), nullable=False)
    response = db.Column(db.String(10000), nullable=False)

    def __init__(self, question, response):
        self.question = question
        self.response = response

@app.route('/')
def index():
    return render_template('index.html', ai_query=AI_Query.query.all())

@app.route('/api/submit_question', methods=['POST'])
def submit_question():
    # Get the question from the POST request
    data = request.get_json()
    question_text = data.get('question')
    response_text = data.get("response")

    # Validate the input
    if not question_text:
        return jsonify({'error': 'Question is required'}), 400
    
    with app.app_context():
        ai_query = AI_Query(question_text, response_text)
        db.session.add(ai_query)
        db.session.commit()
    return jsonify({'response': response_text}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host="localhost", port=5000, debug=True)