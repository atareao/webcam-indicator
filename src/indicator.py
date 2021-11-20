#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# This file is part of webcam-indicator
#
# Copyright (c) 2020 Lorenzo Carbonell Cerezo <a.k.a. atareao>
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

import sys
import gi
from utils import Log
try:
    gi.require_version('Gtk', '3.0')
    gi.require_version('Gdk', '3.0')
    gi.require_version('AppIndicator3', '0.1')
    gi.require_version('GdkPixbuf', '2.0')
    gi.require_version('Notify', '0.7')
except Exception as e:
    Log.error(e)
    exit(-1)
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import AppIndicator3
from gi.repository import GdkPixbuf
from gi.repository import Notify
import os
import webbrowser
import dbus
from config import _
from preferences import Preferences
import config
from configurator import Configuration
from webcam import Webcam

ACTIVE = 1
INACTIVE = 0

class Indicator:

    def __init__(self):

        self.indicator = AppIndicator3.Indicator.new(
            'webcam-indicator',
            'webcam-indicator',
            AppIndicator3.IndicatorCategory.APPLICATION_STATUS)
        self.indicator.set_label('', '')
        self.notification = Notify.Notification.new('', '', None)
        self.load_preferences()

    def set_icon(self, active=ACTIVE):
        if active == ACTIVE:
            if self.theme_light:
                icon = config.ICON_ACTIVED_LIGHT
            else:
                icon = config.ICON_ACTIVED_DARK
            self.indicator.set_status(AppIndicator3.IndicatorStatus.ATTENTION)
            self.indicator.set_attention_icon_full(icon, "")
        else:
            if self.theme_light:
                icon = config.ICON_PAUSED_LIGHT
            else:
                icon = config.ICON_PAUSED_DARK
            self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
            self.indicator.set_icon_full(icon, "")

    def load_preferences(self):
        any_auto_focus = False
        configuration = Configuration()
        self.theme_light = configuration.get('theme-light')
        self.indicator.set_menu(self.build_menu())
        saved_webcams = configuration.get('webcams')
        for webcam in Webcam.get_all():
            for saved_webcam_name in saved_webcams:
                if webcam.name == saved_webcam_name:
                    for aproperty in saved_webcams[saved_webcam_name]:
                        value = saved_webcams[saved_webcam_name][aproperty]
                        webcam.set(aproperty, value)
                        if aproperty == 'focus_auto' and value:
                            any_auto_focus = True
                    break
        self.set_icon(ACTIVE if any_auto_focus else INACTIVE)

    def build_menu(self):
        menu = Gtk.Menu()
        self.menu_toggle_service = {}
        for webcam in Webcam.get_all():
            Log.info(webcam)
            self.menu_toggle_service[webcam.path] = \
                    Gtk.CheckMenuItem.new_with_label(webcam.name)
            self.menu_toggle_service[webcam.path].set_active(
                    webcam.get("focus_auto"))
            self.menu_toggle_service[webcam.path].connect(
                'activate', self.toggle_service, webcam.path)
            menu.append(self.menu_toggle_service[webcam.path])
        menu.append(Gtk.SeparatorMenuItem())

        menu_preferences = Gtk.MenuItem.new_with_label(_('Preferences'))
        menu_preferences.connect('activate', self.show_preferences)
        menu.append(menu_preferences)

        menus_help = Gtk.MenuItem.new_with_label(_('Help'))
        menus_help.set_submenu(self.get_help_menu())
        menu.append(menus_help)

        menu.append(Gtk.SeparatorMenuItem())

        menu_quit = Gtk.MenuItem. new_with_label(_('Quit'))
        menu_quit.connect('activate', self.quit)
        menu.append(menu_quit)
        menu.show_all()
        return menu

    def show_preferences(self, widget):
        widget.set_sensitive(False)
        preferences_dialog = Preferences()
        response = preferences_dialog.run()
        if response == Gtk.ResponseType.ACCEPT:
            preferences_dialog.save()
            configuration = Configuration()
            self.theme_light = configuration.get('theme-light')
            self.load_preferences()
        else:
            preferences_dialog.restore()
        preferences_dialog.destroy()
        widget.set_sensitive(True)

    def get_help_menu(self):
        help_menu = Gtk.Menu()

        homepage_item = Gtk.MenuItem.new_with_label(_('Homepage'))
        homepage_item.connect(
            'activate',
            lambda x: webbrowser.open(
                'http://www.atareao.es/apps/webcam-indicator/'))
        help_menu.append(homepage_item)

        help_item = Gtk.MenuItem.new_with_label(_('Get help online...'))
        help_item.connect(
            'activate',
            lambda x: webbrowser.open(
                'http://www.atareao.es/apps/webcam-indicator/'))
        help_menu.append(help_item)

        translate_item = Gtk.MenuItem.new_with_label(_(
            'Translate this application...'))
        translate_item.connect(
            'activate',
            lambda x: webbrowser.open(
                'http://www.atareao.es/apps/webcam-indicator/'))
        help_menu.append(translate_item)

        bug_item = Gtk.MenuItem.new_with_label(_('Report a bug...'))
        bug_item.connect(
            'activate',
            lambda x: webbrowser.open('https://github.com/atareao\
/webcam-indicator/issues'))
        help_menu.append(bug_item)

        help_menu.append(Gtk.SeparatorMenuItem())

        twitter_item = Gtk.MenuItem.new_with_label(_('Found me in Twitter'))
        twitter_item.connect(
            'activate',
            lambda x: webbrowser.open('https://twitter.com/atareao'))
        help_menu.append(twitter_item)
        #
        github_item = Gtk.MenuItem.new_with_label(_('Found me in GitHub'))
        github_item.connect(
            'activate',
            lambda x: webbrowser.open('https://github.com/atareao'))
        help_menu.append(github_item)

        mastodon_item = Gtk.MenuItem.new_with_label(_('Found me in Mastodon'))
        mastodon_item.connect(
            'activate',
            lambda x: webbrowser.open('https://mastodon.social/@atareao'))
        help_menu.append(mastodon_item)

        about_item = Gtk.MenuItem.new_with_label(_('About'))
        about_item.connect('activate', self.menu_about_response)

        help_menu.append(Gtk.SeparatorMenuItem())

        help_menu.append(about_item)
        return help_menu

    def menu_about_response(self, widget):
        widget.set_sensitive(False)
        ad = Gtk.AboutDialog()
        ad.set_name(config.APPNAME)
        ad.set_version(config.VERSION)
        ad.set_copyright('Copyrignt (c) 2020\nLorenzo Carbonell')
        ad.set_comments(_('Webcam Indicator'))
        ad.set_license('''
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.''')
        ad.set_website('')
        ad.set_website_label('http://www.atareao.es')
        ad.set_authors(['Lorenzo Carbonell Cerezo <a.k.a. atareao>'])
        ad.set_translator_credits('Lorenzo Carbonell Cerezo <a.k.a. atareao>')
        ad.set_documenters(['Lorenzo Carbonell Cerezo <a.k.a. atareao>'])
        ad.set_artists(['Freepik <https://www.flaticon.com/authors/freepik>'])
        ad.set_logo(GdkPixbuf.Pixbuf.new_from_file(config.ICON))
        ad.set_icon(GdkPixbuf.Pixbuf.new_from_file(config.ICON))
        ad.set_program_name(config.APPNAME)

        monitor = Gdk.Display.get_primary_monitor(Gdk.Display.get_default())
        scale = monitor.get_scale_factor()
        monitor_width = monitor.get_geometry().width / scale
        monitor_height = monitor.get_geometry().height / scale
        width = ad.get_preferred_width()[0]
        height = ad.get_preferred_height()[0]
        ad.move((monitor_width - width)/2, (monitor_height - height)/2)

        ad.run()
        ad.destroy()
        widget.set_sensitive(True)

    def toggle_service(self, widget, path):
        Log.info(widget)
        Log.info(path)
        Log.info(widget.get_active())
        any_auto_focus = False
        for webcam in Webcam.get_all():
            if webcam.path == path:
                webcam.set("focus_auto", widget.get_active())
            if webcam.get("focus_auto"):
                any_auto_focus = True
        self.set_icon(ACTIVE if any_auto_focus else INACTIVE)


    def stop(self):
        self.set_icon(INACTIVE)
        #self.menu_toggle_service.set_label(_('Start service'))

    def start(self):
        configuration = Configuration()
        preferences = configuration.get('preferences')


        icon = os.path.join(config.ICONDIR, 'webcam-indicator.svg')
        """
        self.notification.update('webcam-indicator',
                                 message,
                                 icon)
        self.notification.show()
        """

    def quit(self, menu_item):
        self.stop()
        Gtk.main_quit()
        # If Gtk throws an error or just a warning, main_quit() might not
        # actually close the app
        sys.exit(0)


def main():
    if dbus.SessionBus().request_name(
        'es.atareao.WebcamIndicator') !=\
            dbus.bus.REQUEST_NAME_REPLY_PRIMARY_OWNER:
        Log.info("application already running")
        exit(0)

    Notify.init('webcam-indicator')
    Indicator()
    Gtk.main()

if __name__ == '__main__':
    main()
