#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''Tests that the agents are working'''

from mi7.core import agent, agents, new_mission

import tests.controllers
import tests.utils

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
