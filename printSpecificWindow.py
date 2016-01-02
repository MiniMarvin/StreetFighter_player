import pygtk
pygtk.require('2.0')
import gtk
import wnck
import re
import sys
import time
import pyautogui
import pyscreenshot as ps

screen = wnck.screen_get_default()
while gtk.events_pending():
	gtk.main_iteration()

titlePattern = re.compile('.*oogle.*')
titlePattern = re.compile('.*oogle.*')

windows = screen.get_windows()
activew = screen.get_active_window()

for w in windows:
	if titlePattern.match(w.get_name()):
		w.activate(int(time.time()))
		bbox=(w.get_geometry())
		ps.grab_to_file("capture.png",bbox)
		print(str(w.get_name())+"\n")
		print(str(bbox)+"\n")
		#w.activate(int(time.time()))

activew.activate(int(time.time()))	