import urllib.request
import json
from time import sleep
import login
import whichweek

rawhtml = urllib.request.urlopen("https://cfb-scoreboard-api.herokuapp.com/v1/date/" + whichweek.getweek()["next"][1])

data = json.loads(rawhtml.read().decode("utf-8"))

def selections(user):

    userselections = [] 

    for game in data["games"]:

        gameselections = makeselections(game)

        while not gameselections:
            gameselections= makeselections(game)
            
        userselections.append(gameselections)

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
        print("Selections aborted")
        userpicks.write("{}")

def makeselections(game):

    awayrank = ""
    homerank = ""

    if game["odds"]["spread"] != "N/A":

        print("\033[H\033[2J")
        if int(game["awayTeam"]["rank"]) < 26:
            awayrank = str(game["awayTeam"]["rank"]) + " "
        if int(game["homeTeam"]["rank"]) < 26:
            homerank = str(game["homeTeam"]["rank"]) + " "

        print(awayrank + game["awayTeam"]["displayName"] + " at " + homerank + game["homeTeam"]["displayName"])
        awayrank = ""
        homerank = ""
        print(game["odds"]["spread"])
        selection = input("\nWho do you select? (A/H)\n>> ").title()
        if selection == "A":
            print("You selected the " + game["awayTeam"]["displayName"])
            input("Press enter to continue")
            return {"id":game["id"],"pick":"away","spread":game["odds"]["spread"]}
        elif selection == "H":
            print("You selected " + game["homeTeam"]["displayName"])
            input("Press enter to continue")
            return {"id":game["id"],"pick":"home","spread":game["odds"]["spread"]}
        else:
            print("That pick is invalid.")
            input("Press enter to continue")
            return False
    else:
        print("The odds for the games have not come out for this week.")
        exit()

selections(login.login())
