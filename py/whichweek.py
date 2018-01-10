from datetime import date, timedelta
import json

def getweek():

    saturdays = json.load(open('saturdays.json','r'))
    inversesaturdays = {y:x for x,y in saturdays.items()}

    today = date.today()

    if today.weekday() == 5:
        nextsaturday = today + timedelta(days=7)
        lastsaturday = today
        nextsaturday = str(nextsaturday).replace("-","")
        lastsaturday = str(lastsaturday).replace("-","")

    elif today.weekday() == 6:
        nextsaturday = today + timedelta(days=6)
        lastsaturday = today - timedelta(days=1)
        nextsaturday = str(nextsaturday).replace("-","")
        lastsaturday = str(lastsaturday).replace("-","")

    else:
        nextsaturday = today + timedelta(days=abs(5-today.weekday()))
        lastsaturday = today - timedelta(days=abs(-2-today.weekday()))
        nextsaturday = str(nextsaturday).replace("-","")
        lastsaturday = str(lastsaturday).replace("-","")

    return {"next":[inversesaturdays[nextsaturday],nextsaturday],"last":[inversesaturdays[lastsaturday],lastsaturday]}

if __name__ == '__main__':

    print("Next Saturday is week " + getweek()["next"][0] + " on " + getweek()["next"][1])
    print("Last Saturday was week " + getweek()["last"][0] + " on " + getweek()["last"][1])
