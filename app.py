from flask import Flask, render_template, redirect, url_for, request
from models import db, User, Song

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data/music.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html', users=[])


@app.route('/users', methods=['POST'])
def create_user():
    name = request.form.get('name')
    print(f"User added: {name}")  # nur zum Testen
    return redirect(url_for('index'))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)