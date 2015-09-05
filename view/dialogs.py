# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, '../controller/')

import json
import os
import zipfile
from gi.repository import Gtk

from gettext import gettext as _

from mainView import *

gettext.textdomain("lang")
gettext.bindtextdomain("lang", "./mo")
gettext.gettext("hello, world!")


def saveAllToZip(data, toSave):
        fileChooserDialog = Gtk.FileChooserDialog(_("Save Keyboard"), None,
         Gtk.FileChooserAction.SAVE, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
         Gtk.STOCK_OK, Gtk.ResponseType.OK))
        response = fileChooserDialog.run()
        if response == Gtk.ResponseType.OK:
            fileName = fileChooserDialog.get_filename()
            print fileName
            f = open("teclado.k", "w")
            f.write(json.dumps(toSave))
            print toSave
            f.close()

        elif response == Gtk.ResponseType.CANCEL:
            pass

        fileChooserDialog.destroy()

        if not fileName.endswith('.keyboard'):
                fileName += ".keyboard"

        zipFile = zipfile.ZipFile(fileName, "w")
        zipFile.write("teclado.k")
        infoFile = open("info.k", "w")
        screenInfo = getScreenInfo()
        infoFile.write(json.dumps(screenInfo))
        infoFile.close()
        zipFile.write("info.k")
        #zipFile.write("resources/")
        #zipFile.write("pyfiles/")
        zipFile.close()
        os.remove("teclado.k")
        os.remove("info.k")


def openFromKeyboard(data):
        fileChooserDialog = Gtk.FileChooserDialog(_("Save Keyboard"), None,
         Gtk.FileChooserAction.OPEN, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
         Gtk.STOCK_OK, Gtk.ResponseType.OK))
        keyboardFilter = Gtk.FileFilter()
        keyboardFilter.set_name(_("Keyboard Files"))
        keyboardFilter.add_pattern("*.keyboard")
        fileChooserDialog.add_filter(keyboardFilter)
        response = fileChooserDialog.run()
        if response == Gtk.ResponseType.OK:
            fileName = fileChooserDialog.get_filename()
            print fileName
            f = zipfile.ZipFile(fileName, "r")
            fr = f.read("teclado.k")
            setSave(json.loads(fr))
            init()
            #self.window.show_all()
        elif response == Gtk.RESPONSE_CANCEL:
            pass
        fileChooserDialog.destroy()