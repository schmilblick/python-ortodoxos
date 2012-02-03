#!/usr/bin/env python
# encoding: utf-8
"""
quotes.py

Created by Fredrik Stark on 2011-09-10.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import sys
import os
from datetime import datetime
import MySQLdb

class QuoteDb(object):
    def disco(self):
        if hasattr(self, "db") and hasattr(self.db, "close"): 
            try:
                self.db.close()
            except:
                pass
        else:
            pass
    
    def get_cursor(self):
        try:
            if hasattr(self, "db") and hasattr(self.db, "close"): self.db.close()
        except:
            pass
        
        self.db = MySQLdb.connect(host = "localhost", user = "root", passwd = "H4rdum1d1?", db = "quote")
        return self.db.cursor()
        
    def add(self, msg, who, channel):
        cursor = self.get_cursor()
        msg = msg.replace("!addquote ", "")
        cursor.execute('INSERT INTO quote(q, who, channel, added_at) VALUES("%s", "%s", "%s", "%s")' % (msg, who, channel, datetime.now()))
        last_id = cursor.lastrowid
        self.disco()
        cursor.close()
        return last_id
        
    def search(self, term):
        cursor = self.get_cursor()
        cursor.execute("""SELECT q, who, channel, added_at FROM quote WHERE q LIKE '%%%s%%' OR who LIKE '%%%s%%' LIMIT 3""" % (term, term))
        retval = cursor.fetchall()
        lol = []
        for r in retval:
            lol.append(self.format_post(r))
        self.disco()
        cursor.close()
        return lol
    
    def format_post(self, retval):
        nick  = retval[1][:retval[1].find("!")] if "!" in retval[1] else retval[1]
        msg   = retval[0].replace("\n", " | ")
        added_at = retval[3] if retval[3] != "0000-00-00 00:00:00" else "a long time ago"
        return (msg, nick, added_at)

    def get(self, id):
        cursor = self.get_cursor()
        cursor.execute('SELECT q, who, channel, added_at FROM quote WHERE id = %d' % id)
        retval = cursor.fetchone()
        post = self.format_post(retval)
        self.disco()
        cursor.close()
        return post
    
    def random(self):
        cursor = self.get_cursor()
        cursor.execute('SELECT id FROM quote ORDER BY RAND() LIMIT 1')
        retval = cursor.fetchone()
        post = self.get(retval[0])
        self.disco()
        cursor.close()
        return post
        
        