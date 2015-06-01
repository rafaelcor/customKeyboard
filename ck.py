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
import gtk
#import gobject

INITIAL_X, INITIAL_Y = 0, 50


class CustomKey:
    def __init__(self):
        self.menu_items = (
            ("/_File",         None,         None, 0, "<Branch>"),
            ("/File/_New",     "<control>N", None, 0, None),
            ("/File/_Open",    "<control>O", self.openFromJSON, 0, None ),
            ("/File/_Save",    "<control>S", None, 0, None ),
            ("/File/Save _As", None,         self.saveToJSON, 0, None ),
            ("/File/sep1",     None,         None, 0, "<Separator>" ),
            ("/File/Quit",     "<control>Q", gtk.main_quit, 0, None ),
            ("/_Options",      None,         None, 0, "<Branch>" ),
            ("/Options/Run keyboard",  "<control>R", self.run , 0, None ),
            ("/_Help",         None,         None, 0, "<LastBranch>" ),
            ("/_Help/About",   None,         None, 0, None ),
            )
        self.mousePosition = []
        self.cont = 1
        self.save = {}  # "button name":[x, y, sx, sy , label, func]
        self.edit = 0
        self.evpos = []
        window = gtk.Window()
        self.window = window
        window.set_size_request(window.get_screen().get_width(),
                                window.get_screen().get_height() / 3)
        self.eventbox = gtk.EventBox()
        self.eventbox.set_events(
            gtk.gdk.BUTTON_MOTION_MASK |               # restoring missed masks
            gtk.gdk.BUTTON1_MOTION_MASK |
            gtk.gdk.BUTTON2_MOTION_MASK |
            gtk.gdk.BUTTON3_MOTION_MASK
        )
        self.fixed = gtk.Fixed()
        self.fixed.set_size_request(window.get_screen().get_width(),
                                    window.get_screen().get_height() / 3
                                    )

        self.menu = gtk.Menu()
        self.menu_optionEditProperties = gtk.MenuItem("Edit Properties")
        self.menu_deleteButton = gtk.MenuItem("Remove Button")
        self.menu.add(self.menu_optionEditProperties)
        self.menu.add(self.menu_deleteButton)
        self.menu.show_all()

        self.init()
        window.add_events(gtk.gdk.MOTION_NOTIFY | gtk.gdk.BUTTON_PRESS)

        window.connect("key-press-event", self.new_button)
        window.connect("destroy", gtk.main_quit)

        self.vbox = gtk.VBox(False, 1)
        self.vbox.set_border_width(1)

        window.add(self.vbox)
        menubar = self.get_main_menu(window)
        self.vbox.pack_start(menubar, False, True, 0)
        self.vbox.add(self.eventbox)
        self.eventbox.add(self.fixed)
        window.show_all()

    def run(self, widget, event):
        self.window2 = gtk.Window()
        self.fixed2 = gtk.Fixed()
        self.window2.add(self.fixed2)
        self.window2.show_all()
        self.fixed2.show_all()

        for key in self.save:
            button = gtk.Button(self.save[key][4])
            button.set_size_request(self.save[key][2], self.save[key][3])
            self.fixed2.put(button, self.save[key][0], self.save[key][1])
            button.show()
        pass

    def init(self):
        for child in self.fixed.get_children():
            child.destroy()
        for key in self.save:
            self.bb = gtk.EventBox()
            self.bb.set_border_width(1)
            self.bb.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(red=65535,
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
            self.bb.add(gtk.Label(self.save[key][4]))
            self.fixed.put(self.bb, self.save[key][0], self.save[key][1])

    def test(self, widget, event):
        pass
        #if event.x <= 25:
         #   widget.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.SIZING))

    def openFromJSON(self, widget, data):
        fileChooserDialog = gtk.FileChooserDialog("Save Keyboard", None,
         gtk.FILE_CHOOSER_ACTION_OPEN, (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
         gtk.STOCK_OK, gtk.RESPONSE_OK))
        keyboardFilter = gtk.FileFilter()
        keyboardFilter.set_name("Keyboard Files")
        keyboardFilter.add_pattern("*.keyboard")
        fileChooserDialog.add_filter(keyboardFilter)
        response = fileChooserDialog.run()
        if response == gtk.RESPONSE_OK:
            fileName = fileChooserDialog.get_filename()
            print fileName
            f = open(fileName, "r")
            fr = f.readlines()
            self.save = json.loads(fr[0])
            self.init()
            self.window.show_all()
        elif response == gtk.RESPONSE_CANCEL:
            pass
        fileChooserDialog.destroy()

    def saveToJSON(self, widget, data):
        fileChooserDialog = gtk.FileChooserDialog("Save Keyboard", None,
         gtk.FILE_CHOOSER_ACTION_SAVE, (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
         gtk.STOCK_OK, gtk.RESPONSE_OK))
        response = fileChooserDialog.run()
        if response == gtk.RESPONSE_OK:
            fileName = fileChooserDialog.get_filename()
            print fileName
            if not fileName.endswith('.keyboard'):
                fileName += ".keyboard"
            f = open(fileName, "w")
            f.write(json.dumps(self.save))

        elif response == gtk.RESPONSE_CANCEL:
            pass
        fileChooserDialog.destroy()

        pass

    def get_main_menu(self, window):
        accel_group = gtk.AccelGroup()
        item_factory = gtk.ItemFactory(gtk.MenuBar, "<main>", accel_group)

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
            widget.destroy()
            button.add(gtk.Label(self.save[key][4]))
            button.show_all()

    def onButtonDoubleClick(self, widget, event, key):
        print ("2 clicked")
        if widget.get_child() is not None:
            widget.remove(widget.get_child())
        entry = gtk.Entry()
        if self.save[key][4] != "":
            entry.set_text(self.save[key][4])
        entry.set_can_focus(1)
        self.window.set_focus(entry)
        entry.grab_focus()
        entry.connect("key-press-event", self.change_name, key, widget)
        widget.add(entry)
        widget.show_all()

    def new_button(self, widget, event):
        #print "new"
        if event.keyval == 110:
            try:
                x, y = self.save[self.save.keys()[-1]][0:2]
            except:
                x, y = INITIAL_X, INITIAL_Y
            self.save[self.cont] = [x + 50, y, 50, 50, ""]

            b = gtk.EventBox()
            b.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(red=65535,
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

        if event.type == gtk.gdk._2BUTTON_PRESS:
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
        if event.type == gtk.gdk.BUTTON_PRESS and event.button == 3:
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
    gtk.main()
