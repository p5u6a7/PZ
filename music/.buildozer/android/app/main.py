# coding=utf-8
import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.core.audio import SoundLoader, Sound
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from functools import partial
from os import listdir, path
from kivy.clock import Clock
import os

print "aaa1bbb"
class ChooseFile(FloatLayout):
    select = ObjectProperty(None)
    cancel = ObjectProperty(None)


class MusicPlayer(Screen):
    directory = ''  # lokacja folderu z piosenkami
    nowPlaying = ''  # Aktualnie wybrana piosenka
    songs = []  # Lista utworów
    songs2 = []  # Lista utworów
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
            for root, dirs, files in os.walk('/storage'):
                for f in files:
                    filename = os.path.join(root, f)
                    if filename.endswith('.mp3'):
                        self.songs.append(filename)
                        self.songs2.append(f)
                        print f
            #for fil in listdir(self.directory):
                #if fil.endswith('.mp3'):
                    #self.songs.append(fil)

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
        for song in self.songs2:

            btn = Button(text=song[:-4], on_press=playSong)
            icon = Button(size_hint_x=None, size_hint_y=None, background_down="ico.png", background_normal="ico.png")

            # kolorowanie elementów listy
            if self.songs2.index(song) % 2 == 0:
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

#główna klasa programu
class KVMusicApp(App):
    def build(self):
        Builder.load_file("musicplayer.kv")
        music = MusicPlayer()
        music.getpath()
        print music.nowPlaying

        return music

    def on_pause(self):
        return True

    def on_resume(self):
        pass


if __name__ == "__main__":
    KVMusicApp().run()
