#!/usr/bin/env python

from __future__ import print_function

import os
import sys

class Xfce(object):

    _style_descriptors = {
        "auto":      0,
        "centered":  1,
        "tiled":     2,
        "stretched": 3,
        "scaled":    4,
        "zoomed":    5
    }

    def set_background(self, path, style="auto"):
        os.system("xfconf-query --channel xfce4-desktop "
                  "--property /backdrop/screen0/monitor0/image-style "
                  "--set {}".format(self._style_descriptor(style)))
        os.system("xfconf-query --channel xfce4-desktop "
                  "--property /backdrop/screen0/monitor0/image-path "
                  "--set {}".format(path))

    def _style_descriptor(self, name):
        try:
            return self._style_descriptors[name.lower()]
        except KeyError:
            print("Option {} is not supported by xfce4-desktop. Try:".format(name), file=sys.stderr)
            for k in sorted(self._style_descriptors.keys()):
                print("  - {}".format(k), file=sys.stderr)
            raise ValueError("invalid desktop style name")

class Gnome(object):

    _style_descriptors = (
        "centered",
        "scaled",
        "spanned",
        "zoom",
        "stretched",
        "wallpaper"
    )

    def set_background(self, path, style="auto"):
        os.system("gsettings set org.gnome.desktop.background "
                  "picture-options \"{}\"".format(self._style_descriptor(style)))
        os.system("gsettings set org.gnome.desktop.background "
                  "picture-uri \"file://{}\"".format(path))

    def _style_descriptor(self, name):
        if name.lower() in self._style_descriptors:
            return name.lower()
        else:
            print("Option {} is not supported by gnome/gsettings. Try:".format(name), file=sys.stderr)
            for k in sorted(self._style_descriptors):
                print("  - {}".format(k), file=sys.stderr)
            raise ValueError("invalid desktop style name")
