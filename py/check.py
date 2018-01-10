import urllib.request
import json
from time import sleep
import login
import whichweek
from datetime import date

rawhtml = urllib.request.urlopen("https://cfb-scoreboard-api.herokuapp.com/v1/date/" + whichweek.getweek()["last"][1])

data = json.loads(rawhtml.read().decode("utf-8"))

users = open('./users.json', 'r')
userdata = json.loads(users.read())

def checker(user):

    sleep(2)
    print("\033[H\033[2J")

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
    awayrank = ""
    homerank = ""

    for gameselection in userpicksdata:
        for game in data["games"]:

            #If the games are the same
            if gameselection["id"] == game["id"]:

                if int(game["awayTeam"]["rank"]) < 26:
                    awayrank = str(game["awayTeam"]["rank"]) + " "
                if int(game["homeTeam"]["rank"]) < 26:
                    homerank = str(game["homeTeam"]["rank"]) + " "

                print(awayrank + game["awayTeam"]["displayName"] + " at " + homerank + game["homeTeam"]["displayName"])
                awayrank = ""
                homerank = ""
                print(gameselection["spread"])
                
                #If the game is actually over
                if game["status"]["type"] == "STATUS_FINAL":

                    correct = False
                    
                    print("Final score:     " + game["homeTeam"]["abbreviation"], str(float(game["scores"]["home"])) + " - " + str(float(game["scores"]["away"])), game["awayTeam"]["abbreviation"])

                    #If the spread is tilted towards the home team
                    if gameselection["spread"].startswith(game["homeTeam"]["abbreviation"]):
                        favored = "home"
                        notfavored = "away"
                    else:
                        favored = "away"
                        notfavored = "home"

                    #If the favored team's score minus the spread is still better than the losing team
                    adjustedscore = float(game["scores"][favored]) + float(gameselection["spread"][len(game[favored + "Team"]["abbreviation"])+1:])

                    if adjustedscore >= float(game["scores"][notfavored]):

                        #If your pick (home or away) matches the favored team that covered the spread
                        if gameselection["pick"] == favored:
                            correct = True
                            wins += 1
                        else:
                            correct = False
                            losses += 1
                    else:

                        #If your pick (home or away) matches the favored team that did not cover the spread
                        if gameselection["pick"] == favored:
                            correct = False
                            losses += 1
                        else:
                            correct = True
                            wins += 1
                    
                    if favored == "home":
                        print("Adjusted score:  " + game["homeTeam"]["abbreviation"], str(adjustedscore) + " - " + str(float(game["scores"]["away"])), game["awayTeam"]["abbreviation"])
                    else:    
                        print("Adjusted score:  " + game["homeTeam"]["abbreviation"], str(float(game["scores"]["home"])) + " - " + str(adjustedscore), game["awayTeam"]["abbreviation"])

                    if correct:
                        print("\nYou got this game correct\n")
                    else:
                        print("\nYou got this game incorrect\n")

                elif game["status"]["type"] == "STATUS_SCHEDULED":
                    print("This game has not been played yet\n")
                    
                elif game["status"]["type"] == "STATUS_IN_PROGRESS" or game["status"]["type"] == "STATUS_HALFTIME":
                    print("This game is in progress\n")
                    print("The current score is\n" + game["awayTeam"]["abbreviation"], game["scores"]["away"], "-", game["scores"]["home"], game["homeTeam"]["abbreviation"] + "\n")

                else:
                    print("This game is in an unrecognized state.\n")

                input("Press enter to continue")
                print("\033[H\033[2J")

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
    print()

checker(login.login())
