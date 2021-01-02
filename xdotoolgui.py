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


import sys,runxdotool,glib,time,thread
try:
    import pygtk
    pygtk.require("2.0")
except:
    pass
try:
    import gtk
    import gtk.glade
except:
    sys.exit(1)

filename = 'new file'
MouseLocation = False

class xdotoolgui:
    """A gui for xdotool. Make it esay to used in gnome. """

    def __init__(self):
        
        #Set the Glade file
        self.wtree = gtk.glade.XML(sys.path[0]+'/xdotoolgui.glade')
        self.wtree.get_widget('window1').set_title('xdotool-gui')
        self.window = self.wtree.get_widget("window1")
        self.window.show()
        #Create our dictionay and connect it
        dic = { "on_imagemenuitem10_activate" : self.aboutdialog1_activate,
            "on_imagemenuitem1_activate" : self.newtext_activate,
            "on_imagemenuitem2_activate" : self.open_activate,
            "on_imagemenuitem3_activate" : self.save_activate,
            "on_imagemenuitem4_activate" : self.saveother_activate,
            "on_imagemenuitem5_activate" : gtk.main_quit,  
            "on_button1_clicked" : self.move_mouse,
            "on_button3_clicked" : self.click_mouse,
            "on_button4_clicked" : self.delay_time,
            "on_window1_destroy" : gtk.main_quit,
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
        self.wtree.signal_autoconnect(dic)
        self.wtree.get_widget('statusbar1').push(self.wtree.get_widget('statusbar1').get_context_id("file name"),filename)
        #thread.start_new_thread(xdotoolgui.threadmouse,(self,))
        #print 'sub thread id2222 : ', thread.get_ident()

    def aboutdialog1_activate(self, widget):
        #self.wtree = gtk.glade.XML(sys.path[0]+'/xdotoolgui.glade', 'aboutdialog1')
        self.aboutdialog1 = self.wtree.get_widget('aboutdialog1')
        self.aboutdialog1.show()
        
    def quitabout(self, widget):
        self.aboutdialog1.hide()
        
    def newtext_activate(self, widget):
        buffer=self.wtree.get_widget('textview1').get_buffer()
        buffer.set_text('')
        global filename
        filename = 'new file'
        self.wtree.get_widget('statusbar1').push(self.wtree.get_widget('statusbar1').get_context_id("file name"),filename)
        
    def open_activate(self, widget):
        #self.wtree = gtk.glade.XML(sys.path[0]+'/xdotoolgui.glade', 'filechooserdialog1')
        self.filechooserdialog1 = self.wtree.get_widget('filechooserdialog1')
        self.filechooserdialog1.show()
        
    def filechoose_activate(self, widget):
        self.filechooserdialog1.hide()
        #self.wtree.get_widget('window1').set_title('hehe')
        buffer=self.wtree.get_widget('textview1').get_buffer()
        global filename
        filename=self.filechooserdialog1.get_filename()
        self.wtree.get_widget('statusbar1').push(self.wtree.get_widget('statusbar1').get_context_id("FixStatus"),filename)
        f = open(filename, "r")
        buf = f.read()
        f.close()
        buffer.set_text(buf)
    
    def save_activate(self, widget):
        own = self.wtree.get_widget('textview1').get_buffer()
        start, end = own.get_bounds()
        chars = own.get_slice(start, end, False)
        global filename
        self.wtree.get_widget('statusbar1').push(self.wtree.get_widget('statusbar1').get_context_id("FixStatus"),filename)
        file = open(filename, "w")
        file.write(chars)
        file.close()
    def saveother_activate(self, widget):
        self.filechooserdialog2 = self.wtree.get_widget('filechooserdialog2')
        self.filechooserdialog2.show()
        
    def filesaveothercancel(self,widget):
        self.filechooserdialog2.hide()
    def filesaveother(self, widget):
        self.filechooserdialog2.hide()
        buffer=self.wtree.get_widget('textview1').get_buffer()
        global filename
        filename = self.filechooserdialog2.get_filename()
        own = self.wtree.get_widget('textview1').get_buffer()
        start, end = own.get_bounds()
        chars = own.get_slice(start, end, False)
        self.wtree.get_widget('statusbar1').push(self.wtree.get_widget('statusbar1').get_context_id("FixStatus"),filename)
        file = open(filename, "w")
        file.write(chars)
        file.close()
            
    def move_mouse(self, widget):
        self.dialog1 = self.wtree.get_widget('dialog1')
        self.dialog1.show()
        self.wtree.get_widget('entry_x').set_text('0')
        self.wtree.get_widget('entry_y').set_text('0')
    def movemousecancel(self, widget):
        self.dialog1.hide()
        
    def movethemouse(self, widget):
        own = self.wtree.get_widget('textview1').get_buffer()
        start, end = own.get_bounds()
        chars = own.get_slice(start, end, False)
        x=self.wtree.get_widget('entry_x').get_text()
        y=self.wtree.get_widget('entry_y').get_text()
        chars = chars +"move mouse to "+x+" "+y+ "\n"
        own.set_text(chars)
        self.dialog1.hide()
    def delay_cancel(self, widget):
        self.dialog2.hide()
    def delay_time(self, widget):
        self.dialog2 = self.wtree.get_widget('dialog2')
        self.dialog2.show()
        self.wtree.get_widget('entry_time1').set_text('1.0')
    def delay_clicked(self,widget):
        own = self.wtree.get_widget('textview1').get_buffer()
        start, end = own.get_bounds()
        chars = own.get_slice(start, end, False)
        x=self.wtree.get_widget('entry_time1').get_text()
        chars = chars +"delay "+x+" seconds\n"
        own.set_text(chars)
        self.dialog2.hide()
    def click_mouse(self,widget):
        self.dialog3 = self.wtree.get_widget('dialog3')
        self.dialog3.show()
        self.wtree.get_widget('entry_sum3').set_text('1')
        self.wtree.get_widget('entry_time3').set_text('0.0')
        self.wtree.get_widget('combobox1').set_active(0)
    def mouseclick(self,widget):
        own = self.wtree.get_widget('textview1').get_buffer()
        start, end = own.get_bounds()
        chars = own.get_slice(start, end, False)
        x=self.wtree.get_widget('entry_sum3').get_text()
        y=self.wtree.get_widget('entry_time3').get_text()
        n = self.wtree.get_widget('combobox1').get_active()
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
        self.dialog4 = self.wtree.get_widget('dialog4')
        self.dialog4.show()
        #self.wtree.get_widget('entry1').set_text(' ')
        self.wtree.get_widget('entry_sum4').set_text('1')
        self.wtree.get_widget('entry_time4').set_text('0.0')
    def keybord_click(self,widget):
        own = self.wtree.get_widget('textview1').get_buffer()
        start, end = own.get_bounds()
        chars = own.get_slice(start, end, False)
        x=self.wtree.get_widget('entry_sum4').get_text()
        y=self.wtree.get_widget('entry_time4').get_text()
        key=self.wtree.get_widget('entry1').get_text()
        chars = chars +"type keybord as "+key+" for "+x+" times then delay "+y+" seconds\n"
        own.set_text(chars)
        self.dialog4.hide()
    def keybordcancel(self,widget):
        self.dialog4.hide()
    def run(self,widget):
        own = self.wtree.get_widget('textview1').get_buffer()
        start, end = own.get_bounds()
        chars = own.get_slice(start, end, False)
        global filename
        self.wtree.get_widget('statusbar1').push(self.wtree.get_widget('statusbar1').get_context_id("FixStatus"),filename)
        file = open(filename, "w")
        file.write(chars)
        file.close()
        runxdotool.AddCommandToRun(filename)
    def mouselocation(self,widget):
        global MouseLocation
        a = 'get mouse location mode off'
        b = 'get mouse location mode on,now you can type any key like \'s\' to get the mouse location'
        if MouseLocation == True:
            MouseLocation = False
            self.wtree.get_widget('statusbar1').push(self.wtree.get_widget('statusbar1').get_context_id("FixStatus"),a)
        else:
            MouseLocation = True
            self.wtree.get_widget('statusbar1').push(self.wtree.get_widget('statusbar1').get_context_id("FixStatus"),b)
        #print 'main thread id : ', thread.get_ident()
        #thread.start_new_thread(xdotoolgui.threadmouse,(self,))
        #print 'main thread id2 : ', thread.get_ident()
    def threadmouse(self,widget,event):
        #print 'sub thread id : ', thread.get_ident()
        global MouseLocation
        if MouseLocation:
            glib.timeout_add(100, self.ThreadMouse)
    def ThreadMouse(self):
        f = gtk.Window()
        rootwin = f.get_screen().get_root_window()
        x,y,mods = rootwin.get_pointer()
        s = 'mouse location is ('+str(x)+',' + str(y)+')'
        self.wtree.get_widget('statusbar1').push(self.wtree.get_widget('statusbar1').get_context_id("FixStatus"),s)
        own = self.wtree.get_widget('textview1').get_buffer()
        start, end = own.get_bounds()
        chars = own.get_slice(start, end, False)
        chars = chars +"move mouse to "+str(x)+" "+str(y)+ "\n"
        own.set_text(chars)
            #time.sleep(0.01)
        #print 'sub thread id2 : ', thread.get_ident()
#thread.start_new_thread(xdotoolgui.threadmouse,())
if __name__ == "__main__":
    editor =xdotoolgui()
    #editor.window.show()
    gtk.main()
