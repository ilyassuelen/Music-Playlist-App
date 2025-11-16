from models import db, User, Song

class DataManager():
    # ----- User -----
    def create_user(self, name):
        new_user = User(name=name)
        db.session.add(new_user)
        db.session.commit()
        return new_user


    def get_users(self):
        return User.query.all()

    # ----- Song -----
    def get_songs(self, user_id):
        return Song.query.filter_by(user_id=user_id).all()


    def add_song(self, song):
        db.session.add(song)
        db.session.commit()

    def update_song(self, song_id, new_title):
        song = Song.query.get(song_id)
        if song:
            song.title = new_title
            db.session.commit()


    def delete_song(self, song_id):
        song = Song.query.get(song_id)
        if song:
            db.session.delete(song)
            db.session.commit()