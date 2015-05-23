#!/usr/bin/env python
# -*- coding: utf-8 -*-

import webbrowser

import config
from pushbullet import Pushbullet


class Zui:
    def __init__(self):
        if not config.API_KEY:
            webbrowser.open('https://www.pushbullet.com/account')
            API_KEY = input('Copy and Paste Access Token: ')
            with open('config.py', 'r') as rf:
                setting = rf.readlines()
                setting[0] = 'API_KEY = "{0}"\n'.format(API_KEY)
            with open('config.py', 'w') as wf:
                wf.writelines(setting)
                wf.flush()
        else:
            API_KEY = config.API_KEY
        self._name = config.PUSH_TARGET
        self.pb = Pushbullet(API_KEY)
        self.make_devices()
        self.dayone = config.URL_SCHEME

    def make_devices(self):
        for d in self.pb.devices:
            if config.PUSH_TARGET == d.nickname:
                self.target = d
                break
            else:
                new_device = self.pb.new_device(config.PUSH_TARGET)
                #  model argument was not used, only nickname
                self.pb.edit_device(
                                    new_device,
                                    nickname=self._name,
                                    model=config.PUSH_TARGET
                                    )
                self.make_devices()

    def push_to_dayone(self):
        body = input('Write:\n').strip()
        body = self.dayone + body
        push = self.pb.push_note('', body, device=self.target)


def main():
    z = Zui()
    z.push_to_dayone()

if __name__ == '__main__':
    main()
