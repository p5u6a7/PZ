from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.carousel import Carousel
from kivy.uix.image import Image

from kivy.lang import Builder

class ShowTime(BoxLayout):
	def build(self):
		carousel = ObjectProperty(None)
	def showScreenSettingsDisplay(self):
		self.clear_widgets()
		screen = ScreenSettingsDisplay()
		self.add_widget(screen)
	def showScreenSettingsAlerts(self):
		self.clear_widgets()
		screen = ScreenSettingsAlerts()
		self.add_widget(screen)
	def showScreenSettingsSocial(self):
		self.clear_widgets()
		screen = ScreenSettingsSocial()
		self.add_widget(screen)
	def showScreenSettingsSMS(self):
		self.clear_widgets()
		screen = ScreenSettingsSMS()
		self.add_widget(screen)
	def showScreenSettings(self):
		self.clear_widgets()
		showTime = ShowTime()
		self.add_widget(showTime)
    
class Screen1(Screen):
    pass

class Screen2(Screen):
    pass

class ScreenSettings(Screen):
	pass



class ScreenSettingsDisplay(Screen):
    pass
class ScreenSettingsAlerts(Screen):
    pass
class ScreenSettingsSocial(Screen):
    pass
class ScreenSettingsSMS(Screen):
    pass



class ScreenMusic(Screen):
    pass

class MyScreenManager(ScreenManager):
    pass

class MainApp(App):
    def build(self):
        Builder.load_file("ScreenSettings.kv")
        return ShowTime()
		
		
if __name__ == '__main__':
    MainApp().run()
