import urllib.request
import json

rawhtml = urllib.request.urlopen("https://cfb-scoreboard-api.herokuapp.com/v1/date/20170916")

data = rawhtml.read().decode("utf-8")

jsondata = json.loads(data)
print(jsondata)

for game in range(0, len(jsondata["games"])):
    print(jsondata["games"][game]["id"])
