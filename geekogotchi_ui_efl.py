#!/usr/bin/env python

import elementary

class GeekogotchiUI_EFL:
  parent = None
  def __init__(self, p):
    self.parent = p
    elementary.init()
  def start(self):
    '''Start UI, mainloop etc.'''
    self.parent.connect()
    elementary.run()
  def exit(self):
    '''Exit from UI mainloop'''
    elementary.exit()
  def destroy(self):
    '''Shutting down client'''
    self.parent.disconnect()

