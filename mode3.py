# Discovering

from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.app import App

from kivy.clock import Clock
from kivy.animation import Animation

from kivy.uix.stencilview import StencilView
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button

from kivy.core.image import Image
from kivy.core.text import LabelBase
from kivy.graphics import *

from lib.utils import *
import lib.config, lib.kwargs

# Configuration

########################################################################
class Discovering(Widget):

  def __init__(self, **kwargs):

    lib.kwargs.set_kwargs(self, **kwargs)
          
    super(Discovering, self).__init__(**kwargs)

    self.all_zones_of_interest_viewedMessageSent = False

    # First item of self.shapes is the background
    self.bg_img = Image(lib.config.backgrounds[self.clientIdIndex])
    self.bg = AlphaWidget()
    with self.bg.canvas:
      Rectangle(texture=self.bg_img.texture, size=self.bg_img.size, pos=(0,0))
      
    self.add_widget(self.bg)
    
    # zones of interest
    self.shapes = []
    self.descriptions = []
    
    for zi in lib.config.zones_of_interest[self.clientIdIndex]:
      self.shapes.append( ZoneOfInterest(img=Image(zi[0]), pos=zi[1]) )
      self.descriptions.append( ZoneOfDescription(img=Image(zi[2]), pos=zi[3]) )

    Clock.schedule_interval(self.pulse, 0.1)
    
    for shape in self.shapes:            
      # add to the view
      self.add_widget(shape)


# basis
  def start(self):
    print "Discovering start() called"
    Clock.schedule_once(self.checkIfModeIsCompleted, 1)
    self.bg.alpha = 0.0
    self.bg.fadeIn()

    
  def stop(self):
    print "Discovering stop() called"    
    self.reset()
    Clock.unschedule(self.pulse)
    Clock.unschedule(self.checkIfModeIsCompleted)


  def fadein(self):
    pass


  def fadeout(self):
    pass    
    

  def reset(self, instance=False):
    self.all_zones_of_interest_viewedMessageSent = False    
    for shape in self.shapes:
      self.remove_widget(self.descFor(shape))
      shape.viewed = False
    
# Custom methods
  def checkIfModeIsCompleted(self, instance=False):
    # exits if not all shapes are viewed
    for shape in self.shapes:
      if not shape.viewed:
        return
    
    if not self.all_zones_of_interest_viewedMessageSent:
      print "All zones of interest seens"
      self.controller.sendMessage("all_zones_of_interest_viewed") # go to next mode
      self.all_zones_of_interest_viewedMessageSent = True
      
  def descFor(self, shape):
    return self.descriptions[self.shapes.index(shape)]

# Custom callbacks
  def pulse(self, dt):
    for shape in self.shapes:
      Clock.schedule_interval(shape.pulse_widget_alpha, 0.1)


# Kivy callbacks
  def on_touch_down(self, touch):
    pass

     
  def on_touch_move(self, touch):
    pass

    
  def on_touch_up(self, touch):
    # check if mode is complete before so I can read the text.
    # Next touch will throw a message to the server
    self.checkIfModeIsCompleted()

    for shape in self.shapes:
      # add interaction
      if shape.collide_point(*touch.pos):
        if self.children.count(self.descFor(shape)) < 1:
          # displays text box
          print self.descFor(shape)
          self.add_widget(self.descFor(shape))
          shape.viewed = True


########################################################################

      
if __name__ == '__main__':
  class DiscoveringApp(App):
  
    def build(self):
      base = Widget()
      
      discovering = Discovering()
      base.add_widget(discovering)
      discovering.start()
#      clearbtn = Button(text="clear", font_size=14)
#      clearbtn.bind(on_release=discovering.clear)
#      base.add_widget(clearbtn)
      
      return base

  DiscoveringApp().run()
