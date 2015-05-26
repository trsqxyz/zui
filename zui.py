#!/usr/bin/env python
# -*- coding: utf-8 -*-

import functools
import os
import platform
import sys
import webbrowser

import config
from pushbullet import Pushbullet


class Zui:

    def __init__(self):
        self.pb = Pushbullet(self.api_key())
        self.target = self.make_devices()
        self.dayone = config.URL_SCHEME

    def api_key(self):
        if config.API_KEY:
            return config.API_KEY
        else:
            webbrowser.open('https://www.pushbullet.com/account')
            API_KEY = input('Copy and Paste Access Token: ')
            self.config_setting(API_KEY)
            return API_KEY

    def config_setting(self, api_key):
        with open('config.py', 'r') as rf:
            setting = rf.readlines()
            setting[0] = 'API_KEY = "{0}"\n'.format(api_key)
        with open('config.py', 'w') as wf:
            wf.writelines(setting)
            wf.flush()

    def make_devices(self):
        for d in self.pb.devices:
            if config.PUSH_TARGET == d.nickname:
                return d
            else:
                new_device = self.pb.new_device(config.PUSH_TARGET)
                #  model argument was not used, only nickname
                self.pb.edit_device(
                    new_device,
                    nickname=config.PUSH_TARGET,
                    model=config.PUSH_TARGET
                )
                self.make_devices()

    def clear_notepad(f):
        functools.wraps(f)
        def wraps(*args):
            os.system(args[0].clear)
            result = f(*args)
            os.system(args[0].clear)
            return result
        return wraps

    @clear_notepad
    def push_to_dayone(self):
        '''Pushbullet couldn't link then whitespace in URL.
        So, it doesn't push_link, just push_note.
        Unavilable DayOne URL shceme.
        '''
        try:
            #  body = self.dayone + self.notepad()
            body = self.notepad()
            return self.pb.push_note('', body, device=self.target)
        except (KeyboardInterrupt, TypeError) as e:
            return False

    def notepad(self):
        try:
            print('Push: {}, Close: C-c'.format(self.pause))
            lines = [line for line in sys.stdin.readlines()]
            return ''.join(lines)
        except KeyboardInterrupt as e:
            return e

    def check_platform(self):
        cp = {
            'Windows': (
                'CLS',
                'C-z'
            ),
            'Darwin': (
                'clear',
                'C-d'
            ),
        }
        clear, pause = clear[platform.system()][0], clear[platform.system()][1]
        os.system(clear)
        return pause


def main():
    z = Zui()
    while z.push_to_dayone():
        pass
    else:
        print('Bye')


if __name__ == '__main__':
    main()
