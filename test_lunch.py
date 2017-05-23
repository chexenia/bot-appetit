# -*- coding: utf-8 -*- 
import sys
import datetime
import arteclunch as arl
import pickle
from pytz.gae import pytz

def test_db_query(person, wday, hday):
    return arl.reply_order(person, wday, hday)

def print_db():
    with open(arl.MEAL_DB, 'rb') as f:
        meal_db = pickle.load(f)
        for meal in meal_db:
            print(meal.encode('utf-8'))
            for wday in meal_db[meal]:
                print(wday)
                for person in meal_db[meal][wday]:
                    print(person.encode('utf-8'))
                    print(meal_db[meal][wday][person])

    f.close()

if __name__=="__main__":
    if len(sys.argv) < 3:
        print "[Supported format]: person name, week date, hour of the day"
        sys.exit()

    person = sys.argv[1].decode("utf-8")
    wday = int(sys.argv[2])
    hday = int(sys.argv[3])

    reply = test_db_query(person, wday, hday)
    print(datetime.datetime.now(pytz.timezone('Europe/Moscow')))
    print(reply)
    #print_db()