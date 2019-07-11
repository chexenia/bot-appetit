#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import sys
import pickle
import openpyxl
import arteclunch as arl
import os
import time

def generate_personal_reply(order, name, verbose=False):
    reply = [u""]
    
    for item in order:
        reply.append(item[0] + ' - ' + str(int(float(item[2])))) #dish + count 
        if verbose and item[1]:
            reply.append("* " + item[1])

    return reply

def serialize_sheet(wb, sheet_name, meal, db, motto):
    ws = wb[sheet_name]

    splits = arl.split_days(ws)
    persons = arl.enumerate_persons(ws)

    db[meal] = {day : {} for day in splits}

    for name, col in persons:
        for day in splits:
            print(name, day)
            order = arl.get_order(ws, splits, day, col)
            reply = generate_personal_reply(order, name.strip(), verbose=False)
            db[meal][day][name.strip()] = reply + [u"", motto]

if __name__=="__main__":
    start = time.time()
    if len(sys.argv) < 2:
        print "Incorrect format: pass at least the xlsx path."
        sys.exit()

    fname = sys.argv[1]
    motto = sys.argv[2] if len(sys.argv) >= 3 else u""
    wb = openpyxl.load_workbook(filename = fname, read_only=True)

    db = {arl.BREAKFAST : {}, arl.LUNCH : {}}
    print(db)
    
    if os.path.exists(arl.MEAL_DB):
        os.remove(arl.MEAL_DB)

    #serialize_sheet(wb, u'Завтраки', arl.BREAKFAST, db, motto)
    serialize_sheet(wb, u'Лист1', arl.LUNCH, db, motto)

    with open(arl.MEAL_DB, 'wb') as f:
        pickle.dump(db, f)

    f.close()

    print('total dump', time.time() - start, 'sec')