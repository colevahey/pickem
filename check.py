import urllib.request
import json
from time import sleep
import hashlib
import adduser

rawhtml = urllib.request.urlopen("https://cfb-scoreboard-api.herokuapp.com/v1/date/20170923")

data = json.loads(rawhtml.read().decode("utf-8"))

users = open('users.json', 'r')
userdata = json.loads(users.read())

def login():
    uname = input("Username?\n>> ")
    password = input("Password?\n>> \033[8m")
    print("\033[0m")

    hash_object = hashlib.sha224(password.encode())
    hashpassword = hash_object.hexdigest()

    try:
        if userdata[uname]["password"] == hashpassword:
            print("Welcome back " + uname)
            print("Your current record is " + str(userdata[uname]["wins"]) + "-" + str(userdata[uname]["losses"]))
            print()
            sleep(3)
            tester(uname)
            #checker(uname)
        else:
            print("That password is incorrect")
            input("Try again? [Press enter to continue]")
            print()
            login()
    except KeyError:
        print("That user does not exist")
        create = input("Try again [Press enter] or create new user [Press c enter]?\n>> ")
        if create.lower() == "c":
            print()
            print("NEW USER:\n")
            adduser.main()
        else:
            print()
            login()

def checker(user):

    weeknumber = 1

    try:
        userpicks = open('./picks/picks' + str(weeknumber) + '.json', 'r')
        userpicksdata = json.loads(userpicks.read())[user]
    except FileNotFoundError:
        print("You have no picks for week " + str(weeknumber))

    for gameselection in userpicksdata:
        for game in data["games"]:
            if gameselection["id"] == game["id"]:
                print("For game " + game["awayTeam"]["displayName"] + " at " + game["homeTeam"]["displayName"] + " you chose " + gameselection["abbreviation"] + " with a spread of " + gameselection["spread"])

                if game["winner"] != None:
                    winnerlose = ["home","away"]
                    winnerlose.remove(game["winner"])
                    print("The winner of the game was " + game[game["winner"]+"Team"]["displayName"] + " by a score of " + game["scores"][game["winner"]] + " to " + game["scores"][winnerlose[0]] + ".")
                print()
            else:
                pass







def tester(user):

    weeknumber = 1

    try:
        userpicks = open('./picks/picks' + str(weeknumber) + '.json', 'r')
        userpicksdata = json.loads(userpicks.read())[user]
    except FileNotFoundError:
        print("You have no picks for week " + str(weeknumber))

    wins = 0
    losses = 0

    for gameselection in userpicksdata:
        for game in data["games"]:

            #testing
            #CHANGE THIS AFTER SATURDAY
            game["scores"]["home"] = "28"
            game["scores"]["away"] = "21"
            game["status"]["type"] = "STATUS_FINAL"

            #If the games are the same
            if gameselection["id"] == game["id"]:

                print(game["awayTeam"]["displayName"] + " at " + game["homeTeam"]["displayName"])
                print(gameselection["spread"])
                sleep(3)
                
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
                        print("The favored team covered the spread")

                        #If your pick (home or away) matches the favored team that covered the spread
                        if gameselection["pick"] == favored:
                            print("You got this pick correct\n")
                            wins += 1
                        else:
                            print("You got this pick incorrect\n")
                            losses += 1
                    else:
                        print("The favored team did not cover the spread")
                        
                        #If your pick (home or away) matches the favored team that did not cover the spread
                        if gameselection["pick"] == favored:
                            print("You got this pick incorrect\n")
                            losses += 1
                        else:
                            print("You got this pick correct\n")
                            wins += 1

                elif game["status"]["type"] == "STATUS_SCHEDULED":
                    print("This game has not been played yet\n")

                else:
                    print("This game is in progress\n")

    print("Your record this week was " + str(wins) + "-" + str(losses))


login()
