from . import db

class Interval_pref(db.Model):
    __tablename__ = 'interval_prefs'
    interval = db.Column(db.Integer, primary_key=True)
    #timedelta stored here
    wait_time = db.Column(db.Interval, nullable=False)

class Deck(db.Model):
    __tablename__ = 'decks'
    deck_name = db.Column(db.String, primary_key=True)
    deck_tier = db.Column(db.Integer, nullable=False)

class Flashcard(db.Model):
    __tablename__ = 'flashcards'
    front = db.Column(db.String, primary_key=True)
    back = db.Column(db.String)
    deck_name = db.Column(db.String, db.ForeignKey(Deck.deck_name), nullable=False)
    initially_created = db.Column(db.DateTime, nullable=False)
    last_edited = db.Column(db.DateTime, nullable=False)
    last_studied = db.Column(db.DateTime, nullable=False)
    #Despite being called interval, not the same as an SQLAlchemy interval
    interval = db.Column(db.Integer, nullable=False)
    card_type = db.Column(db.Integer, nullable=False)
    #Location of the .wav/.mp3 file, if any, for back of card.
    sound_back = db.Column(db.String)
    sound_front = db.Column(db.String)
