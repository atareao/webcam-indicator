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

from v4l2ctl import V4L2Ctl
from utils import PropertyBool, PropertyInt


class Webcam:
    def __init__(self, path):
        self._path = path
        self.__init()

    @property
    def name(self):
        return self._name

    @property
    def path(self):
        return self._path

    def __init(self):
        self._properties = V4L2Ctl.get_controls(self.path)
        self._data = V4L2Ctl.get_data(self.path)
        self._name = self._data["Card type"]

    @classmethod
    def get_all(cls):
        webcams = []
        for item in V4L2Ctl.get_devices():
            webcams.append(Webcam(item["path"]))
        return webcams

    def get(self, property_name):
        if type(self._properties[property_name]) == PropertyInt:
            value = int(V4L2Ctl.get_control(property_name, self.path))
            self._properties[property_name].value = value
            return self._properties[property_name].percentage
        elif type(self._properties[property_name]) == PropertyBool:
            value = int(V4L2Ctl.get_control(property_name, self.path))
            self._properties[property_name].v4value = value
            return self._properties[property_name].value

    def set(self, property_name, value):
        if type(self._properties[property_name]) == PropertyInt:
            original = self._properties[property_name].percentage
            try:
                self._properties[property_name].percentage = value
                V4L2Ctl.set_control(property_name,
                                    self.path,
                                    self._properties[property_name].value)
            except Exception as exception:
                print(exception)
                self._properties[property_name].percentage = original
        elif type(self._properties[property_name]) == PropertyBool:
            original = self._properties[property_name].value
            try:
                self._properties[property_name].value = value
                V4L2Ctl.set_control(property_name,
                                    self.path,
                                    self._properties[property_name].v4value)
            except Exception as exception:
                print(exception)
                self._properties[property_name].value = original

    def set_default(self, property_name):
        if type(self._properties[property_name]) == PropertyInt:
            original = self._properties[property_name].percentage
            try:
                self._properties[property_name].set_default()
                V4L2Ctl.set_control(property_name,
                                    self.path,
                                    self._properties[property_name].value)
            except Exception as exception:
                print(exception)
                self._properties[property_name].percentage = original
        elif type(self._properties[property_name]) == PropertyBool:
            original = self._properties[property_name].value
            try:
                self._properties[property_name].set_default()
                V4L2Ctl.set_control(property_name,
                                    self.path,
                                    self._properties[property_name].v4value)
            except Exception as exception:
                print(exception)
                self._properties[property_name].value = original

    def __str__(self):
        return (
                f"Name: {self.name}\n"
                f"Path: {self.path}\n"
                )
