#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''Tests that the agents are working'''

from mi7.core import agent, agents, finish_mission, new_mission

import tests.controllers
import tests.utils
from tests.models import User

@new_mission
@agent.spy(User)
def test_spy_raising():
    '''Verifies that we can spy on the user model
    and make it raise'''

    agents.User \
          .intercept('is_authenticated') \
          .raises(ValueError("whatever"))

    controller = tests.controllers.MyController()

    try:
        controller.index()
    except ValueError, err:
        assert str(err) == "whatever"
        return

    assert False, "Should not have gotten this far"
