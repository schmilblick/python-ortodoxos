# -*- coding: utf-8 -*-
from collections import defaultdict
import random
import codecs
import commands
import sys

markov = defaultdict(list)
STOP_WORD = "\n"

def add_to_brain(msg):
    pass

def get_random_line():
    f = open("training_text.txt", "r")
    # read how many lines file has
    a = commands.getoutput('wc -l training_text.txt')
    lines = int(a[0:a.find(' ')])
    # pick a random number between 0 and number of lines in file
    pick_one = random.randint(0, lines)
    # default output
    to_print = "jag är en dvärg"
    count = 0
    cur = f.readline()
    while cur:
        count += 1
        if pick_one == count:
            to_print = cur[:-1]
            break
        cur = f.readline()
    print >> sys.stderr, " get_random line returns type: %s" % type(to_print)
    return to_print


