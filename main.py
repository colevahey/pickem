import urllib.request

rawhtml = urllib.request.urlopen("https://cfb-scoreboard-api.herokuapp.com/v1/date/20170916")

data = rawhtml.read().decode("utf-8")
print(data)
