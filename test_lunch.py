# -*- coding: utf-8 -*- 
import sys
import pickle
import datetime
import arteclunch as artlu

def test_db_query(db, person, date):
    with open(db, 'rb') as f:
        food_db = pickle.load(f)
        msg = (food_db[date][person])
    return msg

def test_query(person, date):
    now = datetime.datetime.now()
    wday = int(now.strftime("%w"))
    hday = int(now.strftime("%H"))
    print(hday)
    meal = ""
    if hday > 9 and hday < 12:
        meal = artlu.BREAKFAST_DB
    else:
        meal = artlu.LUNCH_DB
    msg = test_db_query(meal, person, date)
    return meal, msg

def get_order(person):
    now = datetime.datetime.now()
    wday = int(now.strftime("%w"))
    hday = int(now.strftime("%H"))
    meal = ""
    if hday > 9 and hday < 12:
        meal = artlu.BREAKFAST_DB
    else:
        meal = artlu.LUNCH_DB

    msg = u'Not understood'

    with open(meal, 'rb') as f:
        meal_db = pickle.load(f)
        if wday not in meal_db:
            msg = u"No work - no food. That's the law."
        elif query not in meal_db[wday]:
            msg = u"You did not order."
        else:
            msg = u"\n".join(meal_db[wday][person])

    return msg

if __name__=="__main__":
    if len(sys.argv) < 2:
        print "[Supported format]: person name, week date"
        sys.exit()

    person = sys.argv[1].decode("utf-8")
    date = int(sys.argv[2])

    now = datetime.datetime.now()
    wday = int(now.strftime("%w"))

    print (date, person)
    meal, query = test_query(person, date)

    print(meal)
    for q in query:
        print (q)