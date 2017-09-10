import os
import re

#Curl the html from USAToday Odds Website as a string
rawhtml = os.popen("curl https://www.usatoday.com/sports/ncaaf/odds/").read()

#Find the start and end of the table with all the teams in it
starttable = re.search("<tbody", rawhtml).span()[0]
endtable = re.search("</tbody", rawhtml).span()[1]

print(starttable)
print(endtable)

print("THE TABLE LOOKS LIKE THIS:\n\n\n")

#Slice the html at the table start and end points
table = rawhtml[starttable:endtable]
print(table)

#Find "Penn State" in the table
pennstate = re.search("Penn State", table)
print(pennstate)

#Print the table where Penn State was found
print(table[pennstate.span()[0]:pennstate.span()[1]])
