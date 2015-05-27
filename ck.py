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

import gtk
#import gobject


class CustomKey:
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
            x, y = self.save[self.save.keys()[-1]][0:2]
            self.save[self.cont] = [x + 50, y, 50, 50, ""]

            b = gtk.EventBox()
            b.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(red=65535, green=65535, blue=65535))

            b.set_size_request(self.save[self.cont][2], self.save[self.cont][3])
            b.connect('button-press-event', self.move_key, self.cont)
            b.connect('motion-notify-event', self.move_key, self.cont)
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

    def __init__(self):
        self.mousePosition = []
        self.cont = 2
        self.save = {1:
                    [50, 50, 50, 50, ""]}  # "button name":[x, y, sx, sy func]
        self.edit = 0
        self.evpos = []
        #self.pos = [50, 50]
        window = gtk.Window()
        self.window = window
        window.set_size_request(500, 500)
        self.eventbox = gtk.EventBox()
        self.eventbox.set_events(
            gtk.gdk.BUTTON_MOTION_MASK|               # restoring missed masks
            gtk.gdk.BUTTON1_MOTION_MASK|
            gtk.gdk.BUTTON2_MOTION_MASK|
            gtk.gdk.BUTTON3_MOTION_MASK
        )
        self.fixed = gtk.Fixed()

        for key in self.save:
            self.bb = gtk.EventBox()
            self.bb.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(red=65535, green=65535, blue=65535))
            #self.bq.set_size_request(50, 50)
            self.bb.set_size_request(self.save[key][2], self.save[key][3])
            #self.b.connect("button-press-event", self.onButtonPress, key)
            #self.b.connect("button-release-event", self.onButtonRelease, key)
            #self.eventbox.connect('button-press-event', self.onButtonPress, self.b, key)
            #self.eventbox.connect('motion-notify-event', self.onButtonPress, self.b, key)

            self.bb.connect('button-press-event', self.onButtonPress, key)
            self.bb.connect('motion-notify-event', self.move_key, key)
            self.fixed.put(self.bb, self.save[key][0], self.save[key][1])

        window.add_events(gtk.gdk.MOTION_NOTIFY | gtk.gdk.BUTTON_PRESS)

        window.connect("key-press-event", self.new_button)
        window.connect("destroy", gtk.main_quit)



        window.add(self.eventbox)
        self.eventbox.add(self.fixed)
        window.show_all()

if __name__ == "__main__":
    CustomKey()
    gtk.main()
