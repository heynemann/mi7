#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''Tests that the agents are working'''

from mi7.core import agent, agents, finish_mission, new_mission
from mi7.errors import UnknownAgentError

import tests.controllers
import tests.utils

@new_mission
@agent.spy(tests.controllers.User)
def test_controller_user_spying():
    '''Verifies that we can spy on the user model'''

    agents.User \
          .intercept('is_authenticated') \
          .returns(True)

    controller = tests.controllers.MyController()

    result = controller.index()

    assert result == "WooHoo"

@new_mission
@agent.spy(tests.controllers.User)
def test_finishing_mission_works():
    '''Verifies that after finishing the mission
    the data is cleared properly.'''
    agents.User \
          .intercept('is_authenticated') \
          .returns(True)

    controller = tests.controllers.MyController()

    #forcefully end mission
    finish_mission()

    result = controller.index()

    assert result == "Fail", result

@new_mission
@agent.spy(tests.controllers)
def test_intercepting_modules():
    '''Verifies that spying on modules
    works as well'''

    agents.Controllers \
          .intercept('returns_false') \
          .returns(True)

    assert tests.controllers.returns_false()

@new_mission
def test_agent_does_not_exist():
    '''Verifies that we get a proper error
    if the agent does not exist for this mission'''
    try:
        agents.bond
    except UnknownAgentError:
        assert True
        return
    assert False, "Should not have gotten this far"

@new_mission
@agent.spy(tests.utils)
def test_can_override_global():
    '''Verifies that if we intercept a module imported
    here in the test, the same module when imported
    by the controller still has the interception.'''

    agents.Utils.intercept('always_true') \
                .returns(False)

    controller = tests.controllers.MyController()

    assert not controller.other()

    assert not controller.other2()
