# -*- coding: utf-8 -*-
from gi.repository import Gtk


class SpinButtonWithLabel(Gtk.HBox, Gtk.SpinButton):

    def set_adjustment(self, adjustment):
        self.spinbutton.set_adjustment(adjustment)

    def __init__(self, label):
        super(SpinButtonWithLabel, self).__init__()
        self.add(Gtk.Label(label))
        self.spinbutton = Gtk.SpinButton()
        self.add(self.spinbutton)