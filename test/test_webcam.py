#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2021 Lorenzo Carbonell <a.k.a. atareao>

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import unittest
import sys
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dir_path, "../src"))
from webcam import Webcam
from utils import Log

class TestWebcam(unittest.TestCase):
    def test_get_webcams(self):
        webcams = Webcam.get_all()
        for webcam in webcams:
            Log.info(webcam)
        self.assertGreater(len(webcams), 0)

    def test_get_brightness(self):
        webcam = Webcam.get_all()[0]
        brightness = webcam.get("brightness")
        self.assertGreater(brightness, 0)


    def test_set_brightness(self):
        webcam = Webcam.get_all()[0]
        original = webcam.get("brightness")
        new_brightness = 49
        webcam.set("brightness", new_brightness)
        tmp_brightness = webcam.get("brightness")
        self.assertEqual(new_brightness, tmp_brightness)
        new_brightness = 69
        webcam.set("brightness", new_brightness)
        tmp_brightness = webcam.get("brightness")
        self.assertEqual(new_brightness, tmp_brightness)
        new_brightness = original
        webcam.set("brightness", new_brightness)
        tmp_brightness = webcam.get("brightness")
        self.assertEqual(new_brightness, tmp_brightness)

    def test_focus(self):
        webcam = Webcam.get_all()[0]
        original_focus_auto = webcam.get("focus_auto")
        print(original_focus_auto)
        original_focus_absolute = webcam.get("focus_absolute")
        print(original_focus_absolute)
        webcam.set("focus_auto", False)
        webcam.set("focus_absolute", 50)
        new_focus_absolute = webcam.get("focus_absolute")
        self.assertEqual(new_focus_absolute, 50)
        webcam.set("focus_absolute", original_focus_absolute)
        webcam.set("focus_auto", original_focus_auto)



if __name__ == '__main__':
    unittest.main()
