#!/usr/bin/env python
#-*- coding:utf-8 -*-

from mi7.core import new_mission, spy, spies
import tests.controllers

@new_mission
@spy.on(tests.controllers.User)
def test_controller_verifies_if_user_is_authenticated():
    spies.User \
         .intercept('is_authenticated') \
         .returns(True)

    controller = tests.controllers.MyController()

    result = controller.index()

    assert result == "WooHoo"

