#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''Module with all the Typed Errors
for MI7 - Also known as agent mistakes.'''

class UnknownAgentError(RuntimeError):
    '''Represents trying to guess the identity of
    an agent for whom you don't have clearance.'''
    message = "You do not have clearance to " + \
              "use agent's %s services " + \
              "(agent not found)"

class InvalidAgentTargetError(ValueError):
    '''Represents trying to spy on something that's
    not a module or class'''
    message = "Invalid person to spy on. " + \
              "Valid people are modules " + \
              "and classes."
