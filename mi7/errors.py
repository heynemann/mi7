#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''Module with all the Typed Errors
for MI7 - Also known as agent mistakes.'''

class UnknownAgentError(RuntimeError):
    '''Represents trying to guess the identity of
    an agent for whom you don't have clearance.'''
    pass
