#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''
Core agent decorated_functionality
'''

import sys
import inspect
from modulefinder import ModuleFinder

from mi7.errors import UnknownAgentError, InvalidAgentTargetError

AGENTS_FOR_MISSION = {}
FINDER = None
FINDER_PATH = None

def true_import(module_name):
    module = __import__(module_name)
    if '.' in module_name:
        module = reduce(getattr, module_name.split('.')[1:], module)
    return module

def get_actual_who(who):
    '''Gets the actual target for the interception'''
    if inspect.isclass(who):
        module = sys.modules[who.__module__]
        return getattr(module, who.__name__)
    elif inspect.ismodule(who):
        return sys.modules[who.__name__]

    raise InvalidAgentTargetError(InvalidAgentTargetError.message)

def get_name(cls):
    '''Returns the name of the specified class/module'''
    return cls.__name__.split('.')[-1]

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
            raise UnknownAgentError(UnknownAgentError.message % name)
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
        self.old_getattribute = None
        if inspect.isclass(self.target):
            self.replace_getattribute()

    def replace_getattribute(self):
        def getattribute_replacement(instance, attr_name):
            for interception in self.interceptions.values():
                if interception.match(attr_name):
                    return interception.execute()

            return object.__getattribute__(instance, attr_name)
        self.old_getattribute = getattr(self.target, '__getattribute__')

        setattr(self.target, '__getattribute__', getattribute_replacement)

    def finish_mission(self):
        '''Finishes the mission. Stop intercepting.'''
        setattr(self.target, '__getattribute__', self.old_getattribute) 
        for interception in self.interceptions.values():
            interception.get_lost()

    def intercept(self, what):
        '''Start intercepting one target'''
        self.interceptions[what] = Interception(self, what)

        return self.interceptions[what]

class Interception(object):
    '''Abstracts one interception.'''
    def __init__(self, source_agent, target_name):
        '''Creates one interception'''
        self.agent = source_agent
        self.target_name = target_name
        self.attribute_value = None
        self.return_value = None
        self.exception_value = None
        self.replacements = []

        self.resync_references()

    def match(self, target_name):
        return target_name == self.target_name

    def replace_at_target(self):
        if not inspect.ismodule(self.agent.target):
            return

        replacement = (self.agent.target,
                       self.target_name,
                       getattr(self.agent.target,
                               self.target_name,
                               None))
        if self.attribute_value:
            setattr(self.agent.target,
                    self.target_name,
                    self.attribute_value)
        else:
            setattr(self.agent.target,
                    self.target_name,
                    self.execute)

        self.replacements.append(replacement)
        self.resync_references()

    def resync_references(self):
        '''Resync any references to the given target.'''

        for module_name, module in FINDER.modules.iteritems():
            if module_name == self.agent.target_module_name:
                continue
            if self.target_name in module.globalnames:
                module = true_import(module_name)

                if hasattr(module, self.target_name):
                    method = getattr(module, self.target_name)
                    method_module = method.__module__
                    if method_module == self.agent.target_module_name:
                        replacement = (module, self.target_name, method)
                        self.replacements.append(replacement)
                        setattr(module, self.target_name, self.execute)

    def get_lost(self):
        '''Stop intercepting the target.'''
        for replacement in self.replacements:
            setattr(replacement[0], replacement[1], replacement[2])
        self.replacements = []

    def execute(self, *args, **kw):
        '''Executes the interception.'''
        if self.exception_value:
            raise self.exception_value
        if self.attribute_value:
            return self.attribute_value

        if inspect.ismodule(self.agent.target):
            return self.return_value

        return lambda *args, **kw: self.return_value

    def returns(self, value):
        '''Specifies the return value for the interception.'''
        self.return_value = value
        self.replace_at_target()

    def as_attribute(self, value):
        '''Specifies the return value for the given attribute'''
        self.attribute_value = value
        self.replace_at_target()

    def raises(self, exception):
        '''Specifies that this interception should raise'''
        self.exception_value = exception
        self.replace_at_target()
