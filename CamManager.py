#!/usr/bin/env python3
from gi.repository import Gtk
import sys
import os
import subprocess

module_video="uvcvideo"

class MyWindow(Gtk.ApplicationWindow):
    # a window

    def __init__(self, app):
        Gtk.Window.__init__(self, title="WebCam Manager", application=app)
        self.set_default_size(250, 50)

        # a button
        button = Gtk.Button()
        # with a label
        label =  label_construct()
        button.set_label(label)
        # connect the signal "clicked" emitted by the button
        # to the callback function do_clicked
        button.connect("clicked", self.do_clicked)
        # add the button to the window
        self.add(button)

    # callback function connected to the signal "clicked" of the button
    def do_clicked(self, button):
        loaded = module_loaded(module_video) 
        if loaded == True:
           disable_cam()
           label="WebCam Disable"
        else:
           enable_cam()
           label="WebCam Enable"
        button.set_label(label)

class MyApplication(Gtk.Application):

    def __init__(self):
        Gtk.Application.__init__(self)

    def do_activate(self):
        win = MyWindow(self)
        win.show_all()

    def do_startup(self):
        Gtk.Application.do_startup(self)


def module_loaded(module_name):
    """Checks if module is loaded"""
    lsmod_proc = subprocess.Popen(['lsmod'], stdout=subprocess.PIPE)
    grep_proc = subprocess.Popen(['grep', module_name], stdin=lsmod_proc.stdout)
    grep_proc.communicate()  # Block until finished
    return grep_proc.returncode == 0


def disable_cam():
    subprocess.call(["/usr/sbin/modprobe", "-r", "uvcvideo"])

def enable_cam():
    subprocess.call(["modprobe", module_video])

def label_construct():
    loaded = module_loaded(module_video)
    if loaded == True:
      label="WebCam Enable"
    else:
      label="WebCam Disable"
    return label

app = MyApplication()
exit_status = app.run(sys.argv)
sys.exit(exit_status)
