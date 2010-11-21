#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''
Core agent decorated_functionality
'''

import sys
import inspect
from modulefinder import ModuleFinder

from mi7.errors import UnknownAgentError

AGENTS_FOR_MISSION = {}
FINDER = None
FINDER_PATH = None

def get_actual_who(who):
    '''Gets the actual target for the interception'''
    if inspect.isclass(who):
        module = sys.modules[who.__module__]
        return getattr(module, who.__name__)
    elif inspect.ismodule(who):
        return sys.modules[who.__name__]

    #TODO: TEST THIS!
    raise ValueError("""Invalid person to spy on. 
    Valid people are modules and classes.""")

def get_name(cls):
    '''Returns the name of the specified class/module'''
    return cls.__name__.split('.')[-1].capitalize()

def finish_mission():
    '''Clears up after the agents for the current mission'''
    for one_agent in AGENTS_FOR_MISSION.values():
        one_agent.finish_mission()
    AGENTS_FOR_MISSION.clear()

def new_mission(decorated_function):
    '''Decorator that starts a new mission'''
    global FINDER
    global FINDER_PATH

    if hasattr(decorated_function, 'decorated_function'):
        path = inspect.getfile(decorated_function.decorated_function)
    else:
        path = inspect.getfile(decorated_function)

    if path != FINDER_PATH:
        FINDER = ModuleFinder()
        FINDER.run_script(path)
        FINDER_PATH = path

    def wrapper(*args, **kw):
        '''Wrapper for the new_mission decorator'''
        try:
            return decorated_function(*args, **kw)
        finally:
            finish_mission()
    wrapper.__name__ = decorated_function.__name__
    wrapper.__doc__ = decorated_function.__doc__
    return wrapper

class AgentWrapper(object):
    '''Wraps the agent DSL'''
    @classmethod
    def spy(cls, who):
        '''Spies on a given class/module'''
        def wrapper(decorated_function):
            '''Wrapper for the spy decorator'''
            def wrapper_2(*args, **kw):
                '''Wrapper for the spy decorator'''
                target = get_actual_who(who)
                agent_name = get_name(target)
                agent_on_mission = Agent(agent_name, target)

                AGENTS_FOR_MISSION[agent_name] = agent_on_mission 

                return decorated_function(*args, **kw)
            wrapper_2.__name__ = decorated_function.__name__
            wrapper_2.__doc__ = decorated_function.__name__
            wrapper_2.decorated_function = decorated_function
            return wrapper_2
        return wrapper
agent = AgentWrapper

class AgentsWatcher(object):
    '''Keeps track of agents in the current mission'''
    def __getattr__(self, name):
        '''Returns the agent by name'''
        if not name in AGENTS_FOR_MISSION:
            raise UnknownAgentError("""You do not have clearance to
            use agent's %s services (agent not found)""" % name)
        return AGENTS_FOR_MISSION[name]
agents = AgentsWatcher()

class Agent(object):
    '''Describes one agent'''
    def __init__(self, name, target):
        '''Initializes one agent.'''
        self.name = name
        self.target = target
        self.target_module_name = inspect.isclass(target) and \
                                        target.__module__ or \
                                        target.__name__
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
        self.replacements = []
        self.watch()

    def watch(self):
        '''Start watching the interception target.'''
        self.old_method = getattr(self.agent.target, self.method_name)
        setattr(self.agent.target, self.method_name, self.execute)

        for module_name, module in FINDER.modules.iteritems():
            if inspect.isbuiltin(module) or \
               module_name == self.agent.target_module_name:
                continue
            if self.method_name in module.globalnames:
                module = __import__(module_name)
                if '.' in module_name:
                    module = reduce(getattr, module_name.split('.')[1:], module)
                if hasattr(module, self.method_name):
                    method = getattr(module, self.method_name)
                    method_module = method.__module__
                    if method_module == self.agent.target_module_name:
                        replacement = (module, self.method_name, method)
                        self.replacements.append(replacement)
                        setattr(module, self.method_name, self.execute)
                elif hasattr(module, self.agent.target.__name__):
                    target_name = self.agent.target.__name__
                    setattr(module, target_name, self.agent.target)


    def get_lost(self):
        '''Stop intercepting the target.'''
        setattr(self.agent.target, self.method_name, self.old_method)
        self.old_method = None
        for replacement in self.replacements:
            setattr(replacement[0], replacement[1], replacement[2])
        self.replacements = []

    def execute(self, *args, **kw):
        '''Executes the interception.'''
        return self.return_value

    def returns(self, value):
        '''Specifies the return value for the interception.'''
        self.return_value = value
