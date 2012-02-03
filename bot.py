# -*- coding: utf-8 -*-
import random, re, sys
from twisted.words.protocols import irc
from twisted.internet import protocol
from brain import get_random_line
import cleverbot
from quotes import QuoteDb
from time import sleep
class GlebBot(irc.IRCClient):
    def __init__(self):
        #super(GlebBot, self).__init__()
        self.lineRate = 2
    def _get_nickname(self):
        return self.factory.nickname
    nickname = property(_get_nickname)

    def signedOn(self):
        self.join(self.factory.channel)
        print "Signed on as %s." % (self.nickname,)

    def joined(self, channel):
        print "Joined %s." % (channel,)

    def privmsg(self, user, channel, msg):
        if not user:
            return
        if self.nickname in msg:
            msg = re.compile(self.nickname + "[:,]* ?", re.I).sub('', msg)
            prefix = "%s: " % (user.split('!', 1)[0], )
        else:
            prefix = ''

        if msg.lower().startswith('!addquote'):
            bah = self.factory.quotes.add(msg, user, self.factory.channel)
            self.msg(self.factory.channel, "La till #%s" % bah)
        elif msg.lower().startswith('!quotesearch'):
            bah = self.factory.quotes.search(msg.replace("!quotesearch ", ""))
            print >> sys.stderr, "Searching and found %s search results" % len(bah)
            results = "Hittade %s resultat för '%s'\n" % (len(bah), msg.replace("!quotesearch ", ""))
            for b in bah:
                print >> sys.stderr, " Looping through search results - printing to %s " % self.factory.channel
                print >> sys.stderr, "    %s - %s @ %s" % b
                results += "%s - %s @ %s\n" % b
                print >> sys.stderr, "  sleeping..."
            self.msg(self.factory.channel, results)
        elif msg.lower().startswith('!quote'):
            bah = self.factory.quotes.random()
            self.msg(self.factory.channel, "%s - %s @ %s" % (bah[0], bah[1], bah[2]))
        elif msg.lower().startswith('midi'):
            ri = random.randint(1,3)
            if ri == 1:
                self.msg(self.factory.channel, 'hitler sa alltid: '+get_random_line())
            elif ri == 2:
                self.msg(self.factory.channel, 'hitler sa: '+get_random_line())
            elif ri == 3:
                self.msg(self.factory.channel, '%seller som hitler hitler sa, "%s"' (prefix, get_random_line()))
        elif prefix or random.random() <= self.factory.chattiness:
            print "Sending %s to cleverbot" % msg
            sentence = self.factory.cb.Ask(msg) # generate_sentence(msg, self.factory.chain_length, self.factory.max_words)
            print "  - got reply: %s" % sentence
            if sentence:
                self.msg(self.factory.channel, prefix + sentence)

class GlebBotFactory(protocol.ClientFactory):
    protocol = GlebBot

    def __init__(self, channel, nickname='Gleb', chain_length=3, chattiness=1.0, max_words=100000):
        self.channel = channel
        self.nickname = nickname
        self.chain_length = chain_length
        self.chattiness = chattiness
        self.max_words = max_words
        self.quotes = QuoteDb()
        self.cb = cleverbot.Session()
        self.lineRate = 2

    def clientConnectionLost(self, connector, reason):
        print "Lost connection (%s), reconnecting." % (reason,)
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "Could not connect: %s" % (reason,)
