#!/usr/bin/env python
#-*- coding:utf-8 -*-

class User(object):
    def __init__(self, username="Bernie"):
        self.username = username

    def is_authenticated(self):
        return False
