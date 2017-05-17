#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import sys
import pickle
import openpyxl
import arteclunch

def make_person_string(order, name, verbose=False):
    reply = [u"Your order is waiting:"]
    
    for item in order:
        reply.append(item[0])
        if verbose and item[1]:
            reply.append("* " + item[1])

    return reply

if __name__=="__main__":
    if len(sys.argv) < 3:
        print "Incorrect format: pass at least the xlsx and pickle filename."
        sys.exit()

    fname = sys.argv[1]
    fname_out = sys.argv[2]
    motto = sys.argv[3] if len(sys.argv) >= 4 else u""
    wb = openpyxl.load_workbook(filename = fname, read_only=True)
    ws = wb.active

    splits = arteclunch.split_days(ws)
    persons = arteclunch.enumerate_persons(ws)

    db = {day : {} for day in splits}

    for name, col in persons:
    	for day in splits:
    		order = arteclunch.get_order(ws, splits, day, col)
    		reply = make_person_string(order, name.strip(), verbose=True)
    		db[day][name.strip()] = reply + [u"", motto]

    with open(fname_out, 'wb') as f:
    	pickle.dump(db, f)
