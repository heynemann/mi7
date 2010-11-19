#!/usr/bin/env python
#-*- coding:utf-8 -*-

from mi7.core import agent, agents, finish_mission
import tests.controllers

@agent.spy(tests.controllers.User)
def test_controller_verifies_if_user_is_authenticated():
    agents.User \
         .intercept('is_authenticated') \
         .returns(True)

    controller = tests.controllers.MyController()

    result = controller.index()

    assert result == "WooHoo"

    finish_mission()

@agent.spy(tests.controllers.User)
def test_methods_properly_reset_after_test():
    agents.User \
         .intercept('is_authenticated') \
         .returns(True)

    controller = tests.controllers.MyController()

    #forcefully end mission
    finish_mission()

    result = controller.index()

    assert result == "Fail", result

    finish_mission()
