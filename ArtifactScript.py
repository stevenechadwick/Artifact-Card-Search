import requests
import json

PlaySet0r = requests.get("https://playartifact.com/cardset/00/").json()
PlaySet1r = requests.get("https://playartifact.com/cardset/01/").json()

PlaySet0 = requests.get(PlaySet0r["cdn_root"] + PlaySet0r["url"]).json()
PlaySet1 = requests.get(PlaySet1r["cdn_root"] + PlaySet1r["url"]).json()

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

GiveCardInfo(GetCardInfo())
