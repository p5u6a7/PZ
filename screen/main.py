from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from plyer import *
from kivy.properties import StringProperty
from kivy.clock import Clock, mainthread
from kivy.uix.boxlayout import BoxLayout
from kivy.garden.mapview import MapView, MapMarker, MapLayer
from kivy.properties import ObjectProperty
from kivy.uix.carousel import Carousel
from kivy.uix.image import Image
from kivy.properties import ListProperty
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Line
from kivy.graphics.context_instructions import Translate, Scale
from kivy.lang import Builder
from route import Router
from loadOsm import LoadOsm






class ShowTime(Screen):
    def build(self):
        pass
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

    def goToScreen(self):
        c = self.carousel

        if "screenSettings" in c.current_slide.name:
            slides = c.current_slide.carousel.slides
            c.current_slide.carousel.anim_move_duration = 0
            c.current_slide.carousel.load_slide(slides[1])
            c.current_slide.carousel.anim_move_duration = 0.5


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
'''Tworzymy cala klase LineMapLayer, ktora bedzie nam sluzyc do wyznaczania trasy. Na chwile obecna jest to linia ze stalymi wspolrzednymi'''
class LineMapLayer(MapLayer):
    def __init__(self, **kwargs):
        super(LineMapLayer, self).__init__(**kwargs)
        self.zoom = 0

    '''Funkcja odpowiadajaca za stworzenie wierzcholkow grafu, ktory jest nasza droga'''
    def routeToGpx(self, lat1, lon1, lat2, lon2):
        data = LoadOsm('cycle')
        node1 = data.findNode(lat1, lon1)
        node2 = data.findNode(lat2, lon2)

        router = Router(data)
        result, route = router.doRoute(node1, node2)
        self.count = 0
        self.node=[]

        for i in route:
            self.node.append(data.rnodes[i])
            self.count=self.count+1


    '''W momencie przemieszczenia mapy przerysowujemy linie'''
    def reposition(self):
        mapview = self.parent
        if (self.zoom != mapview.zoom):
            self.draw_line()

    '''Funkcja rysowania linii'''
    def draw_line(self):
        mapview = self.parent
        self.zoom = mapview.zoom

        '''Na ten moment ustawiamy stale wspolrzedne'''
        geo_dom   = [52.9828, 18.5729]
        geo_wydzial = [53.0102, 18.5946]

        point_list=[]
        '''Wywolujemy funkcje ktora zwraca nam wspolrzedne trasy o danych wspolzednych poczatkowych i koncowych (Gdzie to przeniesc???)'''
        self.routeToGpx(float(geo_dom[0]), float(geo_dom[1]), float(geo_wydzial[0]), float(geo_wydzial[1]))

        for j in xrange(len(self.node)-1):
            point_list.extend(mapview.get_window_xy_from(float(self.node[j][0]), float(self.node[j][1]), mapview.zoom))

        scatter = mapview._scatter
        x,y,s = scatter.x, scatter.y, scatter.scale

        with self.canvas:
            self.canvas.clear()
            Scale(1/s,1/s,1)
            Translate(-x, -y)
            Color(0, 0, 255, .6)
            Line(points=point_list, width=3, joint="bevel")


class MainApp(App):
    gps_location = StringProperty()
    gps_status = StringProperty('Click Start to get GPS location updates')
    lat = 0
    lon = 0
    Builder.load_file("screensettings.kv")
    Builder.load_file("groupscreen.kv")
    znacznik=0

    def build(self):
        try:
            gps.configure(on_location=self.on_location, on_status=self.on_status)
            self.start(1000, 0)
        except NotImplementedError:
            self.gps_status = 'GPS is not implemented for your platform'
        return ShowTime()

    def start(self, minTime, minDistance):
        gps.start(minTime, minDistance)

    def stop(self):
        gps.stop()

    '''@mainthread'''
    def on_location(self, **kwargs):
        self.gps_location = '\n'.join([
            '{}={}'.format(k, v) for k, v in kwargs.items()])
        for k, v in kwargs.items():
            if k == "lat":
                MainApp.lat = float(v)
            else:
                if k == "lon":
                    MainApp.lon = float(v)

        '''W karuzeli dodajemy layer wraz z nasza utworzona klasa LineMapLayer'''
        if MainApp.znacznik>0:
            MainApp.get_running_app().root.carousel.slides[0].ids["mapView"].remove_layer(LineMapLayer())
        MainApp.znacznik=1
        MainApp.get_running_app().root.carousel.slides[0].ids["mapView"].add_layer(LineMapLayer(), mode="scatter")
        MainApp.get_running_app().root.carousel.slides[0].ids["marker"].lat = float(MainApp.lat)
        MainApp.get_running_app().root.carousel.slides[0].ids["marker"].lon = float(MainApp.lon)
        MainApp.get_running_app().root.carousel.slides[0].ids["marker2"].lat = 53.0102
        MainApp.get_running_app().root.carousel.slides[0].ids["marker2"].lon = 18.5946
        MainApp.get_running_app().root.carousel.slides[0].ids["mapView"].center_on(float(MainApp.lat), (MainApp.lon))


    '''@mainthread'''
    def on_status(self, stype, status):
        self.gps_status = 'type={}\n{}'.format(stype, status)

    def on_pause(self):
        gps.stop()
        return True

    def on_resume(self):
        gps.start(1000, 0)


pass


if __name__ == '__main__':
    MainApp().run()
