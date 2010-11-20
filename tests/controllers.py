#!/usr/bin/env python
#-*- coding:utf-8 -*-

from tests.models import User

def returns_false():
    return False

class MyController(object):
    def index(self):
        user = User()
        if user.is_authenticated():
            return "WooHoo"
        return "Fail"
