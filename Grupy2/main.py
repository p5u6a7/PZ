from kivy.app import App
from kivy.utils import platform
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from jnius import autoclass
import sqlite3
import sys


class ZoneList():

    _zoneL = []
    #group_list = ObjectProperty()
    
    if platform() == 'android':
        activity = autoclass("org.renpy.android.PythonActivity").mActivity
        Grupy = autoclass("android.provider.ContactsContract$Groups")
        content_resolver = activity.getApplicationContext()
        resolver = content_resolver.getContentResolver()

        grupa = resolver.query(Grupy.CONTENT_URI, None, None, None, None)
        group = grupa

        while (grupa.moveToNext()):

            g = group.getString(group.getColumnIndex("TITLE"))
            if g not in _zoneL:
                _zoneL.append(g)
        grupa.close()
    

    conn = sqlite3.connect('baza.db')
    c = conn.cursor()

    c.execute("CREATE TABLE IF NOT EXISTS Grupy (NAZWA text, BUTTON text)")

    c.execute("SELECT * FROM Grupy")

    dane = c.fetchall()

    if dane == []:
        for i in _zoneL:
            c.execute("INSERT INTO Grupy VALUES (?, ?)", (i, 'autoodebranie'))

    conn.commit()
    conn.close()


class ZoneElements(GridLayout):
    pass


class ZoneCheckBoxes(GridLayout):
    _instance_count = -1
    _zoneNames = ZoneList._zoneL

    #autood = ObjectProperty(False)
    #odrz = StringProperty(False)
    #odrzSMS = ObjectProperty(False)

    def __init__(self, **kwargs):
        super(ZoneCheckBoxes, self).__init__(**kwargs)
        ZoneCheckBoxes._instance_count += 1

        conn = sqlite3.connect('baza.db')
        c = conn.cursor()

        c.execute("SELECT BUTTON FROM Grupy")
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
        c.execute("UPDATE Grupy SET BUTTON=? WHERE NAZWA=?", ('autoodebranie', x[5:len(x)]))
        conn.commit()

    def odrzucenieSMS(self, x):
        conn = sqlite3.connect('baza.db')
        c = conn.cursor()
        c.execute("UPDATE Grupy SET BUTTON=? WHERE NAZWA=?", ('odrzucenieSMS', x[5:len(x)]))
        conn.commit()

    def odrzucenie(self, x):
        conn = sqlite3.connect('baza.db')
        c = conn.cursor()
        c.execute("UPDATE Grupy SET BUTTON=? WHERE NAZWA=?", ('odrzucenie', x[5:len(x)]))
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


class Grupy(App):
    pass


def main():
    Grupy().run()
    
    return 0

if __name__ == '__main__':
    main()


