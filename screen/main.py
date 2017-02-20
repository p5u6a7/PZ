import datetime
from kivy.app import App
from kivy.clock import mainthread
from kivy.graphics import Color, Line
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from math import radians

import requests
from kivy.garden.mapview import MapLayer
from kivy.graphics.context_instructions import Translate, Scale
from kivy.graphics.transformation import Matrix
from kivy.properties import StringProperty, BooleanProperty
from plyer import call
from plyer import gps


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

    def showCallInterface(self):
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

        if "callScreen" in c.current_slide.name:
            slides = c.current_slide.carousel.slides
            c.current_slide.carousel.anim_move_duration = 0
            c.current_slide.carousel.load_slide(slides[1])
            c.current_slide.carousel.anim_move_duration = 0.5


class GroupScreen(Screen):
    auto_center = BooleanProperty(True)

    def rotate(self):
        scatter = self.ids["scatter2"]
        r = Matrix().rotate(-radians(30), 0, 0, 1)
        scatter.apply_transform(r, post_multiply=True,
                                anchor=scatter.to_local(scatter.parent.center_x, scatter.parent.center_y))

    def center(self):
        MainApp.get_running_app().root.carousel.slides[0].ids["mapView"].center_on(float(MainApp.lat), (MainApp.lon))
        self.auto_center = True
        self.redraw_route()

    def calculate_route_nodes(self, lat1, lon1, lat2, lon2):
        MainApp.cos = -1

        '''potrzebne do testowania na komputerze'''
        MainApp.on_location(MainApp.get_running_app())

        for layer in MainApp.get_running_app().root.carousel.slides[0].ids["mapView"]._layers:
            if layer.id == 'line_map_layer':
                layer.routeToGpx(lat1, lon1, lat2, lon2)
                break

    def redraw_route(self):
        for layer in self.ids["mapView"]._layers:
            if layer.id == 'line_map_layer':
                layer.draw_line()
                break


class CallScreen(Screen):
    def build(self):
        pass


class ScreenSettings(Screen):
    def build(self):
        pass


class ScreenSettingsDisplay(Widget):
    pass


class ScreenSettingsAlerts(Widget):
    pass


class ScreenSettingsSocial(Widget):
    pass


class ScreenSettingsSMS(Widget):
    pass


class ScreenMusic(Widget):
    pass


class ScreenContacts(Widget):
    pass


'''poczatek'''


class CallInterface(BoxLayout):
    pass


class DialCallButton(Button):
    def dial(self, *args):
        call.dialcall()


class MakeCallButton(Button):
    tel = StringProperty()

    def call(self, *args):
        call.makecall(tel=self.tel)


'''koniec'''


class LineMapLayer(MapLayer):
    id = 'line_map_layer'

    def __init__(self, **kwargs):
        super(LineMapLayer, self).__init__(**kwargs)
        self.zoom = 0

    '''Funkcja odpowiadajaca za stworzenie wierzcholkow grafu, ktory jest nasza droga'''

    def parseJSON(self, points):
        response = self.downloadJSON(points)
        i = response.text.find('"coordinates":')
        s = ""
        close_bracket_count = 0
        for index in xrange(i + 15, len(response.text)):
            # s.__add__(response.text[index])

            if response.text[index] == "]":
                if close_bracket_count == 1:
                    break
                close_bracket_count += 1
            else:
                close_bracket_count = 0
            s += response.text[index]
        s = s.encode('utf-8')
        slist = s.split('],[')
        slist[0] = slist[0].replace('[', '')
        slist[len(slist) - 1] = slist[len(slist) - 1].replace(']', '')
        i = 0
        a = []
        for item in slist:
            a.append(item.split(','))
            i += 1

        self.count = 0
        self.parent.node = []
        for item in a:
            self.parent.node.append(item)
            self.count += + 1

    def downloadJSON(self, points):
        my_url = 'https://api.mapbox.com/directions/v5/mapbox/cycling/' + points + '?access_token=pk.eyJ1Ijoid2lsY3plazUwMyIsImEiOiJjaXowNnAyMjcwMDE4MzNsd2xvbTd5ZnY0In0.WiuRsomVkCrkN1j78JJ7Aw&overview=full&geometries=geojson'
        response = requests.get(my_url)
        return response

    def routeToGpx(self, lat1, lon1, lat2, lon2):
        points = str(MainApp.lon) + ',' + str(MainApp.lat) + ';' + str(lon2) + ',' + str(lat2)
        self.parseJSON(points)

        '''Wersja offline'''

        '''data = LoadOsm('cycle')
        data = LoadOsm('car')
        node1 = data.findNode(lat1, lon1)
        node2 = data.findNode(lat2, lon2)

        router = Router(data)
        result, route = router.doRoute(node1, node2)
        self.count = 0
        self.parent.node = []

        for i in route:
            self.parent.node.append(data.rnodes[i])
            self.count = self.count + 1'''
        MainApp.route_nodes = True

    '''W momencie przemieszczenia mapy przerysowujemy linie'''

    def reposition(self):
        mapview = self.parent
        if (self.zoom != mapview.zoom and MainApp.route_nodes == True):
            self.draw_line()

    '''Funkcja rysowania linii'''

    def draw_line(self):
        mapview = self.parent
        self.zoom = mapview.zoom

        '''Na ten moment ustawiamy stale wspolrzedne'''
        geo_dom = [52.9828, 18.5729]
        geo_wydzial = [53.0102, 18.5946]

        point_list = []
        '''Wywolujemy funkcje ktora zwraca nam wspolrzedne trasy o danych wspolzednych poczatkowych i koncowych (Gdzie to przeniesc???)'''
        # self.routeToGpx(float(geo_dom[0]), float(geo_dom[1]), float(geo_wydzial[0]), float(geo_wydzial[1]))

        for j in xrange(len(self.parent.node) - 1):
            point_list.extend(
                mapview.get_window_xy_from(float(self.parent.node[j][1]), float(self.parent.node[j][0]), mapview.zoom))

        scatter = mapview._scatter
        x, y, s = scatter.x, scatter.y, scatter.scale

        with self.canvas:
            self.canvas.clear()
            Scale(1 / s, 1 / s, 1)
            Translate(-x, -y)
            Color(0, 0, 255, .6)
            Line(points=point_list, width=3, joint="bevel")


class MainApp(App):
    gps_location = StringProperty()
    gps_status = StringProperty('Click Start to get GPS location updates')
    lat = 53.0102
    lon = 18.5946
    Builder.load_file("screensettings.kv")
    Builder.load_file("groupscreen.kv")
    Builder.load_file("callscreen.kv")
    znacznik = 0
    route_nodes = BooleanProperty(False)
    prev_time = datetime.datetime.now().time()

    def build(self):
        show_time = ShowTime()
        try:
            gps.configure(on_location=self.on_location, on_status=self.on_status)
            self.start(1000, 0)
        except NotImplementedError:
            self.gps_status = 'GPS is not implemented for your platform'
        return show_time

    def start(self, minTime, minDistance):
        gps.start(minTime, minDistance)

    def stop(self):
        gps.stop()

    @mainthread
    def on_location(self, **kwargs):
        duration = (
            datetime.datetime.combine(datetime.date.today(),
                                      datetime.datetime.now().time()) - datetime.datetime.combine(
                datetime.date.today(), MainApp.prev_time)).total_seconds()
        if duration >= 1:
            self.gps_location = '\n'.join([
                                              '{}={}'.format(k, v) for k, v in kwargs.items()])
            for k, v in kwargs.items():
                if k == "lat":
                    MainApp.lat = float(v)
                else:
                    if k == "lon":
                        MainApp.lon = float(v)
            '''W karuzeli dodajemy layer wraz z nasza utworzona klasa LineMapLayer'''
            print "---------------------"
            label = MainApp.get_running_app().root.carousel.slides[0].ids["label1"]
            label.text = str(int(label.text) + 1)

            '''Nie jestem pewien czy usuniecie tego nie bedzie powodowalo problemow'''
            '''if MainApp.znacznik > 0:
                for layer in MainApp.get_running_app().root.carousel.slides[0].ids["mapView"]._layers:
                    if layer.id == 'line_map_layer':
                        MainApp.get_running_app().root.carousel.slides[0].ids["mapView"]._layers.remove(layer)
                        break
            #MainApp.znacznik = 1'''

            mapview = MainApp.get_running_app().root.carousel.slides[0].ids["mapView"]
            if MainApp.znacznik == 0:
                mapview.add_layer(LineMapLayer(), mode="scatter")
                MainApp.znacznik = 1

            MainApp.get_running_app().root.carousel.slides[0].ids["marker"].lat = float(MainApp.lat)
            MainApp.get_running_app().root.carousel.slides[0].ids["marker"].lon = float(MainApp.lon)
            MainApp.get_running_app().root.carousel.slides[0].ids["marker2"].lat = 53.0102
            MainApp.get_running_app().root.carousel.slides[0].ids["marker2"].lon = 18.5946

            if MainApp.get_running_app().root.carousel.slides[0].auto_center:
                mapview.center_on(float(MainApp.lat), (MainApp.lon))
                MainApp.get_running_app().root.carousel.slides[0].redraw_route()
            MainApp.cos = 0
            MainApp.prev_time = datetime.datetime.now().time()

    @mainthread
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
