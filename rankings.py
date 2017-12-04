import json

users = open('./users.json', 'r')
userdata = json.loads(users.read())

def rank():

    print("\033[H\033[2J")

    rankings = {}

    for user in userdata:
        rankings.update({userdata[user]["wins"]/(userdata[user]["wins"]+userdata[user]["losses"]):user})

    for i in range(len(rankings)):
        print(str(i+1) + ": " + rankings[sorted(rankings)[::-1][i]] + " (" + str(sorted(rankings)[::-1][i])[:5] + ")")

if __name__ == '__main__':
    rank()
