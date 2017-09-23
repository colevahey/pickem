import urllib.request
import json
from time import sleep
import login

rawhtml = urllib.request.urlopen("https://cfb-scoreboard-api.herokuapp.com/v1/date/20170923")

data = json.loads(rawhtml.read().decode("utf-8"))

def selections(user):

    userselections = [] 
    awayrank = ""
    homerank = ""

    for game in data["games"]:
        if game["odds"]["spread"] != "N/A":
            if int(game["awayTeam"]["rank"]) < 26:
                awayrank = str(game["awayTeam"]["rank"]) + " "
            if int(game["homeTeam"]["rank"]) < 26:
                homerank = str(game["homeTeam"]["rank"]) + " "

            print(awayrank + game["awayTeam"]["displayName"] + " at " + homerank + game["homeTeam"]["displayName"])
            print(game["odds"]["spread"])
            selection = input("Who do you select? (A/H)\n>> ").title()
            if selection == "A":
                print("You selected the " + game["awayTeam"]["displayName"])
                userselections.append({"id":game["id"],"pick":"away","spread":game["odds"]["spread"]})
            elif selection == "H":
                print("You selected " + game["homeTeam"]["displayName"])
                userselections.append({"id":game["id"],"pick":"home","spread":game["odds"]["spread"]})
            else:
                print("That pick is invalid. You have to start over now.")
                input("Press enter to continue")
                userselections = []
                break
                selections(user)

    try:
        userpicks = open('./picks/picks1.json', 'r')
        userpicksdata = json.loads(userpicks.read())
    except FileNotFoundError:
        userpicksdata = {}

    userpicksdata.update({user:userselections})

    userpicks = open('./picks/picks1.json', 'w')

    if userselections != []:
        print(userselections)
        userpicks.write(json.dumps(userpicksdata))
    else:
        print("All of the games are either in progress or over.")

selections(login.login())
