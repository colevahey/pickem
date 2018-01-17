#!/usr/bin/env python3

import urllib.request

raw = urllib.request.urlopen("https://cfb-scoreboard-api.herokuapp.com/v1/date/20171028")
jsondata = raw.read().decode("utf-8")

with open("data.js","w") as jsonfile:
    jsonfile.write("jsondata = " + jsondata) 

print(jsondata)


