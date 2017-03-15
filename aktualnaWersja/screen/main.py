# -*- coding: utf-8 -*-

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
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
import time
import threading
from Contact import Contact
from Group import Group
import geocoder
from plyer import sms
import sqlite3
import sys

from math import sqrt
from math import atan

from plyer import compass
from kivy.animation import Animation
from kivy.graphics.transformation import Matrix
from kivy.properties import NumericProperty
from kivy.graphics.context_instructions import Translate, Scale

#modyfikacja 1

#SmsManager = autoclass('android.telephony.SmsManager')




AcceptIncomingCall = autoclass("org.test.Phone")

TelephonyManager = autoclass('android.telephony.TelephonyManager')
Context = autoclass('android.content.Context')
activity = autoclass("org.renpy.android.PythonActivity").mActivity
Grupy = autoclass("android.provider.ContactsContract$Groups")

print "asdfg12"

AcceptIncomingCall2 = activity

contacts = []
contacts2 = []
contactsGroups = {}
contactsGroups2 = {}
groups = []
sensorEnabled = False
wsp2 = 0

'''Popup odbieranie telefonu'''
Builder.load_string('''
<ConfirmPopup>:
    cols:1
    Label:
        text: root.text
    GridLayout:
        cols: 2
        size_hint_y: None
        height: '44sp'
        Button:
            text: 'Odbierz'
            on_release: root.dispatch('on_answer','Odbierz')
        Button:
            text: 'Odrzuć'
            on_release: root.dispatch('on_answer', 'Odrzuc')
''')


#
# class AndroidSms(Sms):
#
#     def _send(self, **kwargs):
#         sms = SmsManager.getDefault()
#
#         recipient = kwargs.get('665544954')
#         message = kwargs.get('test smsa xD Syntezator przeczytał?')
#
#         if sms:
#             sms.sendTextMessage(recipient, None, message, None, None)





class ConfirmPopup(GridLayout):
    text = StringProperty()

    def __init__(self, **kwargs):
        self.register_event_type('on_answer')
        super(ConfirmPopup, self).__init__(**kwargs)

    def on_answer(self, *args):
        pass


class ShowTime(Screen):
    popup_shown = False
    flagaCall = 1

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



    def callListener(self):

        self.popup_shown = False
        print activity.number
        if activity.isIncoming and self.popup_shown == False:
            self.popup_shown = True
            content = ConfirmPopup()
            content.bind(on_answer=self._on_answer)
            self.popup = Popup(title="Dzwoni: " + activity.number,
                               content=content,
                               size_hint=(None, None),
                               size=(480, 400),
                               auto_dismiss=False)
            self.popup.open()
        else:
            self.popup_shown = False
            # time.sleep(1)

    def check(self):

        '''content = ConfirmPopup(text='Dzwoni ')
        content.bind(on_answer=self._on_answer)
        self.popup = Popup(title='Dzwoni ',
                           content=content,
                           size_hint=(None, None),
                           size=(480, 400),
                           auto_dismiss=False)
        self.popup.open()'''
        print"nieWiem"
        #self.send_sms()
        self.callListener()
        # self.send_sms()
        # sms2 = AndroidSms()
        # sms2.send('663889095', 'wiadomosc sms')

    def _on_answer(self, instance, answer):
        print "USER ANSWER: ", repr(answer)
        if answer == "Odbierz":
            self.popup_shown = False
            self.flagaCall = 1
            self.popup.dismiss()
            AcceptIncomingCall2.acceptCall()
        else:
            if answer == "Odrzuc":
                self.popup_shown = False
                self.flagaCall = 1
                self.popup.dismiss()
                self.rejectIncomingCall()
        self.popup.dismiss()

    def rejectIncomingCall(self):

        telephonyManager = activity.getSystemService(Context.TELEPHONY_SERVICE)

        telephonyService = activity.dupa(telephonyManager)
        telephonyService.endCall()

    def check2(self, fla):
        # pass
        print "tralalalalala"
        if activity.isIncoming:
            if self.flagaCall == 1:
                self.flagaCall = 2
                print "wszystkie_nr_tel"
                for contact in contacts:
                    print contact.number
                print "wypisz_dane"
                #numTel = str(activity.number)
                num = str(activity.number)
                num = num.replace(" ", "")
                num = num.replace("-", "")
                if num[0] == "+":
                    num = num[-9:]

                numTel = num
                try:
                    nrGrupy = contactsGroups2[contactsGroups[numTel]]
                except:
                    nrGrupy = 99
                    # wykona ise jesli dzwoni obcy nr
                    self.rejectIncomingCall()  # domyślnie ustawione na odrzucenie

                conn = sqlite3.connect('baza.db')
                c = conn.cursor()

                c.execute("SELECT ID_GRUPY FROM Grupy WHERE REAKCJA = 'autoodebranie'")
                dane = c.fetchall()

                c.execute("SELECT ID_GRUPY FROM Grupy WHERE REAKCJA = 'odrzucenieSMS'")
                dane1 = c.fetchall()

                conn.commit()
                conn.close()

                zmienna = BooleanProperty(True)
                zmienna1 = BooleanProperty(True)

                print "dane z bazy: "
                print dane

                for x in dane:
                    if int(nrGrupy) == int(x[0]):
                        #self.callListener()
                        #AcceptIncomingCall2.acceptCall()
                        print 'autoodebranie'
                        zmienna = False
                        print zmienna
                        self.flagaCall = 1
                        break

                if zmienna:
                    for x in dane1:
                        if int(nrGrupy) == int(x[0]):
                            # tutaj miejsce na wywolanie metody odrzucajacej polaczenie z wyslaniem powiadomienia SMS
                            self.rejectIncomingCall()
                            #self.send_sms()
                            print 'odrzucenieSMS'
                            zmienna1 = False
                            print zmienna1
                            self.flagaCall = 1
                            break

                if bool(zmienna) == bool(zmienna1):
                    self.rejectIncomingCall()
                    print 'odrzucenie'
                    self.flagaCall = 1

                    # przypisywanie akci do grup
                    # if int(nrGrupy) == 1:
                    #     AcceptIncomingCall2.acceptCall()
                    # elif int(nrGrupy) == 2:
                    #     self.rejectIncomingCall()
                    # elif int(nrGrupy) == 3:
                    #     AcceptIncomingCall2.acceptCall()
                    # elif int(nrGrupy) == 4:
                    #     AcceptIncomingCall2.acceptCall()
                    # elif int(nrGrupy) == 5:
                    #     self.rejectIncomingCall()
                    # elif int(nrGrupy) == 6:
                    #     self.rejectIncomingCall()
                    # elif int(nrGrupy) == 7:
                    #     self.callListener()
                    #     #self.rejectIncomingCall()
                    #     #self.send_sms()
                    # elif int(nrGrupy) == 99:
                    #     self.callListener()
                    # else:
                    #     self.callListener()
                    # self.callListener()
                    # self.rejectIncomingCall()

                    # Clock.schedule_interval(check2, 1)


class ChooseFile(FloatLayout):
    select = ObjectProperty(None)
    cancel = ObjectProperty(None)


class ChooseNumber(FloatLayout):
    select = ObjectProperty(None)
    cancel = ObjectProperty(None)

    def addNumber1(self):
        self.ids.nrTelefonu.text += self.ids.btn1.text

    def addNumber1(self):
        self.ids.nrTelefonu.text += self.ids.btn1.text

    def addNumber2(self):
        self.ids.nrTelefonu.text += self.ids.btn2.text

    def addNumber3(self):
        self.ids.nrTelefonu.text += self.ids.btn3.text

    def addNumber4(self):
        self.ids.nrTelefonu.text += self.ids.btn4.text

    def addNumber5(self):
        self.ids.nrTelefonu.text += self.ids.btn5.text

    def addNumber6(self):
        self.ids.nrTelefonu.text += self.ids.btn6.text

    def addNumber7(self):
        self.ids.nrTelefonu.text += self.ids.btn7.text

    def addNumber8(self):
        self.ids.nrTelefonu.text += self.ids.btn8.text

    def addNumber9(self):
        self.ids.nrTelefonu.text += self.ids.btn9.text

    def addNumber11(self):
        self.ids.nrTelefonu.text += self.ids.btn11.text

    def addNumber12(self):
        self.ids.nrTelefonu.text += self.ids.btn12.text

    def addNumber0(self):
        self.ids.nrTelefonu.text += self.ids.btn0.text

    def delNumber(self):
        self.ids.nrTelefonu.text = self.ids.nrTelefonu.text[:-1]

    def callPhonePopup(bt):
        Uri = autoclass('android.net.Uri')
        Intent = autoclass('android.content.Intent')
        PythonActivity = autoclass('org.renpy.android.PythonActivity')

        num = "tel:"
        num = num + bt.ids.nrTelefonu.text
        intent = Intent(Intent.ACTION_CALL)
        intent.setData(Uri.parse(num))
        currentActivity = cast('android.app.Activity', PythonActivity.mActivity)
        currentActivity.startActivity(intent)


class MusicPlayer(Screen):
    directory = ''  # lokacja folderu z piosenkami
    nowPlaying = ''  # Aktualnie wybrana piosenka
    songs = []  # Lista utworów
    flaga = 1

    # funkcja wywoływana na przycisku stop/play
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

    # odczytanie ścieżki folderu z pliku
    def getpath(self):
        try:
            f = open("sav.dat", "r")
            self.ids.direct.text = str(f.readline())
            f.close()
            self.ids.searchBtn.text = "Wybierz folder"
            self.getSongs()
        except:
            self.ids.direct.text = ''

    # zapisanie ścieżki folderu do pliku
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

    # główna funkcja służąca do otwarzania muzyki i tworzenia listy utworów
    def getSongs(self):

        self.directory = self.ids.direct.text  # przypisanie katalogu z etykiety

        # Przeniesione do onPressSongs()
        # if self.directory == '':
        # self.fileSelect()

        # sprawdza czy ścieżka katalogu kończy się znakiem '/'
        if not self.directory.endswith('/'):
            self.directory += '/'

            # Sprawdza czy folder istnieje
            # if not path.exists(self.directory):
            # self.ids.status.text = 'Folder nie istnieje'
            # self.ids.status.color = (1, 0, 0, 1)

            # else:

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

        # funkcja uruchamiana w momencie kliknięcia utworu na liście
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

        # tworzenie listy utworów
        for song in self.songs:

            btn = Button(text=song[:-4], on_press=playSong)
            icon = Button(size_hint_x=None, size_hint_y=None, background_down="ico.png", background_normal="ico.png")

            # kolorowanie elementów listy
            if self.songs.index(song) % 2 == 0:
                btn.background_color = (.1, .1, .1, 1)
            else:
                btn.background_color = (.2, .2, .2, 1)

            # dodanie elementów etykiet utworów
            self.ids.scroll.add_widget(icon)
            self.ids.scroll.add_widget(btn)

    # funkcja wywoływana w momencie gdy obecnie odtwarzany utwór się skończy
    def stop_event_flaga(self, song):
        if self.flaga == 1:
            Clock.schedule_once(partial(self.nextSong2, self.nowPlaying))
        if self.flaga == 0:
            Clock.schedule_once(partial(self.backSong2, self.nowPlaying))
        if self.flaga == 4:
            Clock.schedule_once(partial(self.nextSong2, self.nowPlaying))
        if self.flaga == 6:
            Clock.schedule_once(partial(self.nextSong2, self.nowPlaying))

    # funkcja która odtwarza kolejny utwór z listy
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
    auto_center = BooleanProperty(False)
    lonGPS = ''
    latGPS = ''
    flagaGPS = 0




    # sms_recipient = "663889095"
    # sms_message = 'test działania smsów'
    #
    # def send_sms(self, *args):
    #     print "smsik_error"
    #     sms.send(recipient=self.sms_recipient, message=self.sms_message)



    # modyfikacja 2

    def do_toggle(self):
        self.sensorEnabled = False
        try:
            if not self.sensorEnabled:
                compass.enable()
                #Clock.schedule_interval(self.get_readings, 1)

                self.sensorEnabled = True
                #self.ids.toggle_button.text = "Stop compass"
            else:
                compass.disable()
                #Clock.unschedule(self.get_readings)

                self.sensorEnabled = False
                #self.ids.toggle_button.text = "Start compass"
        except NotImplementedError:
            import traceback
            traceback.print_exc()
            status = "Compass is not implemented for your platform"
            #self.ids.status.text = status

    def obliczanie_y1(self, x, y, z):
        if y == 0:
            y = 0.01
        y1 = sqrt(1 / (1 + (x * x) / (y * y)))
        if y < 0:
            y1 = -y1
        return y1

    def obliczanie_x1(self, x, y1):
        x1 = sqrt(1 - y1 * y1)
        if x < 0:
            x1 = -x1
        return x1

    def obliczanie_alpha(self, x1, y1):
        if x1 == 0:
            x1 = 0.01
        if x1 < 0:
            alpha = atan(y1 / x1) + 3.14 + 1.57
        else:
            alpha = atan(y1 / x1) + 1.57
        return alpha
    # rotacja_mapy
    def get_readings(self, dt):
        print "test_rotacjajajajajajajajaja"
        val = compass.orientation
        x = round(int(val[0]), 2)
        y = round(int(val[1]), 2)
        z = round(int(val[2]), 2)

        y1 = round(self.obliczanie_y1(x, y, z), 2)
        x1 = round(self.obliczanie_x1(x, y1), 2)
        alpha = round(self.obliczanie_alpha(x1, y1), 2)
        wsp = (alpha * 360 / 6.28 + 180) % 360
        print wsp
        if wsp < 60 and wsp >= 0:
            wsp = 30
        if wsp < 120 and wsp >= 60:
            wsp = 90
        if wsp < 180 and wsp >= 120:
            wsp = 150
        if wsp < 240 and wsp >= 180:
            wsp = 210
        if wsp < 300 and wsp >= 240:
            wsp = 270
        if wsp <= 360 and wsp >= 300:
            wsp = 330
        if wsp >= 360:
            wsp = 360
        if wsp <= 0:
            wsp = 360
        print wsp
        wsp2 = int(wsp)
        print wsp2
        print self.ids["scatter2"]
        scatter = self.ids["scatter2"]
        r = Matrix().rotate(-radians(wsp2), 0, 0, 1)
        scatter.apply_transform(r, post_multiply=True,
                                anchor=scatter.to_local(scatter.parent.center_x, scatter.parent.center_y))

    # rotacja_mapy

    def Search(self):
        test = self.ids.SearchInput.text
        g = geocoder.google(self.ids.SearchInput.text + ', PL')
        if test == '':
            pass
        else:
            lonGPS2 = g.lng
            latGPS2 = g.lat
            self.lonGPS = str(lonGPS2)
            self.latGPS = str(latGPS2)
            self.flagaGPS = 1

    def returnLon(self):
        self.Search()
        return self.lonGPS

    def returnLat(self):
        self.Search()
        return self.latGPS

    def returnFlag(self):
        self.Search()
        return self.flagaGPS

    def rotate2(self):
        scatter = self.ids["scatter2"]
        r = Matrix().rotate(-radians(wsp2), 0, 0, 1)
        scatter.apply_transform(r, post_multiply=True,
                                anchor=scatter.to_local(scatter.parent.center_x, scatter.parent.center_y))


    def rotate(self):
        scatter = self.ids["scatter2"]
        r = Matrix().rotate(-radians(30), 0, 0, 1)
        scatter.apply_transform(r, post_multiply=True,
                                anchor=scatter.to_local(scatter.parent.center_x, scatter.parent.center_y))

    def center(self):
        MainApp.get_running_app().root.carousel.slides[0].ids["mapView"].center_on(float(MainApp.lat), (MainApp.lon))
        self.auto_center = True
        self.redraw_route()

    def centerTarget(self):
        lon = float(self.returnLon())
        lat = float(self.returnLat())
        MainApp.get_running_app().root.carousel.slides[0].ids["mapView"].center_on(lat, lon)
        # self.auto_center = True
        self.redraw_route()

    def centerMy(self):
        lon = float(MainApp.lon)
        lat = float(MainApp.lat)
        MainApp.get_running_app().root.carousel.slides[0].ids["mapView"].center_on(lat, lon)
        # self.auto_center = True
        self.redraw_route()

    def calculate_route_nodes_run(self):
        self.calculate_route_nodes(self.latGPS, self.lonGPS, self.latGPS, self.lonGPS)

    def calculate_route_nodes(self, lat1, lon1, lat2, lon2):
        MainApp.cos = -1
        self.center()

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

    def dismiss_popup(self):
        self._popup.dismiss()

    def numberSelect(self):
        content = ChooseNumber(select=self.select,
                               cancel=self.dismiss_popup)

        self._popup = Popup(title="Wybierz numer", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def select(self, path):
        # self.directory = path
        # self.ids.direct.text = self.directory
        # self.ids.searchBtn.text = "Wybierz folder"
        # self.savepath(self.directory)
        # self.songs = []
        # self.getSongs()
        self.dismiss_popup()

    # def addNum(self):
    #     def addNumber(bt):
    #         self.ids.nrTelefonu.text = bt.text

    def read_groups(self):
        content_resolver = activity.getApplicationContext()
        resolver = content_resolver.getContentResolver()

        grupa = resolver.query(Grupy.CONTENT_URI, None, None, None, None)
        group = grupa

        while (grupa.moveToNext()):

            id = group.getString(group.getColumnIndex("_id"))
            name = group.getString(group.getColumnIndex("TITLE"))
            if id not in groups:
                groups.append(Group(id, name))
        grupa.close()
        print "grupy_wyswietl"
        for i in groups:
            print i.id + " " + i.name

    def submit_contact(self):
        if platform() == 'android':
            Phone = autoclass("android.provider.ContactsContract$CommonDataKinds$Phone")
            ContactsContract = autoclass("android.provider.ContactsContract$Contacts")
            GroupMembership = autoclass("android.provider.ContactsContract$CommonDataKinds$GroupMembership")

            ContentResolver = autoclass('android.content.Context')

            content_resolver = activity.getApplicationContext()

            resolver = content_resolver.getContentResolver()

            ApplicationContext = autoclass('android.app.Activity')
            # app = ApplicationContext.getApplicationContext()
            Toast = autoclass("android.widget.Toast")
            Cursor = autoclass("android.database.Cursor")
            Data = autoclass("android.provider.ContactsContract$Data")
            phones = resolver.query(Phone.CONTENT_URI, None, None, None, None)
            # phones = resolver.query(Data.CONTENT_URI, None, None, None, None)
            pho = phones

            def callPhone(bt):
                Context = autoclass('android.content.Context')
                Uri = autoclass('android.net.Uri')
                Intent = autoclass('android.content.Intent')
                PythonActivity = autoclass('org.renpy.android.PythonActivity')
                tel = ''
                for contact in contacts:
                    if bt.text == contact.display_name:
                        tel = contact.number
                num = "tel:"
                num = num + tel
                print "to jest "
                print num
                intent = Intent(Intent.ACTION_CALL)
                intent.setData(Uri.parse(num))
                currentActivity = cast('android.app.Activity', PythonActivity.mActivity)
                currentActivity.startActivity(intent)

            self.read_groups()

            RawContactsColumns = autoclass("android.provider.ContactsContract$RawContactsColumns")
            projection = [GroupMembership.GROUP_ROW_ID, RawContactsColumns.CONTACT_ID]
            # projection = [GroupMembership.GROUP_ROW_ID, "contact_id"]
            Cursor = autoclass("android.database.Cursor")
            # c = resolver.query(Data.CONTENT_URI, projection, GroupMembership.GROUP_ROW_ID+"="+groups,None, None)
            a = 1
            print "cosik4"
            # while (phones.moveToNext()):
            #     name = pho.getString(pho.getColumnIndex("display_name"))
            #     phoneNumber = pho.getString(pho.getColumnIndex(Phone.NUMBER))
            #     contact_group_id = pho.getString(pho.getColumnIndex(GroupMembership.GROUP_ROW_ID))
            #     contact_group_name = -1
            #     for group in groups:
            #         if contact_group_id == group.id:
            #             contact_group_name = group.name
            #     if name == "Daniel":
            #         print contact_group_id
            #         print "przerwa"

            # if a == 3:
            #     phoneNumber2 = contact_group_id
            #     print "numerrrrrrrr"
            #     print str(phoneNumber2)
            # a = a + 1
            # if a == 4:
            #     a = 1

            # dl = len(contact_group_id)
            # if dl <= 1:
            # current_contact = Contact(str(name), str(phoneNumber), str(contact_group_id), str(contact_group_name))
            # contacts.append(current_contact)

            self.ids.scroll.bind(minimum_height=self.ids.scroll.setter('height'))

            contacts.sort(key=lambda contact: contact.display_name)
            for contact in contacts:
                btn = Button(text=contact.display_name, on_release=callPhone)
                # btn = Button(text=contact.display_name + "  " + contact.group_id + "  " +contact.number, on_release=callPhone)
                self.ids.scroll.add_widget(btn)
                # contactsGroups[contact.number] = contact.group_id

    def submit_contact2(self):
        if platform() == 'android':
            Phone = autoclass("android.provider.ContactsContract$CommonDataKinds$Phone")
            ContactsContract = autoclass("android.provider.ContactsContract$Contacts")
            GroupMembership = autoclass("android.provider.ContactsContract$CommonDataKinds$GroupMembership")

            ContentResolver = autoclass('android.content.Context')

            content_resolver = activity.getApplicationContext()

            resolver = content_resolver.getContentResolver()

            ApplicationContext = autoclass('android.app.Activity')
            # app = ApplicationContext.getApplicationContext()
            Toast = autoclass("android.widget.Toast")
            Cursor = autoclass("android.database.Cursor")
            Data = autoclass("android.provider.ContactsContract$Data")
            phones = resolver.query(Phone.CONTENT_URI, None, None, None, None)
            phones2 = resolver.query(Data.CONTENT_URI, None, None, None, None)
            pho = phones
            pho2 = phones2

            self.read_groups()

            RawContactsColumns = autoclass("android.provider.ContactsContract$RawContactsColumns")
            projection = [GroupMembership.GROUP_ROW_ID, RawContactsColumns.CONTACT_ID]
            # projection = [GroupMembership.GROUP_ROW_ID, "contact_id"]
            Cursor = autoclass("android.database.Cursor")
            # c = resolver.query(Data.CONTENT_URI, projection, GroupMembership.GROUP_ROW_ID+"="+groups,None, None)
            a = 1
            print "cosik4"
            while (phones2.moveToNext()):
                name = pho2.getString(pho2.getColumnIndex("display_name"))
                idGrupy = pho2.getString(pho2.getColumnIndex(Phone.NUMBER))
                contact_group_id = pho2.getString(pho2.getColumnIndex(GroupMembership.GROUP_ROW_ID))
                contact_group_name = -1
                for group in groups:
                    if contact_group_id == group.id:
                        contact_group_name = group.name

                #dl = len(contact_group_id)
                if contact_group_id is not None:
                    try:
                        dl = len(contact_group_id)
                        if dl <= 1:

                            current_contact = Contact(str(name), str(contact_group_id), str(contact_group_id),
                                                      str(contact_group_name))
                            contacts2.append(current_contact)

                            if name == "Daniel":
                                print name
                                print idGrupy
                                print str(contact_group_id)
                                print "przerwa2"
                    except:
                        pass

            while (phones.moveToNext()):
                name = pho.getString(pho.getColumnIndex("display_name"))
                phoneNumber = pho.getString(pho.getColumnIndex(Phone.NUMBER))
                contact_group_id = pho.getString(pho.getColumnIndex(GroupMembership.GROUP_ROW_ID))
                contact_group_name = -1
                for group in groups:
                    if contact_group_id == group.id:
                        contact_group_name = group.name
                if name == "Daniel":
                    print name
                    print phoneNumber
                    print "przerwa"

                # if a == 3:
                #     phoneNumber2 = contact_group_id
                #     print "numerrrrrrrr"
                #     print str(phoneNumber2)
                # a = a + 1
                # if a == 4:
                #     a = 1

                # dl = len(contact_group_id)
                # if dl <= 1:

                num = str(phoneNumber)
                num = num.replace(" ", "")
                num = num.replace("-", "")
                if num[0] == "+":
                    num = num[-9:]

                current_contact = Contact(str(name), str(num), str(num), str(num))
                contacts.append(current_contact)

            contacts.sort(key=lambda contact: contact.display_name)
            contacts2.sort(key=lambda contact: contact.display_name)

            for contact in contacts:
                contactsGroups[contact.number] = contact.display_name

            for contact in contacts2:
                contactsGroups2[contact.display_name] = contact.number



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
        super(LineMapLayer, self).__init__()
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


class ZoneList:
    _zoneL = []
    Lista = []

    def __init__(self):
        super(self).__init__()

    activity = autoclass("org.renpy.android.PythonActivity").mActivity
    Grupy = autoclass("android.provider.ContactsContract$Groups")
    content_resolver = activity.getApplicationContext()
    resolver = content_resolver.getContentResolver()

    grupa = resolver.query(Grupy.CONTENT_URI, None, None, None, None)
    group = grupa

    while (grupa.moveToNext()):

        g = group.getString(group.getColumnIndex("TITLE"))
        f = group.getString(group.getColumnIndex("_id"))
        if g not in _zoneL:
            _zoneL.append(g)
            Lista.append(f)
    grupa.close()

    conn = sqlite3.connect('baza.db')
    c = conn.cursor()

    c.execute("CREATE TABLE IF NOT EXISTS Grupy (NAZWA TEXT, REAKCJA TEXT, ID_GRUPY INTEGER)")
    c.execute("SELECT * FROM Grupy")
    dane = c.fetchall()

    if dane == []:
        for x in xrange(0, len(_zoneL)):
            c.execute("INSERT INTO Grupy VALUES (?, ?, ?)", (_zoneL[x], 'autoodebranie', Lista[x]))

    conn.commit()
    conn.close()


class ZoneElements(GridLayout):
    pass


class ZoneCheckBoxes(GridLayout):
    _instance_count = -1
    _zoneNames = ZoneList._zoneL

    # autood = ObjectProperty(False)
    # odrz = StringProperty(False)
    # odrzSMS = ObjectProperty(False)

    def __init__(self, **kwargs):
        super(ZoneCheckBoxes, self).__init__(**kwargs)
        ZoneCheckBoxes._instance_count += 1

        conn = sqlite3.connect('baza.db')
        c = conn.cursor()

        c.execute("SELECT REAKCJA FROM Grupy")
        dane = c.fetchall()

        if (dane[ZoneCheckBoxes._instance_count]) == (u'autoodebranie',):
            ZoneCheckBoxes.autood = True
            ZoneCheckBoxes.odrzSMS = False
            ZoneCheckBoxes.odrz = False

        else:
            if dane[ZoneCheckBoxes._instance_count] == (u'odrzucenieSMS',):
                ZoneCheckBoxes.autood = False
                ZoneCheckBoxes.odrzSMS = True
                ZoneCheckBoxes.odrz = False

            else:
                ZoneCheckBoxes.autood = False
                ZoneCheckBoxes.odrzSMS = False
                ZoneCheckBoxes.odrz = True

    def autoodebranie(self, x):
        conn = sqlite3.connect('baza.db')
        c = conn.cursor()
        c.execute("UPDATE Grupy SET REAKCJA=? WHERE NAZWA=?", ('autoodebranie', x[5:len(x)]))
        conn.commit()

    def odrzucenieSMS(self, x):
        conn = sqlite3.connect('baza.db')
        c = conn.cursor()
        c.execute("UPDATE Grupy SET REAKCJA=? WHERE NAZWA=?", ('odrzucenieSMS', x[5:len(x)]))
        conn.commit()

    def odrzucenie(self, x):
        conn = sqlite3.connect('baza.db')
        c = conn.cursor()
        c.execute("UPDATE Grupy SET REAKCJA=? WHERE NAZWA=?", ('odrzucenie', x[5:len(x)]))
        conn.commit()


class ZoneButton(Button):
    _instance_count = -1
    _zoneNames = ZoneList._zoneL

    def __init__(self, **kwargs):
        super(ZoneButton, self).__init__(**kwargs)
        ZoneButton._instance_count += 1


class ZoneLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(ZoneLayout, self).__init__(**kwargs)

        for i in range(len(ZoneList._zoneL)):
            self.add_widget(ZoneElements())


class MainApp(App):
    gps_location = StringProperty()
    gps_status = StringProperty('Click Start to get GPS location updates')
    lat = 53.0102
    lon = 18.5946
    flagCenter = True
    # screensettings.kv tymczasowo zakomentowany w pliku main.kv
    Builder.load_file("screensettings.kv")
    Builder.load_file("groupscreen.kv")
    Builder.load_file("callscreen.kv")
    Builder.load_file("musicplayer.kv")
    Builder.load_file("grupy.kv")
    znacznik = 0
    route_nodes = BooleanProperty(False)
    prev_time = datetime.datetime.now().time()
    needle_angle = NumericProperty(0)

    def build(self):
        show_time = ShowTime()
        callS = CallScreen()
        callS.submit_contact2()
        music = MusicPlayer()
        music.getpath()
        self._anim = None
        Clock.schedule_interval(self.update_compass, 1)
        # modyfikacja 3
        gr = GroupScreen()
        # rotacja_mapy
        gr.do_toggle()
        Clock.schedule_interval(gr.get_readings, 1)
        # rotacja_mapy
        Clock.schedule_interval(show_time.check2, 1)
        try:
            gps.configure(on_location=self.on_location, on_status=self.on_status)
            self.start(1000, 0)
            #modyfikacja rotacja
            self._anim = None
            #Hardware.magneticFieldSensorEnable(True)
            # Clock.schedule_interval(self.update_compass, 1)
            #modyfikacja rotacja
        except NotImplementedError:
            self.gps_status = 'GPS is not implemented for your platform'
        return show_time

    def update_compass(self, *args):

        needle_angle = wsp2
        print "wypisz_wsp"
        print "wsp2"
        print wsp2
        print "needle_angle"
        print needle_angle
        if self._anim:
            self._anim.stop(self)
        self._anim = Animation(needle_angle=needle_angle, d=.2, t='out_quad')
        self._anim.start(self)

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

            group = GroupScreen()
            # modyfikacja 4
            #group.do_toggle()
            #group.get_readings(1)
            #group.rotate2()

            flaga_gps = group.returnFlag()
            lat_2 = group.returnLat()
            lon_2 = group.lonGPS

            print "test_gps"
            print lat_2
            print lon_2
            print flaga_gps

            MainApp.get_running_app().root.carousel.slides[0].ids["marker"].lat = float(MainApp.lat)
            MainApp.get_running_app().root.carousel.slides[0].ids["marker"].lon = float(MainApp.lon)
            if flaga_gps == 1:
                MainApp.get_running_app().root.carousel.slides[0].ids["marker2"].lat = lat_2
                MainApp.get_running_app().root.carousel.slides[0].ids["marker2"].lon = lat_2

            if MainApp.get_running_app().root.carousel.slides[0].auto_center:
                mapview.center_on(float(MainApp.lat), float(MainApp.lon))
                MainApp.get_running_app().root.carousel.slides[0].redraw_route()

            if self.flagCenter == True:
                mapview.center_on(float(MainApp.lat), float(MainApp.lon))
                MainApp.get_running_app().root.carousel.slides[0].redraw_route()
                self.flagCenter = False
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
