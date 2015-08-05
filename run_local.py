#!/usr/bin/env python
from app import create_app, db
from app.models import Interval_pref, Flashcard, Deck

#My application structure was inspired by Miguel Grinberg's book on Flask.

if __name__ == '__main__':
    app = create_app('localserver')
    with app.app_context():
        db.create_all()
    app.run()

