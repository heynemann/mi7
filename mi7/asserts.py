#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''Module with all the Assertions'''

class Assertion(object):
    def __init__(self, agent):
        self.agent = agent

class HasSeenAssertion(Assertion):
    def __init__(self, agent, target):
        Assertion.__init__(self, agent)
        self.target = target

    def __nonzero__(self):
        return self.agent.has_seen_interception(self.target)
