#!/usr/bin/env python
#-*- coding:utf-8 -*-

from mi7.core import finish_mission, spy, spies
import tests.controllers

@spy.on(tests.controllers.User)
def test_controller_verifies_if_user_is_authenticated():
    spies.User \
         .intercept('is_authenticated') \
         .returns(True)

    controller = tests.controllers.MyController()

    result = controller.index()

    assert result == "WooHoo"

    finish_mission()

@spy.on(tests.controllers.User)
def test_methods_properly_reset_after_test():
    spies.User \
         .intercept('is_authenticated') \
         .returns(True)

    controller = tests.controllers.MyController()

    #forcefully end mission
    finish_mission()

    result = controller.index()

    assert result == "Fail", result

    finish_mission()
