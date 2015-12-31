#!/usr/bin/env python
from app import create_app, db
from app.models import Interval_pref, Flashcard, Deck
import argparse

#My application structure was inspired by Miguel Grinberg's book on Flask.

if __name__ == '__main__':
    app = create_app('localserver')
    with app.app_context():
        db.create_all()
    
    parser = argparse.ArgumentParser(description='Run flashcard app')
    #custom port
    parser.add_argument('-p', type=int, default=5000)
    args = parser.parse_args()
    
    app.run(port=args.p)

