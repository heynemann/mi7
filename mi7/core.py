#!/usr/bin/env python
#-*- coding:utf-8 -*-

AGENTS_FOR_MISSION = {}

def get_name(cls):
    return cls.__name__

def finish_mission():
    global AGENTS_FOR_MISSION
    for agent in AGENTS_FOR_MISSION.values():
        agent.finish_mission()
    AGENTS_FOR_MISSION = {}

class AgentWrapper(object):
    @classmethod
    def spy(cls, who):
        global AGENTS_FOR_MISSION
        def wrapper(fn):
            def wrapper_2(*args, **kw):
                agent_name = get_name(who)
                agent_on_mission = Agent(agent_name, who)

                AGENTS_FOR_MISSION[agent_name] = agent_on_mission 

                return fn(*args, **kw)
            wrapper_2.__name__ = fn.__name__
            wrapper_2.__doc__ = fn.__name__
            return wrapper_2
        return wrapper
agent = AgentWrapper

class AgentsWatcher(object):
    def __getattr__(self, name):
        global AGENTS_FOR_MISSION
        return AGENTS_FOR_MISSION[name]
agents = AgentsWatcher()

class Agent(object):
    def __init__(self, name, target):
        self.name = name
        self.target = target
        self.interceptions = {}

    def finish_mission(self):
        for interception in self.interceptions.values():
            interception.get_lost()

    def intercept(self, what):
        self.interceptions[what] = Interception(self, what)
        return self.interceptions[what]

class Interception(object):
    def __init__(self, agent, method_name):
        self.agent = agent
        self.method_name = method_name
        self.return_value = None
        self.old_method = None
        self.watch()

    def watch(self):
        self.old_method = getattr(self.agent.target, self.method_name)
        setattr(self.agent.target, self.method_name, self.execute)

    def get_lost(self):
        setattr(self.agent.target, self.method_name, self.old_method)
        self.old_method = None

    def execute(self, *args, **kw):
        return self.return_value

    def returns(self, value):
        self.return_value = value
