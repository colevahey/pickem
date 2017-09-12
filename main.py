import urllib.request
import json

rawhtml = urllib.request.urlopen("https://cfb-scoreboard-api.herokuapp.com/v1/date/20170916")

data = json.loads(rawhtml.read().decode("utf-8"))

#For each game in the database for that week
for game in range(0, len(data["games"])):

    #If the game has a spread
    if data["games"][game]["odds"]["spread"] != "N/A":

        #Print the teams playing in the game
        print(data["games"][game]["homeTeam"]["displayName"] + " vs. " + data["games"][game]["awayTeam"]["displayName"])

        #Print the spread of the game
        print(data["games"][game]["odds"]["spread"])
        print()
