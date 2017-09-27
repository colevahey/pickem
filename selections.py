import urllib.request
import json
from time import sleep
import login
import whichweek

rawhtml = urllib.request.urlopen("https://cfb-scoreboard-api.herokuapp.com/v1/date/" + whichweek.getweek()["next"][1])

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
            awayrank = ""
            homerank = ""
            print(game["odds"]["spread"])
            selection = input("Who do you select? (A/H)\n>> ").title()
            if selection == "A":
                print("You selected the " + game["awayTeam"]["displayName"])
                print()
                userselections.append({"id":game["id"],"pick":"away","spread":game["odds"]["spread"]})
            elif selection == "H":
                print("You selected " + game["homeTeam"]["displayName"])
                print()
                userselections.append({"id":game["id"],"pick":"home","spread":game["odds"]["spread"]})
            else:
                print("That pick is invalid. You have to start over now.")
                input("Press enter to continue")
                userselections = []
                selections(user)

    try:
        userpicks = open('./picks/picks' + whichweek.getweek()["next"][0] + '.json', 'r')
        userpicksdata = json.loads(userpicks.read())
    except FileNotFoundError:
        userpicksdata = {}

    userpicksdata.update({user:userselections})

    userpicks = open('./picks/picks' + whichweek.getweek()["next"][0] + '.json', 'w')

    if userselections != []:
        print(userselections)
        userpicks.write(json.dumps(userpicksdata))
    else:
        print("Something is wrong...")

selections(login.login())
