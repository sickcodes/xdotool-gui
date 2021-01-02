#!/usr/bin/env python
# xdotool-gui v3.0
# License: GPLv3
# Notice Written by Sick.Codes, January 2021
# Authors:  @sickcodes


#!/usr/bin/env python
#
#       xdotoolgui.py - GUI for xdotool
#       
#       Copyright 2010 esbat <esbatmop@gmail.com>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

import sys
import time
# import thread
import subprocess
import string
import tempfile

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import Gio
from gi.repository import GLib


try:
    import pygtk
    pygtk.require("2.0")
except:
    pass
# try:
#     import gtk
#     import gtk.glade
# except:
#     sys.exit(1)

filename = tempfile.NamedTemporaryFile(delete=True).name #'./.xdotool-script'
MouseLocation = False

class xdotoolgui:
    """A gui for xdotool. Make it esay to used in gnome. """

    def __init__(self):
        #Set the Glade file
        self.builder = Gtk.Builder()
        # try:
        # self.builder.add_from_file("test.ui")
        self.builder.add_from_file("xdotoolgui.glade")
        # except:
        #     print("Error file not found")
        #     sys.exit()

        self.builder.get_object('window1').set_title('xdotool-gui')
        self.window = self.builder.get_object("window1")
        self.window.show()
        #Create our dictionary and connect it
        dic = { "on_imagemenuitem10_activate" : self.aboutdialog1_activate,
            "on_imagemenuitem1_activate" : self.newtext_activate,
            "on_imagemenuitem2_activate" : self.open_activate,
            "on_imagemenuitem3_activate" : self.save_activate,
            "on_imagemenuitem4_activate" : self.saveother_activate,
            # "on_imagemenuitem5_activate" : self.main_quit, ##########
            "on_button1_clicked" : self.move_mouse,
            "on_button3_clicked" : self.click_mouse,
            "on_button4_clicked" : self.delay_time,
            # "on_window1_destroy" : self.main_quit, ##################
            "on_cancel_clicked" : self.filesaveothercancel,
            "on_saveother_clicked": self.filesaveother,
            "on_movemousecancel_clicked" : self.movemousecancel,
            "on_movethemouse_clicked" : self.movethemouse,
            "on_filechooserdialog1_file_activated" : self.filechoose_activate,
            "on_delay_clicked" : self.delay_clicked,
            "on_delaycancel_clicked" : self.delay_cancel,
            "on_mouseclick_clicked" : self.mouseclick,
            "on_mouseclickcancel_clicked" : self.mouseclickcancel,
            "on_keybord_clicked" : self.keybord_clicked,
            "on_keybordclick1_clicked" : self.keybord_click,
            "on_keybordcancel_clicked" : self.keybordcancel,
            "on_button5_clicked" : self.run,
            "on_togglebutton1_toggled" : self.mouselocation,
            "on_window1_expose_event" : self.threadmouse,
            "on_aboutdialog1_close" : self.quitabout}
        self.builder.connect_signals(dic)
        self.builder.get_object('statusbar1').push(self.builder.get_object('statusbar1').get_context_id("file name"),filename)
        #thread.start_new_thread(xdotoolgui.threadmouse,(self,))
        #print 'sub thread id2222 : ', thread.get_ident()

    def aboutdialog1_activate(self, widget):
        #self.builder = gtk.glade.XML(sys.path[0]+'/xdotoolgui.glade', 'aboutdialog1')
        self.aboutdialog1 = self.builder.get_object('aboutdialog1')
        self.aboutdialog1.show()
        
    def quitabout(self, widget):
        self.aboutdialog1.hide()
        
    def newtext_activate(self, widget):
        buffer=self.builder.get_object('textview1').get_buffer()
        buffer.set_text('')
        global filename
        filename = tempfile.NamedTemporaryFile(delete=True).name
        self.builder.get_object('statusbar1').push(self.builder.get_object('statusbar1').get_context_id("file name"),filename)
        
    def open_activate(self, widget):
        #self.builder = gtk.glade.XML(sys.path[0]+'/xdotoolgui.glade', 'filechooserdialog1')
        self.filechooserdialog1 = self.builder.get_object('filechooserdialog1')
        self.filechooserdialog1.show()
        
    def filechoose_activate(self, widget):
        self.filechooserdialog1.hide()
        #self.builder.get_object('window1').set_title('hehe')
        buffer=self.builder.get_object('textview1').get_buffer()
        global filename
        filename=self.filechooserdialog1.get_filename()
        self.builder.get_object('statusbar1').push(self.builder.get_object('statusbar1').get_context_id("FixStatus"),filename)
        f = open(filename, "r")
        buf = f.read()
        f.close()
        buffer.set_text(buf)
    
    def save_activate(self, widget):
        own = self.builder.get_object('textview1').get_buffer()
        start, end = own.get_bounds()
        chars = own.get_slice(start, end, False)
        global filename
        self.builder.get_object('statusbar1').push(self.builder.get_object('statusbar1').get_context_id("FixStatus"),filename)
        file = open(filename, "w")
        file.write(chars)
        file.close()
    def saveother_activate(self, widget):
        self.filechooserdialog2 = self.builder.get_object('filechooserdialog2')
        self.filechooserdialog2.show()
        
    def filesaveothercancel(self,widget):
        self.filechooserdialog2.hide()
    def filesaveother(self, widget):
        self.filechooserdialog2.hide()
        buffer=self.builder.get_object('textview1').get_buffer()
        global filename
        filename = self.filechooserdialog2.get_filename()
        own = self.builder.get_object('textview1').get_buffer()
        start, end = own.get_bounds()
        chars = own.get_slice(start, end, False)
        self.builder.get_object('statusbar1').push(self.builder.get_object('statusbar1').get_context_id("FixStatus"),filename)
        file = open(filename, "w")
        file.write(chars)
        file.close()
            
    def move_mouse(self, widget):
        self.dialog1 = self.builder.get_object('dialog1')
        self.dialog1.show()
        self.builder.get_object('entry_x').set_text('0')
        self.builder.get_object('entry_y').set_text('0')
    def movemousecancel(self, widget):
        self.dialog1.hide()
        
    def movethemouse(self, widget):
        own = self.builder.get_object('textview1').get_buffer()
        start, end = own.get_bounds()
        chars = own.get_slice(start, end, False)
        x=self.builder.get_object('entry_x').get_text()
        y=self.builder.get_object('entry_y').get_text()
        chars = chars +"move mouse to "+x+" "+y+ "\n"
        own.set_text(chars)
        self.dialog1.hide()
    def delay_cancel(self, widget):
        self.dialog2.hide()
    def delay_time(self, widget):
        self.dialog2 = self.builder.get_object('dialog2')
        self.dialog2.show()
        self.builder.get_object('entry_time1').set_text('1.0')
    def delay_clicked(self,widget):
        own = self.builder.get_object('textview1').get_buffer()
        start, end = own.get_bounds()
        chars = own.get_slice(start, end, False)
        x=self.builder.get_object('entry_time1').get_text()
        chars = chars +"delay "+x+" seconds\n"
        own.set_text(chars)
        self.dialog2.hide()
    def click_mouse(self,widget):
        self.dialog3 = self.builder.get_object('dialog3')
        self.dialog3.show()
        self.builder.get_object('entry_sum3').set_text('1')
        self.builder.get_object('entry_time3').set_text('0.0')
        self.builder.get_object('combobox1').set_active(0)
    def mouseclick(self,widget):
        own = self.builder.get_object('textview1').get_buffer()
        start, end = own.get_bounds()
        chars = own.get_slice(start, end, False)
        x=self.builder.get_object('entry_sum3').get_text()
        y=self.builder.get_object('entry_time3').get_text()
        n = self.builder.get_object('combobox1').get_active()
        if n == 0:
            m = "left"
        if n == 1:
            m = "right"
        if n == 2:
            m = "middle"
        chars = chars +"click mouse "+m+" button for "+x+" times then delay "+y+" seconds\n"
        own.set_text(chars)
        self.dialog3.hide()
    def mouseclickcancel(self,widget):
        self.dialog3.hide()
    def keybord_clicked(self,widget):
        self.dialog4 = self.builder.get_object('dialog4')
        self.dialog4.show()
        #self.builder.get_object('entry1').set_text(' ')
        self.builder.get_object('entry_sum4').set_text('1')
        self.builder.get_object('entry_time4').set_text('0.0')
    def keybord_click(self,widget):
        own = self.builder.get_object('textview1').get_buffer()
        start, end = own.get_bounds()
        chars = own.get_slice(start, end, False)
        x = self.builder.get_object('entry_sum4').get_text()
        y = self.builder.get_object('entry_time4').get_text()
        key = self.builder.get_object('entry1').get_active_text()
        if self.builder.get_object('entry1_text').get_text() != '':
            key = self.builder.get_object('entry1_text').get_text()
        chars = chars +"type keybord as "+key+" for "+x+" times then delay "+y+" seconds\n"
        own.set_text(chars)
        self.dialog4.hide()
    def keybordcancel(self,widget):
        self.dialog4.hide()
    def run(self,widget):
        own = self.builder.get_object('textview1').get_buffer()
        start, end = own.get_bounds()
        chars = own.get_slice(start, end, False)
        global filename
        self.builder.get_object('statusbar1').push(self.builder.get_object('statusbar1').get_context_id("FixStatus"),filename)
        file = open(filename, "w")
        file.write(chars)
        file.close()
        self.add_command_to_run(filename)
    def mouselocation(self,widget):
        global MouseLocation
        a = 'get mouse location mode off'
        b = 'get mouse location mode on,now you can type any key like \'s\' to get the mouse location'
        if MouseLocation == True:
            MouseLocation = False
            self.builder.get_object('statusbar1').push(self.builder.get_object('statusbar1').get_context_id("FixStatus"),a)
        else:
            MouseLocation = True
            self.builder.get_object('statusbar1').push(self.builder.get_object('statusbar1').get_context_id("FixStatus"),b)
        #print 'main thread id : ', thread.get_ident()
        #thread.start_new_thread(xdotoolgui.threadmouse,(self,))
        #print 'main thread id2 : ', thread.get_ident()
    def threadmouse(self,widget,event):
        #print 'sub thread id : ', thread.get_ident()
        global MouseLocation
        if MouseLocation:
            GLib.timeout_add(100, self.ThreadMouse)
    def ThreadMouse(self):
        f = Gtk.Window()
        rootwin = f.get_screen().get_root_window()
        pointer = rootwin.get_pointer()
        x,y = pointer.x,pointer.y
        s = 'mouse location is ('+str(x)+',' + str(y)+')'
        self.builder.get_object('statusbar1').push(self.builder.get_object('statusbar1').get_context_id("FixStatus"),s)
        own = self.builder.get_object('textview1').get_buffer()
        start, end = own.get_bounds()
        chars = own.get_slice(start, end, False)
        chars = chars +"move mouse to "+str(x)+" "+str(y)+ "\n"
        own.set_text(chars)
    def add_command_to_run(self, command_path):
        # print(command_path)
        self.command_path = command_path
        afile = open(self.command_path)
        command_parameters = afile.read().split("\n")
        for s in command_parameters:
            command = s.split(" ")
            if command[0] == 'move':
                subprocess.check_call(["xdotool","mousemove",command[3],command[4]])
            if command[0] == 'delay':
                time.sleep(string.atof(command[1]))
            if command[0] == 'click':
                if command[2] == 'left':
                    for i in command[5]:
                        subprocess.check_call(["xdotool","click","1"])
                        time.sleep(string.atof(command[9]))
                if command[2] == 'middle':
                    for i in command[5]:
                        subprocess.check_call(["xdotool","click","2"])
                        time.sleep(string.atof(command[9]))
                if command[2] == 'right':
                    for i in command[5]:
                        subprocess.check_call(["xdotool","click","3"])
                        time.sleep(string.atof(command[9]))
            if command[0] == 'type':
                for i in command[5]:
                    subprocess.check_call(["xdotool","key",command[3]])
                    time.sleep(string.atof(command[9]))
        return 0
            #time.sleep(0.01)
        #print 'sub thread id2 : ', thread.get_ident()
#thread.start_new_thread(xdotoolgui.threadmouse,())
if __name__ == "__main__":
    editor =xdotoolgui()
    #editor.window.show()
    Gtk.main()
    


