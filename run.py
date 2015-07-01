#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys

import zipfile
import json
from gi.repository import Gtk, Gdk, Pango, GdkPixbuf

import sendkey

#argv1 file 1 or string 2 option


try:
    if sys.argv[1] == "1":
        f = zipfile.ZipFile(sys.argv[2], "r")
        save = json.loads(f.read("teclado.k"))
    else:
        try:
            s = sys.argv[2]
            #print s
            save = json.loads('%s' % sys.argv[2])
            #print save["2"]
        except Exception as e:
            print e

    window2 = Gtk.Window()
    window2.set_keep_above(True)
    window2.set_accept_focus(False)
    fixed2 = Gtk.Fixed()
    window2.add(fixed2)
    window2.show_all()
    fixed2.show_all()

    for key in save:
        print key
        button = Gtk.Button(save[key][4])
        button.set_size_request(save[key][2], save[key][3])
        fixed2.put(button, save[key][0], save[key][1])
        try:
            button.modify_bg(Gtk.StateFlags.NORMAL, save[key][6])
        except:
            button.modify_bg(Gtk.StateFlags.NORMAL, Gdk.Color(red=65535,
                                                              green=65535,
                                                              blue=65535))
        try:
            button.modify_font(Pango.FontDescription(save[key][7]))
        except Exception as e:
            print "problems setting font"
            print e
        try:
            if save[key][8] != "":
                button.remove(button.get_child())
                img = Gtk.Image()
                pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(
                                                      save[key][8],
                                                      save[key][2],
                                                      save[key][3]
                                                      )
                img.set_from_pixbuf(pixbuf)
                img.show_all()
                button.add(img)
                button.show_all()
        except Exception as e:
            print e
        button.show()
        if save[key][5].split("->")[0] == "Write":
            print "---"
            toSimulate = save[key][5].split("->")[1]
            print "---"
            button.connect("clicked", sendkey.sendkey, toSimulate)
        elif save[key][5].split("->")[0] == "Speak":
            button.connect("clicked", lambda x: os.system("espeak -ves '%s'"
                                      % save[key][5].split("->")[1]))
        elif save[key][5].split("->")[0] == "System Action":
            pass

        Gtk.main()
except:
    print "Modo de empleo: run.py number option"
    print "Si number es 1, option debe ser un archivo .keyboard"
    print "Si number es 2, option debe ser un string"


