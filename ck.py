# Copyright (C) 2015 Rafael Cordano <rafael.cordano@gmail.com>
# Copyright (C) 2015 Ezequiel Pereira <ezequi>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
import json

from gi.repository import Gtk, Gdk
#import gobject

INITIAL_X, INITIAL_Y = 0, 50
INITIAL_W, INITIAL_H = 50, 50

UI_INFO = """
<ui>
  <menubar name='MenuBar'>
    <menu action='FileMenu'>
      <menuitem action='FileNewStandard' />
      <menuitem action='FileOpen' />
      <menuitem action='FileSave' />
      <menuitem action='FileSaveAs' />
      <separator />
      <menuitem action='FileQuit' />
    </menu>
    <menu action='OptionMenu'>
      <menuitem action='OptionRunKeyboard' />
    </menu>
    <menu action='HelpMenu'>
      <menuitem action='Help'/>
      <menuitem action='About'/>
    </menu>
  </menubar>
  <toolbar name='ToolBar'>
    <toolitem action='FileNewStandard' />
    <toolitem action='FileOpen' />
    <toolitem action='FileQuit' />
  </toolbar>
</ui>
"""


class CustomKey:
    def __init__(self):
        self.editing = False
        """
        self.menu_items = (
            ("/_File",         None,         None, 0, "<Branch>"),
            ("/File/_New",     "<control>N", None, 0, None),
            ("/File/_Open",    "<control>O", self.openFromJSON, 0, None ),
            ("/File/_Save",    "<control>S", None, 0, None ),
            ("/File/Save _As", None,         self.saveToJSON, 0, None ),
            ("/File/sep1",     None,         None, 0, "<Separator>" ),
            ("/File/Quit",     "<control>Q", Gtk.main_quit, 0, None ),
            ("/_Options",      None,         None, 0, "<Branch>" ),
            ("/Options/Run keyboard",  "<control>R", self.run , 0, None ),
            ("/_Help",         None,         None, 0, "<LastBranch>" ),
            ("/_Help/About",   None,         None, 0, None ),
            )
        """
        ####Main Menu
        action_group = Gtk.ActionGroup("my_actions")
        self.add_file_menu_actions(action_group)
        self.add_options_menu_actions(action_group)


        self.mousePosition = []
        self.cont = 1
        self.save = {}  # "button name":[x, y, sx, sy , label, func]
        self.edit = 0
        self.evpos = []
        window = Gtk.Window()
        self.window = window
        window.set_size_request(window.get_screen().get_width(),
                                window.get_screen().get_height() / 3)
        self.eventbox = Gtk.EventBox()
        self.eventbox.set_events(
            Gdk.EventMask.BUTTON_MOTION_MASK |               # restoring missed masks
            Gdk.EventMask.BUTTON1_MOTION_MASK |
            Gdk.EventMask.BUTTON2_MOTION_MASK |
            Gdk.EventMask.BUTTON3_MOTION_MASK
        )
        self.fixed = Gtk.Fixed()
        self.fixed.set_size_request(window.get_screen().get_width(),
                                    window.get_screen().get_height() / 3
                                    )

        self.menu = Gtk.Menu()
        self.menu_optionEditProperties = Gtk.MenuItem("Edit Properties")
        self.menu_deleteButton = Gtk.MenuItem("Remove Button")
        self.menu.add(self.menu_optionEditProperties)
        self.menu.add(self.menu_deleteButton)
        self.menu.show_all()

        self.init()
        window.add_events(Gdk.EventMask.POINTER_MOTION_MASK |
                          Gdk.EventMask.BUTTON_PRESS_MASK)

        window.connect("key-press-event", self.new_button)
        window.connect("destroy", Gtk.main_quit)

        self.vbox = Gtk.VBox(False, 1)
        self.vbox.set_border_width(1)

        window.add(self.vbox)
        uimanager = self.create_ui_manager()
        uimanager.insert_action_group(action_group)

        menubar = uimanager.get_widget("/MenuBar")
        self.vbox.pack_start(menubar, False, True, 0)
        self.vbox.add(self.eventbox)
        self.eventbox.add(self.fixed)
        window.show_all()

    def run(self, widget, event):
        self.window2 = Gtk.Window()
        self.fixed2 = Gtk.Fixed()
        self.window2.add(self.fixed2)
        self.window2.show_all()
        self.fixed2.show_all()

        for key in self.save:
            button = Gtk.Button(self.save[key][4])
            button.set_size_request(self.save[key][2], self.save[key][3])
            self.fixed2.put(button, self.save[key][0], self.save[key][1])
            button.show()
        pass

    def init(self):
        for child in self.fixed.get_children():
            child.destroy()
        for key in self.save:
            self.bb = Gtk.EventBox()
            self.bb.set_border_width(1)
            self.bb.modify_bg(Gtk.StateFlags.NORMAL, Gdk.Color(red=65535,
                                                              green=65535,
                                                              blue=65535))
            self.bb.set_size_request(self.save[key][2], self.save[key][3])

            self.bb.connect('button-press-event', self.onButtonPress, key)
            self.bb.connect('motion-notify-event', self.move_key, key)
            self.bb.connect("enter-notify-event", self.test)
            self.bb.connect_object("event", self.onButtonRightClick, self.menu)
            self.menu_deleteButton.connect("button-press-event",
                                            self.removeButton,
                                            self.cont,
                                            self.bb)
            self.menu_optionEditProperties.connect("button-press-event",
                                                   self.editButton,
                                                   self.cont,
                                                   self.bb)
            self.bb.add(Gtk.Label(self.save[key][4]))
            self.fixed.put(self.bb, self.save[key][0], self.save[key][1])

    def test(self, widget, event):
        pass
        #if event.x <= 25:
         #   widget.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.SIZING))

    def openFromJSON(self, data):
        fileChooserDialog = Gtk.FileChooserDialog("Save Keyboard", None,
         Gtk.FileChooserAction.OPEN, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
         Gtk.STOCK_OK, Gtk.ResponseType.OK))
        keyboardFilter = Gtk.FileFilter()
        keyboardFilter.set_name("Keyboard Files")
        keyboardFilter.add_pattern("*.keyboard")
        fileChooserDialog.add_filter(keyboardFilter)
        response = fileChooserDialog.run()
        if response == Gtk.ResponseType.OK:
            fileName = fileChooserDialog.get_filename()
            print fileName
            f = open(fileName, "r")
            fr = f.readlines()
            self.save = json.loads(fr[0])
            self.init()
            self.window.show_all()
        elif response == Gtk.RESPONSE_CANCEL:
            pass
        fileChooserDialog.destroy()

    def saveToJSON(self, widget, data):
        fileChooserDialog = Gtk.FileChooserDialog("Save Keyboard", None,
         Gtk.FILE_CHOOSER_ACTION_SAVE, (Gtk.STOCK_CANCEL, Gtk.RESPONSE_CANCEL,
         Gtk.STOCK_OK, Gtk.RESPONSE_OK))
        response = fileChooserDialog.run()
        if response == Gtk.RESPONSE_OK:
            fileName = fileChooserDialog.get_filename()
            print fileName
            if not fileName.endswith('.keyboard'):
                fileName += ".keyboard"
            f = open(fileName, "w")
            f.write(json.dumps(self.save))

        elif response == Gtk.RESPONSE_CANCEL:
            pass
        fileChooserDialog.destroy()

        pass

    def add_file_menu_actions(self, action_group):
        action_filemenu = Gtk.Action("FileMenu", "File", None, None)
        action_group.add_action(action_filemenu)

        action_filenew = Gtk.Action("FileNewStandard", None, None, Gtk.STOCK_NEW)
        action_group.add_action(action_filenew)

        action_fileopen = Gtk.Action("FileOpen", None, None, Gtk.STOCK_OPEN)
        action_group.add_action(action_fileopen)
        action_fileopen.connect("activate", self.openFromJSON)

        action_filesave = Gtk.Action("FileSave", None, None, Gtk.STOCK_SAVE)
        action_group.add_action(action_filesave)

        action_filesaveas = Gtk.Action("FileSaveAs", None, None, Gtk.STOCK_SAVE_AS)
        action_group.add_action(action_filesaveas)
        action_filesaveas.connect("activate", self.saveToJSON)

        action_filequit = Gtk.Action("FileQuit", None, None, Gtk.STOCK_QUIT)
        action_group.add_action(action_filequit)




    def add_options_menu_actions(self, action_group):
        action_optionmenu = Gtk.Action("OptionMenu", "Options", None, None)
        action_group.add_action(action_optionmenu)

        action_optionrunkeyboard = Gtk.Action("OptionRunKeyboard", None, None, Gtk.STOCK_EXECUTE)
        action_group.add_action(action_optionrunkeyboard)


    def create_ui_manager(self):
        uimanager = Gtk.UIManager()

        # Throws exception if something went wrong
        uimanager.add_ui_from_string(UI_INFO)

        # Add the accelerator group to the toplevel window
        accelgroup = uimanager.get_accel_group()
        self.window.add_accel_group(accelgroup)
        return uimanager

    def get_main_menu(self, window):
        accel_group = Gtk.AccelGroup()
        item_factory = Gtk.ItemFactory(Gtk.MenuBar, "<main>", accel_group)

        item_factory.create_items(self.menu_items)

        window.add_accel_group(accel_group)

        self.item_factory = item_factory
        return item_factory.get_widget("<main>")

    def move_key(self, widget, event, key):
        self.evpos = self.save[key][0:2]
        self.evpos[0] += int(event.x - 25)
        self.evpos[1] += int(event.y - 25)
        self.fixed.move(widget, self.evpos[0], self.evpos[1])
        self.save[key][0:2] = self.evpos

    def change_name(self, widget, event, key, button):
        print event.keyval

        if event.keyval == 65293 or event.keyval == 65421:
            self.save[key][4] = widget.get_text()
            #self.save[key][2], self.save[key][3] = button.get_size_request()

            widget.destroy()
            button.add(Gtk.Label(self.save[key][4]))
            button.show_all()
            self.editing = False

    def onButtonDoubleClick(self, widget, event, key):
        self.editing = True
        print ("2 clicked")
        if widget.get_child() is not None:
            widget.remove(widget.get_child())
        entry = Gtk.Entry()

        if self.save[key][4] != "":
            entry.set_text(self.save[key][4])
        entry.set_can_focus(1)
        self.window.set_focus(entry)
        entry.grab_focus()
        entry.connect("key-press-event", self.change_name, key, widget)
        widget.add(entry)
        widget.show_all()
        #entry.set_size_request(50, 50)

    def new_button(self, widget, event):
        #print "new"
        w, h = INITIAL_W, INITIAL_H
        if event.keyval == 110 and self.editing is not True:
            try:
                x, y = self.save[self.save.keys()[-1]][0:2]
                w, h = self.save[self.save.keys()[-1]][2:4]
                print w,h
            except:
                x, y = INITIAL_X, INITIAL_Y
                w, h = INITIAL_W, INITIAL_H
            self.save[self.cont] = [x + w, y, 50, 50, ""]

            b = Gtk.EventBox()
            b.modify_bg(Gtk.StateFlags.NORMAL, Gdk.Color(red=65535,
                                                        green=65535,
                                                        blue=65535))
            b.set_border_width(1)
            b.set_size_request(self.save[self.cont][2], self.save[self.cont][3])
            b.connect('button-press-event', self.onButtonPress, self.cont)
            b.connect('motion-notify-event', self.move_key, self.cont)
            b.connect_object("event", self.onButtonRightClick, self.menu)
            self.menu_deleteButton.connect("button-press-event",
                                           self.removeButton,
                                           self.cont,
                                           b)
            self.menu_optionEditProperties.connect("button-press-event",
                                                   self.editButton,
                                                   self.cont,
                                                   b)
            self.fixed.put(b, self.save[self.cont][0], self.save[self.cont][1])
            self.window.show_all()

        self.cont += 1

    def onButtonPress(self, widget, event, key):
        if event.type == Gdk.EventType._2BUTTON_PRESS:
            self.onButtonDoubleClick(widget, event, key)

        else:
            self.evpos = self.save[key][0:2]
            self.evpos[0] += int(event.x - 25)
            self.evpos[1] += int(event.y - 25)

    def onButtonRelease(self, widget, event, key):
        #print "br"
        self.pos = self.save[key][0:2]
        if (self.evpos[0] != self.pos[0] and
            self.evpos[1] != self.pos[1]):
                self.fixed.remove(widget)
                self.pos[0] += int(event.x - 25)
                self.pos[1] += int(event.y - 25)
                self.save[key][0:2] = self.pos[0], self.pos[1]
                self.fixed.put(widget, self.pos[0], self.pos[1])
        else:
            pass

    def onButtonRightClick(self, widget, event):
        if event.type == Gdk.EventType.BUTTON_PRESS and event.button == 3:
            widget.popup(None, None, None, event.button, event.time)
            print
            pass

    def removeButton(self, widget, event, key, button):
        print button
        #button.destroy()
        #self.fixed.show_all()
        print key

    def editButton(self, widget, event, key, button):
        print key

if __name__ == "__main__":
    CustomKey()
    Gtk.main()
