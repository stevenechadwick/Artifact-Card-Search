import os
import requests
import json
import datetime

global PlaySet0r
PlaySet0r = {}
global PlaySet1r
PlaySet1r = {}
global PlaySet0
PlaySet0 = {}
global PlaySet1
PlaySet1 = {}
global Expiretime

def GetAPIData():

    global PlaySet0r
    global PlaySet1r
    global PlaySet0
    global PlaySet1
    global Expiretime

    PlaySet0r = requests.get("https://playartifact.com/cardset/00/").json()
    PlaySet1r = requests.get("https://playartifact.com/cardset/01/").json()

    Expiretime = PlaySet0r["expire_time"]

    with open('PlaySet0.json', 'w') as f:
        json.dump(requests.get(PlaySet0r["cdn_root"] + PlaySet0r["url"]).json(), f)
    with open('PlaySet1.json', 'w') as f:
        json.dump(requests.get(PlaySet1r["cdn_root"] + PlaySet1r["url"]).json(), f)

    with open('PlaySet0.json') as f:
        PlaySet0 = json.load(f)
    with open('PlaySet1.json') as f:
        PlaySet1 = json.load(f)

#PlaySet0 = requests.get(PlaySet0r["cdn_root"] + PlaySet0r["url"]).json()
#PlaySet1 = requests.get(PlaySet1r["cdn_root"] + PlaySet1r["url"]).json()

# Searches playsets for user inputted card name
def GetCardInfo():
    user_search = input("Card name: ")
    for card in PlaySet0["card_set"]["card_list"]:
        if (card["card_name"]["english"]).lower() == user_search.lower():
            return card
        else:
            for card in PlaySet1["card_set"]["card_list"]:
                if (card["card_name"]["english"]).lower() == user_search.lower():
                    return card

def APIExpire():
    if datetime.datetime.utcnow().timestamp() > Expiretime:
        return True

# Takes dictionary argument and prints relevant information
def GiveCardInfo(card):
    if bool(card):
        print("Name:" + " " + card.get("card_name")["english"])
        print("Card Type:" + " " + card.get("card_type"))
        print("Card Colour:" + " " + GetCardColour(card))
        if "mana_cost" in card.keys():
            print("Mana Cost:" + " " + str(card.get("mana_cost")))
        if "attack" in card.keys():
            print("Attack:" + " " + str(card.get("attack")))
        if "hit_points" in card.keys():
            print("Hit Points:" + " " + str(card.get("hit_points")))
        if bool(card.get("card_text")):
            print(card.get("card_text")["english"])
        else:
            GetCardAbility(card)
    else:
        print("Sorry that's not a valid card")
    if APIExpire():
        GetAPIData()
    GiveCardInfo(GetCardInfo())

# Checks what colour a card is to return in GiveCardInfo function
def GetCardColour(card):
    if "is_blue" in card.keys():
        return "Blue"
    if "is_black" in card.keys():
        return "Black"
    if "is_red" in card.keys():
        return "Red"
    if "is_green" in card.keys():
        return "Green"

# Gets abilities for hero cards as their text is not displayed the same as spells
def GetCardAbility(card):
    if bool(card.get("references")):
        for x in PlaySet1["card_set"]["card_list"]:
            if x["card_id"] == card["references"][1]["card_id"]:
                print(x.get("card_type") + ": " + x.get("card_text")["english"])
            if x["card_id"] == card["references"][0]["card_id"]:
                print("Signature Card:" + " " + x.get("card_name")["english"])

GetAPIData()
GiveCardInfo(GetCardInfo())
