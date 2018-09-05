import urllib.request
import json
import login
import whichweek
from datetime import date

rawhtml = urllib.request.urlopen("https://cfb-scoreboard-api.herokuapp.com/v1/date/" + whichweek.getweek()["last"][1])

data = json.loads(rawhtml.read().decode("utf-8"))

users = open('users.json', 'r')
userdata = json.loads(users.read())

def checker(user):

    try:
        userpicks = open('./picks/picks' + whichweek.getweek()["last"][0] + '.json', 'r')
        try:
            userpicksdata = json.loads(userpicks.read())[user]
        except KeyError:
            print("User " + user + " was either just added or has not made any picks for this week")
            exit()
    except FileNotFoundError:
        print("You have no picks for week " + whichweek.getweek()["last"][0])
        exit()

    wins = 0
    losses = 0

    for gameselection in userpicksdata:
        for game in data["games"]:

            #If the games are the same
            if gameselection["id"] == game["id"]:

                if int(game["awayTeam"]["rank"]) < 26:
                    awayrank = str(game["awayTeam"]["rank"]) + " "
                if int(game["homeTeam"]["rank"]) < 26:
                    homerank = str(game["homeTeam"]["rank"]) + " "

                #If the game is actually over
                if game["status"]["type"] == "STATUS_FINAL":

                    #If the spread is tilted towards the home team
                    if gameselection["spread"].startswith(game["homeTeam"]["abbreviation"]):
                        favored = "home"
                        notfavored = "away"
                    else:
                        favored = "away"
                        notfavored = "home"

                    #If the favored team's score minus the spread is still better than the losing team
                    if float(game["scores"][favored]) + float(gameselection["spread"][len(game[favored + "Team"]["abbreviation"])+1:]) >= float(game["scores"][notfavored]):

                        #If your pick (home or away) matches the favored team that covered the spread
                        if gameselection["pick"] == favored:
                            wins += 1
                        else:
                            losses += 1
                    else:
                        
                        #If your pick (home or away) matches the favored team that did not cover the spread
                        if gameselection["pick"] == favored:
                            losses += 1
                        else:
                            wins += 1

    print("Your record this week was " + str(wins) + "-" + str(losses))
    if date.today().weekday() != 5:
        try:
            weekrecord = userdata[user]["week" + whichweek.getweek()["last"][0]]
            print("Your record was already updated for this week.")
        except KeyError:
            userdata[user]["week" + whichweek.getweek()["last"][0]] = str(wins) + "-" + str(losses) 
            userdata[user]["wins"] += wins
            userdata[user]["losses"] += losses
    else:
        print("You cannot update your record on Saturday when some games may still be in progress.")

    users = open('users.json','w')
    users.write(json.dumps(userdata))
    print("Your overall record is " + str(userdata[user]["wins"]) + "-" + str(userdata[user]["losses"]))

checker(login.login())
