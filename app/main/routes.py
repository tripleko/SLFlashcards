from flask import render_template, redirect, url_for, request, jsonify
from ..models import Deck, Flashcard, Interval_pref
from . import main
from .. import db
import json

from datetime import datetime, timedelta

#TODO, move helper functions unrelated to the routes to a separate file.

#Returns the next card to be studied in a deck, or None.
def getNextCard(deck):
    card = None

    if Deck.query.filter_by(deck_name=deck).first() is not None:
        all_card = Flashcard.query.filter_by(deck_name=deck)
        for i in range(1, 4):
            wait_time = Interval_pref.query.filter_by(interval=i).first().wait_time
            i_cards = all_card.filter_by(interval=i).all()
            for temp_card in i_cards:
                if (datetime.now() - temp_card.last_studied) >= wait_time:
                    card = temp_card
                    break 

            if card is not None:
                break

        if card is None:
            for i in range(0, 1):
                wait_time = Interval_pref.query.filter_by(interval=i).first().wait_time
                i_cards = all_card.filter_by(interval=i).all()
                for temp_card in i_cards:
                    if (datetime.now() - temp_card.last_studied) >= wait_time:
                        card = temp_card
                        break 

                if card is not None:
                    break

        if card is None:
            for i in range(4, 36):
                wait_time = Interval_pref.query.filter_by(interval=i).first().wait_time
                i_cards = all_card.filter_by(interval=i).all()
                for temp_card in i_cards:
                    if (datetime.now() - temp_card.last_studied) >= wait_time:
                        card = temp_card
                        break 

                if card is not None:
                    break
    return card

#Returns the number of cards available for study in a deck.
def countToStudy(deck):
    count = 0

    if Deck.query.filter_by(deck_name=deck).first() is not None:
        all_card = Flashcard.query.filter_by(deck_name=deck).all()
        for card in all_card:
            wait_time = Interval_pref.query.filter_by(interval=card.interval).first().wait_time
            if (datetime.now() - card.last_studied) >= wait_time:
                count += 1

    return count

@main.route("/")
def index():
    deck_all = Deck.query.all()
    deck_list = []
    for row in deck_all:
        priority_count = 0
        priority_count += Flashcard.query.filter_by(deck_name=row.deck_name).filter_by(interval=0).count()
        priority_count += Flashcard.query.filter_by(deck_name=row.deck_name).filter_by(interval=1).count()
        priority_count += Flashcard.query.filter_by(deck_name=row.deck_name).filter_by(interval=2).count()

        temp = {"deck_tier": row.deck_tier,
                "deck_name": row.deck_name,
                "total_count": Flashcard.query.filter_by(deck_name=row.deck_name).count(),
                "to_study_count": countToStudy(row.deck_name),
                "priority_count": priority_count}
        deck_list.append(temp)

    return render_template("index.html", deck_list=deck_list)

#Used to edit existing cards or add a new one.
@main.route("/ajax/editcard", methods=["POST"])
def ajax_editcard():
    data_dict = request.get_json()
    #print(data_dict)

    return_dict = {"error": False}

    if "old_front" not in data_dict:
        return_dict = {"error": True,
                       "error_msg": "old_front was not sent in request data!"}
        return jsonify(return_dict)

    if data_dict["new_front"] == "":
        return_dict = {"error": True,
                       "error_msg": "Front of card can't be blank!"}
        return jsonify(return_dict)

    #Handle special case where this is a new card.
    if data_dict["old_front"] == "":
        new_card = Flashcard(front=data_dict["new_front"],
                             back=data_dict["new_back"],
                             deck_name=data_dict["deck_name"],
                             initially_created=datetime.now(),
                             last_edited=datetime.now(),
                             last_studied=datetime.now() - timedelta(hours=1),
                             interval=0,
                             card_type=data_dict["card_type"],
                             sound_back=data_dict["sound_back"],
                             sound_front=data_dict["sound_front"])
        db.session.add(new_card)
        db.session.commit()
        print("Value of card cardtype: ", data_dict["card_type"])
        #print Flashcard(data_dict["new_front"])
        return jsonify(return_dict)

    edit_card = Flashcard.query.filter_by(front=data_dict["old_front"]).first()

    if edit_card is None:
        return_dict = {"error": True}
        return jsonify(return_dict)

    if data_dict["minor_edit"] is not True:
        edit_card.interval = 0
        edit_card.last_studied = datetime.now() - timedelta(hours=1)

    edit_card.front = data_dict["new_front"]
    edit_card.back = data_dict["new_back"]
    edit_card.last_edited = datetime.now()
    edit_card.card_type = data_dict["card_type"]
    edit_card.sound_back = data_dict["sound_back"]
    edit_card.sound_front = data_dict["sound_front"]
    
    db.session.commit()

    return jsonify(return_dict)

#Used by the study page to update intervals only.
@main.route("/ajax/updatecard", methods=["POST"])
def ajax_updatecard():
    data_dict = request.get_json()
    edit_card = Flashcard.query.filter_by(front=data_dict["front"]).first()

    edit_card.interval = data_dict["interval"]
    if(data_dict["last_studied"] == 0):
        edit_card.last_studied = datetime.now()
    else:
        edit_card.last_studied = data_dict["last_studied"]

    db.session.commit()

    card = getNextCard(data_dict["deck_name"])
    return_dict = None

    if(card is not None):
        return_dict = {"card_front": card.front,
        "card_back": card.back,
        "last_studied": card.last_studied,
        "interval": card.interval}

    #NEGATIVE value interval indicates there is no card to return.
    else:
        return_dict = {"interval": -1}

    return jsonify(**return_dict)


@main.route("/study/<deck>/")
def study(deck):
    deck_exists = False
    deck_total_cards = 0
    if Deck.query.filter_by(deck_name=deck).first() is not None:
        deck_exists=True
        deck_total_cards = Deck.query.filter_by(deck_name=deck).count()   

    card = getNextCard(deck)

    return render_template("study.html", deck=deck,
                            deck_total_cards=deck_total_cards,
                            deck_exists=deck_exists, card=card)


@main.route("/edit/<deck>/")
def edit(deck):
    deck_exists=False

    if Deck.query.filter_by(deck_name=deck).first() is not None:
        deck_exists=True

        card_all = Flashcard.query.filter_by(deck_name=deck).all()
        card_list = []
        for row in card_all:
            temp = {"front": row.front,
                    "back": row.back,
                    "deck_name": row.deck_name,
                    "initially_created": row.initially_created,
                    "last_edited": row.last_edited,
                    "last_studied": row.last_studied,
                    "interval": row.interval,
                    "card_type": row.card_type,
                    "sound_back": row.sound_back,
                    "sound_front": row.sound_front}

            card_list.append(temp)

    return render_template("edit.html", deck=deck, deck_exists=deck_exists, card_list=card_list)

#TODO: This is a temporary route. Should combine functionality into one edit route later.
@main.route("/ajax/intervaledit", methods=["POST"])
def intervaldb():
    if len(request.json) <= 0:
        return "Failure. No cards found."

    card_query = Flashcard.query.filter_by(deck_name=request.json[0]["deck"])

    for row in request.json:
        edit_row = card_query.filter_by(front=row["front"]).first()
        if edit_row is None:
            continue
        if row["to_delete"]:
            db.session.delete(edit_row)
        else:
            edit_row.interval = row["interval"]

    db.session.commit()

    return "Success"


#TODO: This is a temporary route. Should combine functionality into one edit route later.
#Since I'm basically the only user of this right now, I'm rolling with this somewhat half-assed solution.
@main.route("/intervaledit/<deck>/")
def intervaledit(deck):
    card_list = []

    deck_exists=False

    if Deck.query.filter_by(deck_name=deck).first() is not None:
        deck_exists=True

        card_all = Flashcard.query.filter_by(deck_name=deck).all()
        card_list = []
        for row in card_all:
            temp = {"interval": row.interval,
                    "front": row.front,
                    "back": row.back,
                    "last_studied": row.last_studied}

            card_list.append(temp)

    return render_template("intervaledit.html", deck_exists=deck_exists, card_list=card_list, deck=deck)


@main.route("/ajax/editdeck", methods=["POST"])
def editdb():
    for row in request.json:
        if row["deck_name"].strip() == "":
            continue

        #Indicates this is a new deck.
        if row["orig_name"].strip() == "":
            #Check if it's up for deletion before doing anything else.
            if row["to_delete"] == True:
                continue
            else:
                db.session.add(Deck(deck_name=row["deck_name"], deck_tier=row["deck_tier"]))
                continue

        edit_row = Deck.query.filter_by(deck_name=row["orig_name"]).first()

        #Only allow deletes on empty decks for now.
        if row["to_delete"] == True:
            if Flashcard.query.filter_by(deck_name=row["orig_name"]).count() == 0:
                db.session.delete(edit_row)

        else:
            fc = Flashcard.query.filter_by(deck_name=row["orig_name"]).all()

            for card in fc:
                card.deck_name = row["deck_name"]

            edit_row.deck_name = row["deck_name"]
            edit_row.deck_tier = row["deck_tier"]

    db.session.commit()
    return "Success"


@main.route("/managedecks")
def managedecks():
    deck_list = []
    for row in Deck.query.all():
        temp = {"deck_tier": row.deck_tier,
                "deck_name": row.deck_name,
                "total_count": Flashcard.query.filter_by(deck_name=row.deck_name).count()}
        deck_list.append(temp)

    return render_template("managedecks.html", deck_list=deck_list)