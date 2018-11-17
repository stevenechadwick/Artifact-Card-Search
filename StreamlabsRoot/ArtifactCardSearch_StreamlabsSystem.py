import urllib
import json
import os
import codecs
import sys
import re
import datetime

# Streamlabs boilerplate script info
ScriptName = "Artifact Card Search"
Website = "https://github.com/some_fake_thing"
Description = "Card Search"
Creator = "us"
Version = "1.1.0"

SETTINGS_CARD_NAME = "CardName"
SETTINGS_CARD_TYPE = "CardType"
SETTINGS_CARD_TEXT = "CardText"
SETTINGS_CARD_RARITY = "Rarity"
SETTINGS_CARD_COLOUR = "Colour"
SETTINGS_CARD_ATTACK = "Attack"
SETTINGS_CARD_ARMOUR = "Armour"
SETTINGS_CARD_HEALTH = "Health"
SETTINGS_CARD_SIGNATURE = "SignatureCard"
SETTINGS_CARD_COST = "Cost"

MandatorySettings = [SETTINGS_CARD_NAME, SETTINGS_CARD_TYPE, SETTINGS_CARD_TEXT, 
        SETTINGS_CARD_RARITY, SETTINGS_CARD_COLOUR, SETTINGS_CARD_ATTACK, 
        SETTINGS_CARD_ARMOUR, SETTINGS_CARD_HEALTH, SETTINGS_CARD_SIGNATURE, SETTINGS_CARD_COST]

PlaySet0Meta = {}
PlaySet1Meta = {}
PlaySet0 = {}
PlaySet1 = {}
Settings = {}

def Debugtochat(msg):
    var_exists = 'Parent' in locals() or 'Parent' in globals()
    if var_exists:
        Parent.SendStreamMessage(msg)
    else:
        print msg

def Debugtolog(msg):
    var_exists = 'Parent' in locals() or 'Parent' in globals()
    if var_exists:
        Parent.Log("Script Debug", msg)
    else:
        print msg

#---------------------------
#   [Required] Initialize Data (Only called on load)
#---------------------------
def Init():
    global PlaySet0Meta
    global PlaySet1Meta
    global PlaySet0
    global PlaySet1

    Debugtochat("Initializing ArtifactCardSearch")

    Dirname = os.path.dirname(__file__)    
    LoadSettings()


    PlaySet0Meta = LoadAPIData(os.path.join(Dirname, 'PlaySet0Meta.json'),"https://playartifact.com/cardset/00/")
    PlaySet1Meta = LoadAPIData(os.path.join(Dirname, 'PlaySet1Meta.json'),"https://playartifact.com/cardset/01/")

    if APIExpired(PlaySet0Meta['expire_time']):
        PlaySet0Meta = DownloadAndCache(os.path.join(Dirname, 'PlaySet0Meta.json'),"https://playartifact.com/cardset/00/")
        PlaySet0 = DownloadAndCache(os.path.join(Dirname, 'PlaySet0.json'), PlaySet0Meta["cdn_root"] + PlaySet0Meta["url"])
    else:
        LoadAPIData(os.path.join(Dirname, 'PlaySet0.json'), PlaySet0Meta["cdn_root"] + PlaySet0Meta["url"])

    if APIExpired(PlaySet1Meta['expire_time']):
        PlaySet1Meta = DownloadAndCache(os.path.join(Dirname, 'PlaySet1Meta.json'),"https://playartifact.com/cardset/01/")
        PlaySet1 = DownloadAndCache(os.path.join(Dirname, 'PlaySet1.json'), PlaySet1Meta["cdn_root"] + PlaySet1Meta["url"])    
    else:
        LoadAPIData(os.path.join(Dirname, 'PlaySet1.json'), PlaySet1Meta["cdn_root"] + PlaySet1Meta["url"])


    # try:
    #     with open(os.path.join(Dirname, 'PlaySet0.json')) as f:
    #         PlaySet0 = json.load(f)
    #     Debugtolog("Playset0 cache loaded")
    # except:
    #     Debugtolog("Downloading Playset0 JSON Data")
    #     PlaySet0Meta = DownloadJSONBlob("https://playartifact.com/cardset/00/")
    #     PlaySet0 = DownloadJSONBlob(PlaySet0Meta["cdn_root"] + PlaySet0Meta["url"])

    #     with open(os.path.join(Dirname, 'PlaySet0.json'), 'w') as f:
    #         json.dump(PlaySet0, f)

    # try:
    #     with open(os.path.join(Dirname, 'PlaySet1.json')) as f:
    #         PlaySet1 = json.load(f)
    #     Debugtolog("Playset1 cache loaded")
    # except:
    #     Debugtolog("Downloading Playset1 JSON Data")
    #     PlaySet1Meta = DownloadJSONBlob("https://playartifact.com/cardset/01/")
    #     PlaySet1 = DownloadJSONBlob(PlaySet1Meta["cdn_root"] + PlaySet1Meta["url"])
        
    #     with open(os.path.join(Dirname, 'PlaySet1.json'), 'w') as f:
    #         json.dump(PlaySet1, f)

    Debugtolog("JSON data loaded")


#---------------------------
#   [Required] Execute Data / Process messages
#---------------------------
def Execute(data):
    if data.IsChatMessage():
        Parent.SendStreamMessage(SanitizeText((ProcessChatMessage(data.Message))))

#---------------------------
#   [Required] Tick method (Gets called during every iteration even when there is no incoming data)
#---------------------------
def Tick():

    return

#---------------------------
#   [Optional] Reload Settings (Called when a user clicks the Save Settings button in the Chatbot UI)
#---------------------------
def ReloadSettings(jsonData):
    LoadSettings()
    return

#---------------------------
#   [Optional] Unload (Called when a user reloads their scripts or closes the bot / cleanup stuff)
#---------------------------
def Unload():
    Debugtochat("Unload")
    return

def DownloadJSONBlob(url):
    var_exists = 'Parent' in locals() or 'Parent' in globals()
    if var_exists:
        req = Parent.GetRequest(url, {})
    else:
        req = urllib.urlopen(url)

    # Built in requests function adds another layer to JSON object
    json_dict = json.loads(req)
    apiset = json.loads(json_dict['response'])   
    return apiset

def ProcessChatMessage(chatmessage):
    result = re.match('\[\[(.*?)\]\]', chatmessage)
    if result is None:
        return ''
    cardname = result.group(1)
    card, playset = GetCardInfo(cardname)
    return GiveCardInfo(card, playset)

# Searches playsets for user inputted card name
def GetCardInfo(cardname):
    for card in PlaySet0["card_set"]["card_list"]:
        if (card["card_name"]["english"]).lower() == cardname.lower():
            return card, PlaySet0
        else:
            for card in PlaySet1["card_set"]["card_list"]:
                if (card["card_name"]["english"]).lower() == cardname.lower():
                    return card, PlaySet1

# Takes dictionary argument and prints relevant information
def GiveCardInfo(card, playset):
    cardinfo = ""
    if bool(card):
        if Settings[SETTINGS_CARD_NAME]:
            cardinfo += "Name: " + card.get("card_name")["english"] + " || "
        if Settings[SETTINGS_CARD_TYPE]:
            cardinfo += "Card Type: " + card.get("card_type") + " || "
        if bool(GetCardColour(card)) and Settings[SETTINGS_CARD_COLOUR]:
            cardinfo += "Card Colour: " + GetCardColour(card) + " || "
        if "mana_cost" in card.keys() and Settings[SETTINGS_CARD_COST]:
            cardinfo += "Mana Cost: " + str(card.get("mana_cost")) + " || "
        if "attack" in card.keys() and Settings[SETTINGS_CARD_ATTACK]:
            cardinfo += "Attack: " + str(card.get("attack")) + " || "
        if "armor" in card.keys() and Settings[SETTINGS_CARD_ARMOUR]:
            cardinfo += "Armour: " + str(card.get("armor")) + " || "
        if "hit_points" in card.keys() and Settings[SETTINGS_CARD_HEALTH]:
            cardinfo += "Hit Points: " + str(card.get("hit_points")) + " || "
        if bool(card.get("card_text")) and Settings[SETTINGS_CARD_TEXT]:
            cardinfo += card.get("card_text")["english"] + " || "
        if card.get("card_type") == "Hero" and Settings[SETTINGS_CARD_SIGNATURE]:
            cardinfo = GetCardAbility(card, cardinfo, playset)
    else:
        Debugtochat("Sorry that's not a valid card")
    return cardinfo

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
def GetCardAbility(card, cardinfo, playset):
    if bool(card.get("references")):
        for x in playset["card_set"]["card_list"]:
            if x["card_id"] == card["references"][0]["card_id"]:
                cardinfo += "Signature Card: " + x.get("card_name")["english"] + " || "
            if x["card_id"] == card["references"][0]["card_id"]:
                cardinfo += x.get("card_type") + ": " + x.get("card_text")["english"] + " || " 

    return cardinfo

def SanitizeText(text):
    tag_re = re.compile(r'<[^>]+>')
    return tag_re.sub(" ", text)

def LoadSettings():
    Dirname = os.path.dirname(__file__)
    filename = os.path.join(Dirname, "Settings\settings.json")
    
    try:
        with codecs.open(filename, encoding="utf-8-sig", mode="r") as f:
            settingsdict = json.load(f, encoding="utf-8")
    except Exception as e:
        print e
        settingsdict = {}

    for x in MandatorySettings:
        if x not in settingsdict:
            settingsdict[x] = False

    global Settings
    Settings = settingsdict

def LoadAPIData(filename, url):
    # If JSON file is cached, load cache
    # Otherwise, download JSON from API and update cache
    try:
        with open(filename) as f:
            JSONData = json.load(f)
        Debugtolog(filename + " cache loaded")
    except:
        JSONData = DownloadAndCache(filename, url)
    return JSONData

def DownloadAndCache(filename, url):
    Debugtolog("Downloading " + filename + " JSON Data")
    JSONData = DownloadJSONBlob(url)
    
    with open(filename, 'w') as f:
        json.dump(JSONData, f)
    return JSONData

def APIExpired(Expiretime):
    return datetime.datetime.utcnow() > datetime.datetime.utcfromtimestamp(Expiretime)
