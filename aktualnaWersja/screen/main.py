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
from jnius import autoclass
from jnius import cast, PythonJavaClass, java_method
from kivy.utils import platform
from functools import partial
from os import listdir, path
from kivy.clock import Clock
from kivy.core.audio import SoundLoader, Sound
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup


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
class ChooseFile(FloatLayout):
    select = ObjectProperty(None)
    cancel = ObjectProperty(None)

class MusicPlayer(Screen):
    directory = ''  # lokacja folderu z piosenkami
    nowPlaying = ''  # Aktualnie wybrana piosenka
    songs = []  # Lista utworów
    flaga = 1

    #funkcja wywoływana na przycisku stop/play
    def stopSong(self):
        self.flaga = 88
        if self.nowPlaying == '':
            title = self.songs[0]
            self.nowPlaying = SoundLoader.load(self.directory + str(title))
            self.ids.nowplay.text = self.songs[0]
        if self.nowPlaying.state == 'stop':
            self.flaga = 5
            self.nowPlaying.play()
            if self.flaga == 5:
                self.flaga = 6
                if self.flaga == 6:
                    self.nowPlaying.bind(on_stop=self.stop_event_flaga)
        else:
            self.flaga = 99
            self.nowPlaying.stop()

    # funkcja wywoływana na przycisku Następny utwór
    def nextSong(self):
        self.flaga = 1
        if self.nowPlaying == '':
            title = self.songs[0]
            self.nowPlaying = SoundLoader.load(self.directory + str(title))
            self.ids.nowplay.text = self.songs[0]
            self.nowPlaying.play()
        else:
            self.nowPlaying.stop()
        print("nextkSong")
        if self.flaga == 1:
            self.nowPlaying.bind(on_stop=self.stop_event_flaga)

    # funkcja wywoływana na przycisku Poprzedni utwór
    def backSong(self):
        self.flaga = 0
        dl = len(self.songs) - 1
        if self.nowPlaying == '':
            title = self.songs[dl]
            self.nowPlaying = SoundLoader.load(self.directory + str(title))
            self.ids.nowplay.text = self.songs[dl]
            self.nowPlaying.play()
        else:
            self.nowPlaying.stop()
        print("backSong")
        if self.flaga == 0:
            self.nowPlaying.bind(on_stop=self.stop_event_flaga)

    #odczytanie ścieżki folderu z pliku
    def getpath(self):
        try:
            f = open("sav.dat", "r")
            self.ids.direct.text = str(f.readline())
            f.close()
            self.ids.searchBtn.text = "Wybierz folder"
            self.getSongs()
        except:
            self.ids.direct.text = ''

    #zapisanie ścieżki folderu do pliku
    def savepath(self, path):
        f = open("sav.dat", "w")
        f.write(path)
        f.close()

    def dismiss_popup(self):
        self._popup.dismiss()

    def fileSelect(self):
        content = ChooseFile(select=self.select,
                             cancel=self.dismiss_popup)

        self._popup = Popup(title="Wybierz folder", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def select(self, path):
        self.directory = path
        self.ids.direct.text = self.directory
        self.ids.searchBtn.text = "Wybierz folder"
        self.savepath(self.directory)
        self.songs = []
        self.getSongs()
        self.dismiss_popup()

    # proba wyczyszczenia listy utworow po dodaniu nowego folderu
    def onPressSongs(self):
        self.fileSelect()
        # music = MusicPlayer()
        # music.getpath()
        # return music
        # self.getSongs()

    #główna funkcja służąca do otwarzania muzyki i tworzenia listy utworów
    def getSongs(self):

        self.directory = self.ids.direct.text  # przypisanie katalogu z etykiety

        # Przeniesione do onPressSongs()
        # if self.directory == '':
        # self.fileSelect()

        # sprawdza czy ścieżka katalogu kończy się znakiem '/'
        if not self.directory.endswith('/'):
            self.directory += '/'

        # Sprawdza czy folder istnieje
        #if not path.exists(self.directory):
            #self.ids.status.text = 'Folder nie istnieje'
            #self.ids.status.color = (1, 0, 0, 1)

        #else:

            self.ids.status.text = ''

            self.ids.scroll.bind(minimum_height=self.ids.scroll.setter('height'))

            # get mp3 files from directory
            for fil in listdir(self.directory):
                if fil.endswith('.mp3'):
                    self.songs.append(fil)

            # Jeśli nie znaleziono plików mp3 w wybranym katalogu
            if self.songs == [] and self.directory != '':
                self.ids.status.text = 'Nie znaleziono muzyki!'
                self.ids.status.color = (1, 0, 0, 1)

            self.songs.sort()


        #funkcja uruchamiana w momencie kliknięcia utworu na liście
        def playSong(bt):
            self.flaga = 3
            try:
                self.nowPlaying.stop()
            except:
                pass
            finally:
                self.nowPlaying = SoundLoader.load(self.directory + bt.text + '.mp3')
                self.nowPlaying.play()
                self.ids.nowplay.text = bt.text + '.mp3'
                if self.flaga == 3:
                    self.flaga = 4
                    if self.flaga == 4:
                        self.nowPlaying.bind(on_stop=self.stop_event_flaga)

        #tworzenie listy utworów
        for song in self.songs:

            btn = Button(text=song[:-4], on_press=playSong)
            icon = Button(size_hint_x=None, size_hint_y=None, background_down="ico.png", background_normal="ico.png")

            # kolorowanie elementów listy
            if self.songs.index(song) % 2 == 0:
                btn.background_color = (.1, .1, .1, 1)
            else:
                btn.background_color = (.2, .2, .2, 1)

            #dodanie elementów etykiet utworów
            self.ids.scroll.add_widget(icon)
            self.ids.scroll.add_widget(btn)

    #funkcja wywoływana w momencie gdy obecnie odtwarzany utwór się skończy
    def stop_event_flaga(self, song):
        if self.flaga == 1:
            Clock.schedule_once(partial(self.nextSong2, self.nowPlaying))
        if self.flaga == 0:
            Clock.schedule_once(partial(self.backSong2, self.nowPlaying))
        if self.flaga == 4:
            Clock.schedule_once(partial(self.nextSong2, self.nowPlaying))
        if self.flaga == 6:
            Clock.schedule_once(partial(self.nextSong2, self.nowPlaying))

    #funkcja która odtwarza kolejny utwór z listy
    def nextSong2(self, songfile, dt):
        self.flaga = 1
        dl = len(self.songs)
        a = 0
        b = int(a)
        next2 = 0
        for song in self.songs:

            if self.songs[b] == self.ids.nowplay.text:
                next1 = b + 1
                next2 = int(next1)
                if next2 >= dl:
                    next2 = 0
                b = 0
            else:
                b += 1

        if self.nowPlaying.state == 'stop':
            pass
        else:
            self.nowPlaying.stop()
        title = self.songs[next2]
        self.nowPlaying = SoundLoader.load(self.directory + str(title))
        self.nowPlaying.play()
        self.ids.nowplay.text = self.songs[next2]
        print("nextSong2")
        if self.flaga == 1:
            self.nowPlaying.bind(on_stop=self.stop_event_flaga)

    # funkcja która odtwarza poprzedni utwór z listy
    def backSong2(self, songfile, dt):
        self.flaga = 1
        a = 0
        b = int(a)
        next2 = 0
        for song in self.songs:

            if self.songs[b] == self.ids.nowplay.text:
                next1 = b - 1
                next2 = int(next1)
                b = 0
            else:
                b += 1

        if self.nowPlaying.state == 'stop':
            pass
        else:
            self.nowPlaying.stop()
        title = self.songs[next2]
        self.nowPlaying = SoundLoader.load(self.directory + str(title))
        self.nowPlaying.play()
        self.ids.nowplay.text = self.songs[next2]
        print("backSong2")
        if self.flaga == 1:
            self.nowPlaying.bind(on_stop=self.stop_event_flaga)


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
    kontakty = []
    telefony = []
    kontakty2 = []
    telefony2 = []
    lista = {}

    def submit_contact(self):
        if platform() == 'android':
            activity = autoclass("org.renpy.android.PythonActivity").mActivity
            Phone = autoclass("android.provider.ContactsContract$CommonDataKinds$Phone")
            ContactsContract = autoclass("android.provider.ContactsContract$Contacts")

            ContentResolver = autoclass('android.content.Context')

            content_resolver = activity.getApplicationContext()

            resolver = content_resolver.getContentResolver()

            ApplicationContext = autoclass('android.app.Activity')
            # app = ApplicationContext.getApplicationContext()
            Toast = autoclass("android.widget.Toast")
            Cursor = autoclass("android.database.Cursor")
            phones = resolver.query(Phone.CONTENT_URI, None, None, None, None)
            pho = phones

            def sortowanie():
                c = 0
                for kontakt in self.kontakty:
                    self.lista[self.kontakty[c]] = self.telefony[c]
                    c = c + 1
                    sorted(self.lista)

            def callPhone(bt):
                Context = autoclass('android.content.Context')
                Uri = autoclass('android.net.Uri')
                Intent = autoclass('android.content.Intent')
                PythonActivity = autoclass('org.renpy.android.PythonActivity')
                b=0
                tel=''
                for kontakt in self.kontakty:
                        if bt.text == self.kontakty2[b]:
                            tel=self.telefony2[b]
                        b=b+1
                b = 0
                num = "tel:"
                num = num + tel
                #num = num + bt.text
                #num = num + "724324231"
                intent = Intent(Intent.ACTION_CALL)
                intent.setData(Uri.parse(num))
                currentActivity = cast('android.app.Activity', PythonActivity.mActivity)
                currentActivity.startActivity(intent)

            n = -1
            while (phones.moveToNext()):
                n = n + 1

                name = pho.getString(pho.getColumnIndex("display_name"))
                phoneNumber = pho.getString(pho.getColumnIndex(Phone.NUMBER))
                name2 = str(name)
                phoneNumber2 = str(phoneNumber)
                #btn = Button(id=phoneNumber2, text=name2, on_release=callPhone)
                #btn2 = Button(id=phoneNumber2, text=phoneNumber2, on_release=callPhone)

                self.ids.scroll.bind(minimum_height=self.ids.scroll.setter('height'))

                self.kontakty.append(name2)
                self.kontakty2.append(name2)
                self.telefony.append(phoneNumber2)

            sortowanie()
            self.kontakty2.sort()
            d = 0
            for kontakt in self.kontakty:
                self.telefony2.append(self.lista[self.kontakty2[d]])
                btn = Button(text=self.kontakty2[d], on_release=callPhone)
                d = d + 1
                self.ids.scroll.add_widget(btn)


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
    Builder.load_file("musicplayer.kv")
    znacznik = 0
    route_nodes = BooleanProperty(False)
    prev_time = datetime.datetime.now().time()

    def build(self):
        show_time = ShowTime()
        music = MusicPlayer()
        music.getpath()
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
