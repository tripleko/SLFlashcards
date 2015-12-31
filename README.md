This is a localserver Flask application for [spaced repetition](https://en.wikipedia.org/wiki/Spaced_repetition) learning. Currently it is still very much a work in process and not super user friendly. Most people will prefer [Anki](http://ankisrs.net/), a great and mature piece of of software. This project is mostly just written for me.

I'd been using Anki for a while, but I found myself wanting more custom features than I could easily squeeze out of it. More distressingly, I occasionally ran into a very difficult pinpoint bug with the scheduling. So I sat down, wrote this out, and have slowly been adding features as I go along.

It's been pretty useful for me so far in the ~5 months I've been studying with it. At some point in the future though, I'm probably going to drop this and do a complete re-write with electron or something.

Out of the box features include:
* Flashcards allow unrestricted HTML/CSS/Javascript.
* Code highlighting.
* Simple support for sound.
* Optional drawing area (ex. for drawing kanji)
* Easy to sync data (deck is contained in a single SQLite file).
* Runs completely locally (no internet connection required)

##Getting Started

This is a Flask application that requires SQLAlchemy and nothing else so the requirements.txt file is fairly short:

```
pip install -r requirements.txt
```

To run the app:

```
python run_local.py
```

The application will run on http://127.0.0.1:5000/ by default. Just head over to your browser and take a look. UI is kind of hacky still.

##Screenshots

Main menu:

![Main Menu](docs/screenshots/main_menu.png?raw=true)

Easy to practice drawing chinese characters:

![Study](docs/screenshots/study.png?raw=true)

Code highlighting:

![Highlighting](docs/screenshots/highlight.png?raw=true)