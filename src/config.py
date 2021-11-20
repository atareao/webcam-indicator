#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# This file is part of webcam-indicator
#
# Copyright (c) 2020 1orenzo Carbonell Cerezo <a.k.a. atareao>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import locale
import gettext

PARAMS = {'theme-light': True,
          'debug': False,
          'webcams': []
          }

CONFIG_DIR = os.path.join(os.path.expanduser('~'), '.config/webcam-indicator')
CONFIG_FILE = os.path.join(CONFIG_DIR, 'webcam-indicator.conf')


def is_package():
    return __file__.find('src') < 0


APP = 'webcam-indicator'
APPNAME = 'Webcam Manager'

# check if running from source
if is_package():
    ROOTDIR = '/usr/share'
    LANGDIR = os.path.join(ROOTDIR, 'locale-langpack')
    APPDIR = os.path.join(ROOTDIR, APP)
    CHANGELOG = os.path.join(APPDIR, 'changelog')
    ICONDIR = os.path.join(ROOTDIR, 'icons')
    AUTOSTARTDIR = os.path.join(ROOTDIR, 'autostart')
else:
    ROOTDIR = os.path.abspath(os.path.dirname(__file__))
    LANGDIR = os.path.normpath(os.path.join(ROOTDIR, '../template1'))
    APPDIR = ROOTDIR
    DEBIANDIR = os.path.normpath(os.path.join(ROOTDIR, '../debian'))
    CHANGELOG = os.path.join(DEBIANDIR, 'changelog')
    ICONDIR = os.path.normpath(os.path.join(ROOTDIR, '../data/icons/'))
    AUTOSTARTDIR = os.path.normpath(
        os.path.join(ROOTDIR, '../data/autostart/'))
AUTOSTART = os.path.join(AUTOSTARTDIR, 'webcam-indicator-autostart.desktop')
ICON = os.path.join(ICONDIR, 'webcam-indicator.svg')
ICON_ACTIVED_LIGHT = os.path.join(ICONDIR, 'webcam-indicator-active-light.svg')
ICON_PAUSED_LIGHT = os.path.join(ICONDIR, 'webcam-indicator-paused-light.svg')
ICON_ACTIVED_DARK = os.path.join(ICONDIR, 'webcam-indicator-active-dark.svg')
ICON_PAUSED_DARK = os.path.join(ICONDIR, 'webcam-indicator-paused-dark.svg')
ICON_ERROR_DARK = os.path.join(ICONDIR, 'webcam-indicator-error-dark.svg')
ICON_ERROR_LIGHT = os.path.join(ICONDIR, 'webcam-indicator-error.svg')

f = open(CHANGELOG, 'r')
line = f.readline()
f.close()
pos = line.find('(')
posf = line.find(')', pos)
VERSION = line[pos + 1:posf].strip()
if not is_package():
    VERSION = VERSION + '-src'

try:
    current_locale, encoding = locale.getdefaultlocale()
    language = gettext.translation(APP, LANGDIR, [current_locale])
    language.install()
    _ = language.gettext
except Exception as e:
    print(e)
    _ = str
APPNAME = _(APPNAME)
