#!/usr/bin/env python

import elementary, edje, ecore, e_dbus
from functools import partial

class GeekogotchiUI_EFL:
  parent = None
  def __init__(self, p):
    self.parent = p
    self.petid = -1
    elementary.init()
    self.win = elementary.Window('geekogotchi', elementary.ELM_WIN_BASIC)
    self.win.title_set('Geekogotchi')
    bg = elementary.Background(self.win)
    bg.show()
    self.win.resize_object_add(bg)
    self.win.destroy = self.windowClose
    frame = elementary.Frame(self.win)
    box = elementary.Box(self.win)
    frame.content_set(box)
    frame.show()
    self.win.resize_object_add(frame)
    box.show()

    self.age = elementary.Label(self.win)
    box.pack_start(self.age)
    self.age.show()

    self.state = elementary.Label(self.win)
    box.pack_end(self.state)
    self.state.show()

    self.values = elementary.Box(self.win)
    self.values.show()
    box.pack_end(self.values)

    self.health = elementary.Label(self.win)
    self.values.pack_end(self.health)
    self.health.show()

    self.hungry = elementary.Label(self.win)
    self.values.pack_end(self.hungry)
    self.hungry.show()

    self.happy = elementary.Label(self.win)
    self.values.pack_end(self.happy)
    self.happy.show()

    self.buttons = elementary.Box(self.win)
    self.buttons.horizontal_set(True)
    self.buttons.homogenous_set(True)
    box.pack_end(self.buttons)
    self.buttons.show()

    self.feed = elementary.Button(self.win)
    self.feed.label_set('Feed')
    self.feed.clicked = self.feedPet
    self.buttons.pack_end(self.feed)
    self.feed.show()

    self.heal = elementary.Button(self.win)
    self.heal.label_set('Heal')
    self.heal.clicked = self.healPet
    self.buttons.pack_end(self.heal)
    self.heal.show()

    self.play = elementary.Button(self.win)
    self.play.label_set('Play')
    self.play.clicked = self.playWithPet
    self.buttons.pack_end(self.play)
    self.play.show()

    self.remove = elementary.Button(self.win)
    self.remove.label_set('Remove')
    self.remove.clicked = self.removePet
    box.pack_end(self.remove)

  def windowClose(self, *args, **kargs):
    self.parent.stop()
  def timer(self, interval, func):
    return ecore.timer_add(interval, func)
  def connect(self):
    self.parent.connect(mainloop = e_dbus.DBusEcoreMainLoop())
    print self.parent.serverVersion()
    self.selectPet()
  def removePet(self, *args, **kargs):
    self.parent.deletePet(self.petid)
    self.windowClose()
  def selectPet(self):
    dia = elementary.InnerWindow(self.win)
    new = elementary.Button(dia)
    new.label_set('New pet')
    new._callback_add('clicked', partial(self.newPet, dia))
    new.show()
    list = elementary.List(dia)
    list.size_hint_align_set(-1.0,-1.0)
    list.size_hint_weight_set(1.0, 1.0)
    petlist = self.parent.getPets()
    for pet in petlist:
      list.item_append(str(pet), None, None, partial(self.loadPet, pet, dia))
    list.go()
    list.show()
    box = elementary.Box(dia)
    box.pack_start(list)
    box.pack_end(new)
    box.show()
    dia.content_set(box)
    self.win.resize_object_add(dia)
    dia.show()
    dia.activate()
  def loadPet(self, pet, dia, *args, **kargs):
    self.pet = self.parent.pet(pet)
    self.petid = pet
    self.update(self.pet.GetState(), str(pet))
    dia.delete()
  def newPet(self, dia, *args, **kargs):
    self.petid = self.parent.addPet()
    self.pet = self.parent.pet(self.petid)
    dia.delete()
  def update(self, props, path):
    if path.replace('/org/shr/Geekogotchi/Pet/','') != str(self.petid):
      return False
    self.age.label_set('Age: '+str(props['Age'])+' years')
    if props['Alive'] and not props['Borned']:
      self.state.label_set('Not borned yet')
      self.age.hide()
      self.buttons.hide()
    elif props['Dead']:
      self.state.label_set('Dead ('+props['DeadReason']+')')
      self.age.show()
      self.happy.label_set('')
      self.health.label_set('')
      self.hungry.label_set('')
      self.buttons.hide()
      self.remove.show()
    else:
      self.state.label_set('')
      self.happy.label_set('Happiness: '+str(props['Happiness'])+'%')
      self.health.label_set('Health: '+str(props['Health'])+'%')
      self.hungry.label_set('Hungriness: '+str(props['Hungriness'])+'%')
      self.age.show()
      self.buttons.show()
  def feedPet(self, *args, **kargs):
    self.pet.Feed(0)
  def playWithPet(self, *args, **kargs):
    if self.pet.Play(0):
      self.pet.GoodPlay(0)
  def healPet(self, *args, **kargs):
    self.pet.Heal()
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
