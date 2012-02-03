# -*- coding: utf-8 -*-
import os
import sys
from twisted.internet import reactor
from bot import GlebBotFactory
from brain import add_to_brain

if __name__ == "__main__":
    try:
        chan = sys.argv[1]
        nick = sys.argv[2]
    except IndexError:
        print "Please specify a channel name."
        print "Example:"
        print "  python main.py alternativet"
    reactor.connectTCP('stockholm.se.quakenet.org', 6667, GlebBotFactory('#' + chan, nick, 2, chattiness=0.06))
    reactor.run()
