#!/usr/bin/env python
#-*- coding:utf-8 -*-

from tests.models import User
import tests.utils
from tests.utils import always_true

def returns_false():
    return False

class MyController(object):
    def index(self):
        user = User()
        if user.is_authenticated():
            return "WooHoo"
        return "Fail"

    def other(self):
        return tests.utils.always_true()

    def other2(self):
        return always_true()

    def user_name(self):
        user = User()

        return user.username

    def return_other_attribute(self):
        user = User()
        return user.other_attribute
