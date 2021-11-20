#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# This file is part of webcam-indicator
#
# Copyright (c) 2021 Lorenzo Carbonell Cerezo <a.k.a. atareao>
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

import gi

try:
    gi.require_version('Gtk', '3.0')
    gi.require_version('Gdk', '3.0')
except ValueError as e:
    print(e)
    exit(1)
from gi.repository import Gtk
import os
import config
import shutil
from config import _
from configurator import Configuration
from basedialog import BaseDialog
from webcam import Webcam


class LeftLabel(Gtk.Label):
    def __init__(self, label):
        Gtk.Label.__init__(self)
        self.set_label(label)
        self.set_xalign(0)


class Preferences(BaseDialog):
    def __init__(self):
        self._switches = {
            "focus_auto": {"name": _("Auto focus"), "value": {}}
        }
        self._properties = {
            "focus_absolute": {"name": _("Focus"), "value": {}},
            "brightness": {"name": _("Brightness"), "value": {}},
            "contrast": {"name": _("Contrast"), "value": {}},
            "saturation": {"name": _("Staturation"), "value": {}},
            "sharpness": {"name": _("Sharpness"), "value": {}},
            "zoom_absolute": {"name": _("Zoom"), "value": {}}
        }
        BaseDialog.__init__(self, _('Preferences'), None, ok_button=True,
                            cancel_button=True)
        self.load()

    def on_switch_status_changed(self, widget, status, aproperty, path):
        self._webcams[path].set(aproperty, status)
        if aproperty == "focus_auto":
            self.pwidget[path]['focus_absolute'].set_sensitive(not status)

    def on_scale_value_changed(self, widget, scroll, value, aproperty, path):
        self._webcams[path].set(aproperty, value)

    def init_ui(self):
        BaseDialog.init_ui(self)

        notebook = Gtk.Notebook.new()
        self.add_widget(notebook)

        grid_general = self.build_general_options()
        notebook.append_page(grid_general, Gtk.Label.new(_("General")))

        self._webcams = {}
        self.pwidget = {}
        for webcam in Webcam.get_all():
            self._webcams[webcam.path] = webcam
            grid = Gtk.Grid()
            grid.set_row_spacing(10)
            grid.set_column_spacing(10)
            grid.set_margin_bottom(10)
            grid.set_margin_start(10)
            grid.set_margin_end(10)
            grid.set_margin_top(10)
            notebook.append_page(grid, Gtk.Label.new(webcam.name))

            self.pwidget[webcam.path] = {}
            start = 0
            for index, aproperty in enumerate(self._switches):
                print(aproperty)
                try:
                    value = webcam.get(aproperty)
                    self._switches[aproperty]["value"] = {webcam.path: value}
                    grid.attach(LeftLabel(self._switches[aproperty]["name"]),
                                0, start + index, 1, 1)
                    self.pwidget[webcam.path][aproperty] = Gtk.Switch.new()
                    self.pwidget[webcam.path][aproperty].set_active(value)
                    self.pwidget[webcam.path][aproperty].set_halign(
                            Gtk.Align.START)
                    self.pwidget[webcam.path][aproperty].connect(
                        "state-set", self.on_switch_status_changed,
                        aproperty,
                        webcam.path)
                    grid.attach(self.pwidget[webcam.path][aproperty], 1,
                            start + index, 1, 1)
                except Exception as exception:
                    print(exception)

            start = 1
            for index, aproperty in enumerate(self._properties):
                try:
                    value = webcam.get(aproperty)
                    self._properties[aproperty]["value"] = {webcam.path: value}
                    grid.attach(LeftLabel(self._properties[aproperty]["name"]),
                                0, start + index, 1, 1)
                    orientation = Gtk.Orientation.HORIZONTAL
                    adjustment = Gtk.Adjustment.new(value, 0, 101, 1, 1, 1)
                    self.pwidget[webcam.path][aproperty] = Gtk.Scale.new(
                            orientation, adjustment)
                    self.pwidget[webcam.path][aproperty].set_digits(0)
                    self.pwidget[webcam.path][aproperty].connect(
                        "change-value", self.on_scale_value_changed,
                        aproperty,
                        webcam.path)
                    self.pwidget[webcam.path][aproperty].set_size_request(
                            300, 10)
                    grid.attach(self.pwidget[webcam.path][aproperty], 1,
                            start + index, 1, 1)
                except Exception as exception:
                    print(exception)
            status = webcam.get('focus_auto')
            self.pwidget[webcam.path]['focus_absolute'].set_sensitive(
                    not status)

    def restore(self):
        for aproperty in self._switches:
            for path in self._switches[aproperty]['value']:
                webcam = Webcam(path)
                value = self._switches[aproperty]['value'][path]
                webcam.set(aproperty, value)
        for aproperty in self._properties:
            for path in self._properties[aproperty]['value']:
                webcam = Webcam(path)
                value = self._properties[aproperty]['value'][path]
                webcam.set(aproperty, value)

    def build_general_options(self):
        grid_general = Gtk.Grid()
        grid_general.set_row_spacing(10)
        grid_general.set_column_spacing(10)
        grid_general.set_margin_bottom(10)
        grid_general.set_margin_start(10)
        grid_general.set_margin_end(10)
        grid_general.set_margin_top(10)

        grid_general.attach(LeftLabel(_('Theme light:')), 0, 0, 1, 1)
        self.theme_light = Gtk.Switch.new()
        self.theme_light.set_halign(Gtk.Align.START)
        grid_general.attach(self.theme_light, 1, 0, 1, 1)

        grid_general.attach(LeftLabel(_('Autostart:')), 0, 1, 1, 1)
        self.autostart = Gtk.Switch.new()
        self.autostart.set_halign(Gtk.Align.START)
        grid_general.attach(self.autostart, 1, 1, 1, 1)

        grid_general.attach(LeftLabel(_('Debug:')), 0, 2, 1, 1)
        self.debug = Gtk.Switch.new()
        self.debug.set_halign(Gtk.Align.START)
        grid_general.attach(self.debug, 1, 2, 1, 1)
        return grid_general

    def load(self):
        configuration = Configuration()

        self.theme_light.set_active(configuration.get('theme-light'))

        autostart_file = 'webcam-indicator-autostart.desktop'
        if os.path.exists(os.path.join(
                os.getenv('HOME'), '.config', 'autostart', autostart_file)):
            self.autostart.set_active(True)
        else:
            self.autostart.set_active(False)
        self.debug.set_active(configuration.get('debug'))

    def save(self):
        configuration = Configuration()
        configuration.set('theme-light', self.theme_light.get_active())
        configuration.set('debug', self.debug.get_active())

        webcams = {}
        for webcam in Webcam.get_all():
            webcams[webcam.name] = {}
            for aproperty in self._switches:
                webcams[webcam.name][aproperty] = webcam.get(aproperty)
            for aproperty in self._properties:
                webcams[webcam.name][aproperty] = webcam.get(aproperty)
        configuration.set('webcams', webcams)
        configuration.save()

        autostart_file = 'webcam-indicator-autostart.desktop'
        autostart_file = os.path.join(
            os.getenv('HOME'), '.config', 'autostart', autostart_file)
        if self.autostart.get_active():
            if not os.path.exists(os.path.dirname(autostart_file)):
                os.makedirs(os.path.dirname(autostart_file))
            shutil.copyfile(config.AUTOSTART, autostart_file)
        else:
            if os.path.exists(autostart_file):
                os.remove(autostart_file)


if __name__ == '__main__':
    preferences = Preferences()
    response = preferences.run()
    if response == Gtk.ResponseType.ACCEPT:
        preferences.save()
    else:
        preferences.restore()
    preferences.destroy()
