#!/usr/bin/env python

import elementary, edje, ecore, e_dbus

class GeekogotchiUI_EFL:
  parent = None
  def __init__(self, p):
    self.parent = p
    elementary.init()
    self.win = elementary.Window('geekogotchi', elementary.ELM_WIN_BASIC)
    self.win.title_set('Geekogotchi')
    bg = elementary.Background(self.win)
    bg.show()
    self.win.resize_object_add(bg)
    self.win.destroy = self.windowClose
  def windowClose(self, *args, **kargs):
    self.parent.stop()
  def timer(self, interval, func):
    return ecore.timer_add(interval, func)
  def connect(self):
    self.parent.connect(mainloop = e_dbus.DBusEcoreMainLoop())
  def start(self):
    '''Start UI, mainloop etc.'''
    self.connect()
    self.win.show()
    elementary.run()
  def exit(self):
    '''Exit from UI mainloop'''
    elementary.exit()
  def destroy(self):
    '''Shutting down client'''
    self.parent.disconnect()
    elementary.shutdown()
