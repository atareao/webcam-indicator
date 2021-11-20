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

import glob
import re
from plumbum import local
from utils import PropertyInt, PropertyBool

class V4L2Ctl:
    v4l2ctl = local["v4l2-ctl"]

    @classmethod
    def get_devices(cls):
        items = []
        paths = glob.glob("/dev/video*")
        for path in paths:
            formats_raw = cls.v4l2ctl("--list-formats", "--device", path)
            pattern = r"\[\d*\]: (.*)"
            formats = re.findall(pattern, formats_raw)
            if formats:
                info_raw = cls.get_info(path)
                pattern = r"Card type\s*:\s*(.*)"
                names = re.findall(pattern, info_raw)
                if names:
                    items.append({"name": names[0], "path": path})
        return items

    @classmethod
    def get_info(cls, path):
        return cls.v4l2ctl("--info", "--device", path)

    @staticmethod
    def _get_property(data_raw, pattern):
        m = re.findall(pattern, data_raw)
        if m:
            return [int(item) for item in m[0]]
        raise Exception("Not found property")

    @classmethod
    def get_data(cls, path):
        data = {}
        data_raw = cls.v4l2ctl("--info", "--device", path)
        dis = ["Driver name", "Card type", "Bus info", "Driver version"]
        for name in dis:
            pattern = f"{name}\s*:\s*(.*)"
            try:
                result = re.findall(pattern, data_raw)
                if result:
                    data[name] = result[0]
                else:
                    data[name] = None
            except Exception as exception:
                data[name] = None
        return data

    @classmethod
    def get_controls(cls, path):
        properties = {}
        data_raw = cls.v4l2ctl("--list-ctrls", "--device", path)
        pis = ["brightness", "contrast", "saturation", "gain",
               "white_balance_temperature", "sharpness",
               "backlight_compensation", "exposure_absolute", "pan_absolute",
               "tilt_absolute", "focus_absolute", "zoom_absolute",
               "led1_frequency"]
        for name in pis:
            pattern = f"{name}[^:]*:\smin=([-]*\d*)\smax=(\d*)\sstep=(\d*)\sdefault=(\d*)\svalue=(\d*)"
            try:
                properties[name] = PropertyInt(*cls._get_property(data_raw, pattern))
            except Exception as exception:
                properties[name] = None
                print(exception)
        pms = ["power_line_frequency", "exposure_auto", "led1_mode"]
        for name in pms:
            try:
                pattern = f"{name}[^:]*:\smin=([-]*\d*)\smax=(\d*)\sdefault=(\d*)\svalue=(\d*)"
                mini, maxi, default, value = cls._get_property(data_raw, pattern)
                properties[name] = PropertyInt(mini, maxi, 1, default, value)
            except Exception as exception:
                properties[name] = None
                print(exception)
        pbs = ["white_balance_temperature_auto", "exposure_auto_priority",
               "focus_auto"]
        for name in pbs:
            try:
                pattern = f"{name}[^:]*:\sdefault=(\d*)\svalue=(\d*)"
                default, value = cls._get_property(data_raw, pattern)
                properties[name] = PropertyBool(default, value)
            except Exception as exception:
                properties[name] = None
                print(exception)
        return properties

    @classmethod
    def get_control(cls, control, path):
        data_raw = cls.v4l2ctl("--get-ctrl", control, "--device", path)
        pattern = f"{control}:\s(\d*)"
        result = re.findall(pattern, data_raw)
        return result[0]

    @classmethod
    def set_control(cls, control, path, value):
        cls.v4l2ctl("--set-ctrl", f"{control}={value}", "--device", path)
