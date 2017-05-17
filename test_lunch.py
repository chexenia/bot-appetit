# -*- coding: utf-8 -*- 
import sys
import pickle
import datetime
import arteclunch as artlu

def test_db_query(db, person, date):
    with open(db, 'rb') as f:
        lunch_db = pickle.load(f)
        msg = (lunch_db[date][person])
    return msg

if __name__=="__main__":
    if len(sys.argv) < 3:
        print "[Supported format]: db, person name, date"
        sys.exit()

    db = sys.argv[1]
    person = sys.argv[2].decode("utf-8")
    date = int(sys.argv[3])

    now = datetime.datetime.now()
    wday = int(now.strftime("%w"))

    print date, person
    query = test_db_query(db, person, date)

    for q in query:
        print q