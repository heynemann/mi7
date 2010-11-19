#!/usr/bin/env python
#-*- coding:utf-8 -*-

SPIES_FOR_MISSION = {}

def get_name(cls):
    return cls.__name__

def clear_mission():
    pass

def new_mission(fn):
    clear_mission()
    return fn

class SpyWrapper(object):
    @classmethod
    def on(cls, who):
        spy_name = get_name(who)
        spy_on_mission = Spy(spy_name, who)
        SPIES_FOR_MISSION[spy_name] = spy_on_mission
        def wrapper(fn):
            def wrapper_2(*args, **kw):
                return fn(*args, **kw)
            wrapper_2.__name__ = fn.__name__
            wrapper_2.__doc__ = fn.__name__
            return wrapper_2
        return wrapper
spy = SpyWrapper

class SpiesWatcher(object):
    def __getattr__(self, name):
        return SPIES_FOR_MISSION[name]
spies = SpiesWatcher()

class Spy(object):
    def __init__(self, name, target):
        self.name = name
        self.target = target
        self.interceptions = {}

    def finish_mission(self):
        for interception in self.interception.values():
            interception.get_lost()

    def intercept(self, what):
        self.interceptions[what] = Interception(self, what)
        return self.interceptions[what]

class Interception(object):
    def __init__(self, spy, method_name):
        self.spy = spy
        self.method_name = method_name
        self.return_value = None
        self.old_method = None
        self.watch()

    def watch(self):
        self.old_method = getattr(self.spy.target, self.method_name)
        setattr(self.spy.target, self.method_name, self.execute)

    def get_lost(self):
        setattr(self.spy.target, self.method_name, self.old_method)
        self.old_method = None

    def execute(self, *args, **kw):
        return self.return_value

    def returns(self, value):
        self.return_value = value
