from flask import Flask, render_template, redirect, url_for, request
from models import db, User, Song
from data_manager import DataManager
import os
import requests

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/music.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

data_manager = DataManager()

@app.route('/')
def index():
    users = data_manager.get_users()
    return render_template('index.html', users=users)


@app.route('/users', methods=['POST'])
def create_user():
    name = request.form.get('name')
    data_manager.create_user(name)
    return redirect(url_for('index'))


@app.route('/users/<int:user_id>/songs')
def list_songs(user_id):
    songs = data_manager.get_songs(user_id)
    return render_template('songs.html', songs=songs, user_id=user_id)


@app.route('/users/<int:user_id>/songs', methods=['POST'])
def add_song(user_id):
    title = request.form.get('title')
    artist = request.form.get('artist')
    genre = request.form.get('genre')
    cover_url = request.form.get('cover_url')

    # Fallbacks: If no input -> Use iTunes API
    if not artist or not genre or not cover_url:
        search_term = title.replace(" ", "+")
        url = f"https://itunes.apple.com/search?term={search_term}&limit=1&entity=song"
        response = requests.get(url).json()
        results = response.get("results")

        if results:
            first = results[0]
            if not artist:
                artist = first.get("artistName")
            if not genre:
                genre = first.get("primaryGenreName")
            if not cover_url:
                cover_url = first.get("artworkUrl100")

    song = Song(
        title=title,
        artist=artist if artist else "Unknown Artist",
        genre=genre if genre else "Unknown Genre",
        cover_url=cover_url if cover_url else "",
        user_id=user_id
    )

    data_manager.add_song(song)
    return redirect(url_for('list_songs', user_id=user_id))


@app.route('/users/<int:user_id>/songs/<int:song_id>/delete', methods=['POST'])
def delete_song(user_id, song_id):
    data_manager.delete_song(song_id)
    return redirect(url_for('list_songs', user_id=user_id))


@app.route('/users/<int:user_id>/songs/<int:song_id>/update', methods=['POST'])
def update_song(user_id, song_id):
    new_title = request.form.get('new_title')
    data_manager.update_song(song_id, new_title)
    return redirect(url_for('list_songs', user_id=user_id))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)