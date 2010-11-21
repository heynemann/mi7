#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''Tests that the agents are working'''

from mi7.core import agent, agents, finish_mission, new_mission

import tests.controllers
import tests.utils
from tests.models import User

@new_mission
@agent.spy(User)
def test_spying_an_attr():
    '''Verifies that we can spy on the user model
    and replace an attribute'''

    agents.User \
          .intercept('username') \
          .as_attribute("Waldo")

    controller = tests.controllers.MyController()

    result = controller.user_name()

    assert result == "Waldo"
