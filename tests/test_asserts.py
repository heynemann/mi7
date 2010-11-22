#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''Tests that the agents are reporting'''

from mi7.core import agent, agents, new_mission

import tests.controllers
import tests.utils
from tests.models import User

@new_mission
@agent.spy(User)
def test_spy_assertion():
    '''Verifies that a spy reports the result of
    an interception.'''

    agents.User \
          .intercept('is_authenticated') \
          .returns("whatever")

    controller = tests.controllers.MyController()

    assert not agents.User.has_seen('is_authenticated')

    controller.index()

    assert agents.User.has_seen('is_authenticated')
