from datetime import date, timedelta
import calendar
import json

def saturdaysfromcalendar():
    today = date.today().day
    calendar.setfirstweekday(calendar.SATURDAY)
    saturdaysfromcal = []
    lastsat = 0
    nextsat = 0
    for week in calendar.monthcalendar(date.today().year,date.today().month):
        if week[0] != 0:
            saturdaysfromcal.append(week[0])
    for day in saturdaysfromcal:
        if day != 0:
            if day + 7 < today or day - 7 > today:
                pass
            else:
                if today - day >= 0:
                    lastsat = day
                else:
                    nextsat = day
    if lastsat == 0:
        if date.today().month != 1:
            lastsat = calendar.monthcalendar(date.today().year, date.today().month-1)[-1][0]
        else:
            lastsat = calendar.monthcalendar(date.today().year-1,12)[-1][0]
    if nextsat == 0:
        if date.today().month != 12:
            nextsat = calendar.monthcalendar(date.today().year, date.today().month+1)[1][0]
        else:
            nextsat = calendar.monthcalendar(date.today().year+1, 1)[1][0]
            
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

    saturdaysfromcalendar()

    print("Next Saturday is week " + getweek()["next"][0] + " on " + getweek()["next"][1])
    print("Last Saturday was week " + getweek()["last"][0] + " on " + getweek()["last"][1])
