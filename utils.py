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
      <menuitem action='OptionSetKeyboardWindow' />
    </menu>
    <menu action='HelpMenu'>
      <menuitem action='Help'/>
      <menuitem action=
'About'/>
    </menu>
  </menubar>
  <toolbar name='ToolBar'>
    <toolitem action='FileNewStandard' />
    <toolitem action='FileOpen' />
    <toolitem action='FileQuit' />
  </toolbar>
</ui>
"""