#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''
Core agent functionality
'''

from mi7.errors import UnknownAgentError

AGENTS_FOR_MISSION = {}

def get_name(cls):
    '''Returns the name of the specified class/module'''
    return cls.__name__.split('.')[-1].capitalize()

def finish_mission():
    '''Clears up after the agents for the current mission'''
    for one_agent in AGENTS_FOR_MISSION.values():
        one_agent.finish_mission()
    AGENTS_FOR_MISSION.clear()

def new_mission(function):
    '''Decorator that starts a new mission'''
    def wrapper(*args, **kw):
        '''Wrapper for the new_mission decorator'''
        try:
            return function(*args, **kw)
        finally:
            finish_mission()
    wrapper.__name__ = function.__name__
    wrapper.__doc__ = function.__doc__
    return wrapper

class AgentWrapper(object):
    '''Wraps the agent DSL'''
    @classmethod
    def spy(cls, who):
        '''Spies on a given class/module'''
        def wrapper(function):
            '''Wrapper for the spy decorator'''
            def wrapper_2(*args, **kw):
                '''Wrapper for the spy decorator'''
                agent_name = get_name(who)
                agent_on_mission = Agent(agent_name, who)

                AGENTS_FOR_MISSION[agent_name] = agent_on_mission 

                return function(*args, **kw)
            wrapper_2.__name__ = function.__name__
            wrapper_2.__doc__ = function.__name__
            return wrapper_2
        return wrapper
agent = AgentWrapper

class AgentsWatcher(object):
    '''Keeps track of agents in the current mission'''
    def __getattr__(self, name):
        '''Returns the agent by name'''
        if not name in AGENTS_FOR_MISSION:
            raise UnknownAgentError("You do not have clearance to use agent's %s services (agent not found)" % name)
        return AGENTS_FOR_MISSION[name]
agents = AgentsWatcher()

class Agent(object):
    '''Describes one agent'''
    def __init__(self, name, target):
        '''Initializes one agent.'''
        self.name = name
        self.target = target
        self.interceptions = {}

    def finish_mission(self):
        '''Finishes the mission. Stop intercepting.'''
        for interception in self.interceptions.values():
            interception.get_lost()

    def intercept(self, what):
        '''Start intercepting one target'''
        self.interceptions[what] = Interception(self, what)
        return self.interceptions[what]

class Interception(object):
    '''Abstracts one interception.'''
    def __init__(self, source_agent, method_name):
        '''Creates one interception'''
        self.agent = source_agent
        self.method_name = method_name
        self.return_value = None
        self.old_method = None
        self.watch()

    def watch(self):
        '''Start watching the interception target.'''
        self.old_method = getattr(self.agent.target, self.method_name)
        setattr(self.agent.target, self.method_name, self.execute)

    def get_lost(self):
        '''Stop intercepting the target.'''
        setattr(self.agent.target, self.method_name, self.old_method)
        self.old_method = None

    def execute(self, *args, **kw):
        '''Executes the interception.'''
        return self.return_value

    def returns(self, value):
        '''Specifies the return value for the interception.'''
        self.return_value = value
