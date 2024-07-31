from flask import Flask, url_for, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from proccess_image import set_up_proccess_image_function

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

db = SQLAlchemy(app)

set_up_proccess_image_function()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

@app.route('/', methods=['GET', 'POST'])
def serve_index():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        info_already_exists = User.query.filter_by(email=email).first() or User.query.filter_by(email=email).first()
        if info_already_exists:
            error_message = "Some information already exists!"
            return render_template('index.html', users=User.query.all(), error_message=error_message)
        user = User(username=username, email=email)
        db.session.add(user)
        db.session.commit()
        return render_template('index.html', users=User.query.all())
    return render_template('index.html', users=User.query.all())

@app.route('/<path:path>')
def serve_static(path):
    return render_template('static', path)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host="localhost", port=5000, debug=True)
