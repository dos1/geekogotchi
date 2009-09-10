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
    box = elementary.Box(self.win)
    self.win.resize_object_add(box)
    box.show()

    self.age = elementary.Label(self.win)
    box.pack_start(self.age)
    self.age.show()

    self.state = elementary.Label(self.win)
    box.pack_end(self.state)
    self.state.show()

    self.health = elementary.Label(self.win)
    box.pack_end(self.health)
    self.health.show()

    self.hungry = elementary.Label(self.win)
    box.pack_end(self.hungry)
    self.hungry.show()

    self.happy = elementary.Label(self.win)
    box.pack_end(self.happy)
    self.happy.show()

  def windowClose(self, *args, **kargs):
    self.parent.stop()
  def timer(self, interval, func):
    return ecore.timer_add(interval, func)
  def connect(self):
    self.parent.connect(mainloop = e_dbus.DBusEcoreMainLoop())
    print self.parent.serverVersion()
    self.parent.addPet()
  def update(self, props):
    self.age.label_set('Age: '+str(props['Age'])+' years')
    if props['Alive'] and not props['Borned']:
      self.state.label_set('Not borned yet')
    elif props['Dead']:
      self.state.label_set('Dead')
    else:
      self.state.label_set('')
      self.happy.label_set('Happiness: '+str(props['Happiness'])+'%')
      self.health.label_set('Health: '+str(props['Health'])+'%')
      self.hungry.label_set('Hungriness: '+str(props['Hungriness'])+'%')
  def start(self):
    '''Start UI, mainloop etc.'''
    self.win.show()
    elementary.run()
  def exit(self):
    '''Exit from UI mainloop'''
    elementary.exit()
  def destroy(self):
    '''Shutting down client'''
    self.parent.disconnect()
    elementary.shutdown()
