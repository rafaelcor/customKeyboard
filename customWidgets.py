# -*- coding: utf-8 -*-

# Copyright (C) 2015 Rafael Cordano <rafael.cordano@gmail.com>
# Copyright (C) 2015 Ezequiel Pereira <eze2307@gmail.com>
# Copyright (C) 2015 Franco Profeti <fprofeti98@gmail.com>
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

ENABLE_HANDLES = True
from gi.repository import Gtk, Gdk, GdkPixbuf
import cairo


class SpinButtonWithLabel(Gtk.HBox, Gtk.SpinButton):

    def set_adjustment(self, adjustment):
        self.spinbutton.set_adjustment(adjustment)

    def __init__(self, label):
        super(SpinButtonWithLabel, self).__init__()
        self.add(Gtk.Label(label))
        self.spinbutton = Gtk.SpinButton()
        self.add(self.spinbutton)


class ResizableEventBox(Gtk.EventBox):
    def __init__(self, fixed, x, y, w, h):
        super(ResizableEventBox, self).__init__()
        self.typec = 2
        self.fixed = fixed
        self.resizePos = []
        self.showResize = False
        self.lock = False
        self.can_focus_out = True
        self.dragevent = 0
        self.screen = Gdk.Screen.get_default()
        self.modify_bg(Gtk.StateFlags.NORMAL, Gdk.Color(red=65535,
                                                        green=65535,
                                                        blue=65535))
        self.set_events(Gdk.EventMask.POINTER_MOTION_MASK |
                        Gdk.EventMask.BUTTON_MOTION_MASK |
                        Gdk.EventMask.BUTTON1_MOTION_MASK |
                        Gdk.EventMask.BUTTON2_MOTION_MASK |
                        Gdk.EventMask.BUTTON3_MOTION_MASK)
        if ENABLE_HANDLES:
            self.connect("button-press-event", self.enableResize)
        self.connect("leave-notify-event", self.set_focus_out)
        self.connect("motion-notify-event", self.set_focus_in)
        self.connect("size-allocate", self.resized)
        im1, im2, im3, im4 = Gtk.Image(),Gtk.Image(),Gtk.Image(),Gtk.Image()
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(
                                                      "img/resizer.png",
                                                      12,
                                                      12
                                                      )

        im1.set_from_pixbuf(pixbuf)
        im2.set_from_pixbuf(pixbuf)
        im3.set_from_pixbuf(pixbuf)
        im4.set_from_pixbuf(pixbuf)

        self.img1, self.img2, self.img3, self.img4 = Gtk.EventBox(), Gtk.EventBox(), Gtk.EventBox(), Gtk.EventBox()

        self.img1.add(im1)
        self.img2.add(im2)
        self.img3.add(im3)
        self.img4.add(im4)

        self.img1.set_events(Gdk.EventMask.POINTER_MOTION_MASK)
        self.img1.connect("button-press-event", self.enableDrag)
        self.img1.connect("button-release-event", self.disableDrag)
        self.img1.connect("leave-notify-event", self.set_focus_out)
        self.img1.connect("motion-notify-event", self.set_focus_in)
        self.img4.set_events(Gdk.EventMask.POINTER_MOTION_MASK)
        self.img4.connect("button-press-event", self.enableDrag)
        self.img4.connect("button-release-event", self.disableDrag)
        self.img4.connect("leave-notify-event", self.set_focus_out)
        self.img4.connect("motion-notify-event", self.set_focus_in)
        self.img3.set_events(Gdk.EventMask.POINTER_MOTION_MASK)
        self.img3.connect("button-press-event", self.enableDrag)
        self.img3.connect("button-release-event", self.disableDrag)
        self.img3.connect("leave-notify-event", self.set_focus_out)
        self.img3.connect("motion-notify-event", self.set_focus_in)
        self.img2.set_events(Gdk.EventMask.POINTER_MOTION_MASK)
        self.img2.connect("button-press-event", self.enableDrag)
        self.img2.connect("button-release-event", self.disableDrag)
        self.img2.connect("leave-notify-event", self.set_focus_out)
        self.img2.connect("motion-notify-event", self.set_focus_in)


    def changePointer(self, widget, event, typec):
        if typec is 1:
            typec = Gdk.CursorType.SIZING
        else:
            typec = Gdk.CursorType.ARROW
        widget.get_toplevel().get_root_window(). \
                             set_cursor(Gdk.Cursor(Gdk.CursorType.SIZING))

    def moveResizer(self, widget, event):
        screen = self.screen
        if event.x > screen.get_width():
            event.x = screen.get_width()
        if abs(event.x) > screen.get_width():
            event.x = screen.get_width()

        if event.x < 0:
            event.x = 0

        if event.y > screen.get_height():
            event.y = screen.get_height()
        if abs(event.y) > screen.get_height():
            event.y = screen.get_height()
        if event.y < 0:
            event.y = 0

        print "event.x: %s"%event.x
        print "event.y: %s"%event.y
        print event.get_window().get_position()
        self.evpos = [widget.get_allocation().x, widget.get_allocation().y]
        self.evpos[0] -= widget.get_allocation().width/2
        self.evpos[1] -= widget.get_allocation().height/2
        print self.evpos, event.x, event.y
        if self.evpos[0] in range(0, screen.get_width()+1):
            self.evpos[0] += int(abs(event.x))
            self.evpos[0] = abs(self.evpos[0])
            self.evpos[1] += int(abs(event.y))
            self.evpos[1] = abs(self.evpos[1])
            print "E0", self.evpos
            self.fixed.remove(widget)
            self.fixed.put(widget, self.evpos[0], self.evpos[1])
        if widget == self.img1:
            self.fixed.remove(self.img3)
            self.fixed.remove(self.img4)
            self.fixed.put(self.img3, self.evpos[0], self.img3.get_allocation().y)
            self.fixed.put(self.img4, self.img4.get_allocation().x, self.evpos[1])
        if widget == self.img2:
            self.fixed.remove(self.img3)
            self.fixed.remove(self.img4)
            self.fixed.put(self.img4, self.evpos[0], self.img4.get_allocation().y)
            self.fixed.put(self.img3, self.img3.get_allocation().x, self.evpos[1])
        if widget == self.img3:
            self.fixed.remove(self.img1)
            self.fixed.remove(self.img2)
            self.fixed.put(self.img1, self.evpos[0], self.img1.get_allocation().y)
            self.fixed.put(self.img2, self.img2.get_allocation().x, self.evpos[1])
        if widget == self.img4:
            self.fixed.remove(self.img1)
            self.fixed.remove(self.img2)
            self.fixed.put(self.img2, self.evpos[0], self.img2.get_allocation().y)
            self.fixed.put(self.img1, self.img1.get_allocation().x, self.evpos[1])

        x = self.img1.get_allocation().x
        y = self.img1.get_allocation().y
        w = self.img2.get_allocation().x-self.img1.get_allocation().x
        h = self.img2.get_allocation().y-self.img1.get_allocation().y
        self.fixed.move(self, x, y)
        self.set_size_request(abs(w), abs(h))

    def enableDrag(self, widget, event):
        self.dragevent = widget.connect("motion-notify-event", self.moveResizer)

    def disableDrag(self, widget, event):
        widget.disconnect(self.dragevent)
        self.dragevent = 0

    def enableResize(self, widget, event):
        print "this works"
        print event.button
        self.typec = 1
        if self.showResize:
            return
        self.can_focus_out = False
        self.showResize = True

        if not self.lock:
            self.lock = True
            self.fixed.put(self.img1, self.pos[0], self.pos[1]) # Arriba-Izquierda
            self.fixed.put(self.img2, self.pos[0]+self.pos[3], self.pos[1]+self.pos[2]) # Abajo-Derecha
            self.fixed.put(self.img3, self.pos[0], self.pos[1]+self.pos[2]) # Abajo-Izquierda
            self.fixed.put(self.img4, self.pos[0]+self.pos[3], self.pos[1]) # Arriba-Derecha

            self.img1.connect("enter-notify-event", self.changePointer, self.typec)
            self.img2.connect("enter-notify-event", self.changePointer, self.typec)
            self.img3.connect("enter-notify-event", self.changePointer, self.typec)
            self.img4.connect("enter-notify-event", self.changePointer, self.typec)

        self.fixed.show_all()

    def disableResize(self):
        self.typec = 2
        self.showResize = False
        self.img1.hide()
        self.img2.hide()
        self.img3.hide()
        self.img4.hide()

    def set_focus_out(self, widget, event):
        if not self.dragevent:
            self.can_focus_out = True
            return
        self.moveResizer(widget, event)

    def set_focus_in(self, *args):
        self.can_focus_out = False

    def resized(self, widget, event):
        self.pos = [event.x, event.y, event.width, event.height]
        print self.pos

    def relocate_handles(self, *args):
        self.fixed.move(self.img1, self.pos[0], self.pos[1])
        self.fixed.move(self.img2, self.pos[0]+self.pos[3], self.pos[1]+self.pos[2])
        self.fixed.move(self.img3, self.pos[0], self.pos[1]+self.pos[2])
        self.fixed.move(self.img4, self.pos[0]+self.pos[3], self.pos[1])


class TransparentWindowWithBorder(Gtk.Window):

    def __init__(self, width, heigth, xpos, ypos):
        super(TransparentWindowWithBorder, self).__init__()

        self.width = width
        self.heigth = heigth
        self.xpos = xpos
        self.ypos = ypos

        self.tran_setup()
        self.init_ui()

    def init_ui(self):
        self.set_decorated(False)
        self.connect("draw", self.on_draw)

        self.set_title("Transparent window")
        self.resize(self.width, self.heigth)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.connect("delete-event", Gtk.main_quit)
        self.show_all()

    def tran_setup(self):

        self.set_app_paintable(True)
        screen = self.get_screen()

        visual = screen.get_rgba_visual()
        if visual is not None and screen.is_composited():
            self.set_visual(visual)

    def on_draw(self, wid, cr):

        cr.set_source_rgba(0.0, 0.0, 0.0, 0.0)
        cr.set_operator(cairo.OPERATOR_SOURCE)
        cr.paint()

        cr.set_line_width(9.0)

        cr.rectangle(0, 0, self.width, self.heigth)
        cr.set_source_rgba(0.0, 1.0, 0.0, .75)
        cr.stroke()

    def changeSizeAndPosition(self, newWidth, newHeigth, newPosX, newPosY):
        self.width = newWidth
        self.heigth = newHeigth
        self.xpos = newPosX
        self.ypos = newPosY
        self.resize(newWidth, newHeigth)
        self.move(newPosX, newPosY)