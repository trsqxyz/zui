#!/usr/bin/env python
# -*- coding: utf-8 -*-

import webbrowser
from pushbullet import Pushbullet
from config import *


class Zui:
    def __init__(self):
        if not API_KEY:
            webbrowser.open('https://www.pushbullet.com/account')
            API_KEY = input('Copy and Paste Access Token: ')
            with open('config.py') as f:
                f.write(API_KEY)
                f.flush()
        self.pb = Pushbullet(API_KEY)
        
    def hitsu(self):
        push = pb.push_note(input())
