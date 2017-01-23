# coding=utf-8
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

from os import listdir, path


class ChooseFile(FloatLayout):
    select = ObjectProperty(None)
    cancel = ObjectProperty(None)


class MusicPlayer(Screen):
    directory = ''  # lokacja folderu z piosenkami
    nowPlaying = ''  # Aktualnie wybrana piosenka
    songs = []  # Lista utworów

    def stopSong(self):
        if self.nowPlaying == '':
            title = self.songs[0]
            self.nowPlaying = SoundLoader.load(self.directory + str(title))
            self.ids.nowplay.text = self.songs[0]
        if self.nowPlaying.state == 'stop':
            self.nowPlaying.play()
        else:
            self.nowPlaying.stop()

    def nextSong(self):
        if self.nowPlaying == '':
            title = self.songs[0]
            self.nowPlaying = SoundLoader.load(self.directory + str(title))
            self.ids.nowplay.text = self.songs[0]
        a = 0
        b = int(a)

        next2 = 0
        self.nowPlaying.stop()
        for song in self.songs:
            self.nowPlaying = SoundLoader.load(self.directory + self.ids.nowplay.text + '.mp3')
            self.nowPlaying.stop()

            if self.songs[b] == self.ids.nowplay.text:
                next1 = b + 1
                next2 = int(next1)
            b += 1

        title = self.songs[next2]
        self.nowPlaying = SoundLoader.load(self.directory + str(title))
        self.nowPlaying.play()
        self.ids.nowplay.text = self.songs[next2]

    def backSong(self):
        if self.nowPlaying == '':
            title = self.songs[0]
            self.nowPlaying = SoundLoader.load(self.directory + str(title))
            self.ids.nowplay.text = self.songs[0]
        a = 0
        b = int(a)
        next = 0
        next2 = 0
        self.nowPlaying.stop()
        for song in self.songs:
            self.nowPlaying = SoundLoader.load(self.directory + self.ids.nowplay.text + '.mp3')

            self.nowPlaying.stop()

            if self.songs[b] == self.ids.nowplay.text:
                next = b - 1
                next2 = int(next)
            b = b + 1

        title = self.songs[next2]
        self.nowPlaying = SoundLoader.load(self.directory + str(title))
        self.nowPlaying.play()
        self.ids.nowplay.text = self.songs[next2]

    def getpath(self):
        try:
            f = open("sav.dat", "r")
            self.ids.direct.text = str(f.readline())
            f.close()
            self.ids.searchBtn.text = "Wybierz folder"
            self.getSongs()
        except:
            self.ids.direct.text = ''

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

            for song in self.songs:

                def playSong(bt):
                    try:
                        self.nowPlaying.stop()
                    except:
                        pass
                    finally:
                        self.nowPlaying = SoundLoader.load(self.directory + bt.text + '.mp3')
                        # .length pobiera dla cześci plików błędą wartości -1
                        #print("%f\n" % self.nowPlaying.length)
                        self.nowPlaying.play()
                        self.ids.nowplay.text = bt.text + '.mp3'

                btn = Button(text=song[:-4], on_press=playSong)
                icon = Button(size_hint_x=None, size_hint_y=None, background_down="ico.png", background_normal="ico.png")

                # Color Buttons Alternatively
                if self.songs.index(song) % 2 == 0:
                    btn.background_color = (.1, .1, .1, 1)
                else:
                    btn.background_color = (.2, .2, .2, 1)

                #dodanie elementów etykiet utworów
                self.ids.scroll.add_widget(icon)
                self.ids.scroll.add_widget(btn)




class KVMusicApp(App):
    def build(self):
        Builder.load_file("MusicPlayer.kv")
        music = MusicPlayer()
        music.getpath()
        return music

    def on_pause(self):
        return True

    def on_resume(self):
        pass


if __name__ == "__main__":
    KVMusicApp().run()
