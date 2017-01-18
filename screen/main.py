from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.garden.mapview import MapView
from kivy.properties import ObjectProperty
from kivy.uix.carousel import Carousel
from kivy.uix.image import Image
from kivy.properties import ListProperty

from kivy.lang import Builder


class ShowTime(Screen):
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
        show_time = ShowTime()
        self.add_widget(show_time)
        c = self.carousel
        slides = c.slides
        c.anim_move_duration = 0
        c.load_slide(slides[1])
        c.anim_move_duration = 0.5

    def goToScreen(self):
        c = self.carousel

        if "screenSettings" in c.current_slide.name:
            slides = c.current_slide.carousel.slides
            c.current_slide.carousel.anim_move_duration = 0
            c.current_slide.carousel.load_slide(slides[1])
            c.current_slide.carousel.anim_move_duration = 0.5
        else:
            if "screenGroup" in c.current_slide.name:
                print(c)



class GroupScreen(Screen):
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


class ScreenContacts(Screen):
    pass


class MyScreenManager(ScreenManager):
    pass


class MainApp(App):
    def build(self):
        Builder.load_file("ScreenSettings.kv")
        Builder.load_file("GroupScreen.kv")
        return ShowTime()


if __name__ == '__main__':
    MainApp().run()
