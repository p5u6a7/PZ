from kivy.app import App
from kivy.utils import platform
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.uix.listview import ListItemButton
from jnius import autoclass


class ZoneList():

    _zoneL = []

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

    #_zoneL = ["Basement","Sun Room","Den","Living Room","Front Door"]


class ZoneElements(GridLayout):
    pass


class ZoneCheckBoxes(GridLayout):
    _instance_count = -1
    _zoneNames = ZoneList._zoneL

    def __init__(self, **kwargs):
        super(ZoneCheckBoxes, self).__init__(**kwargs)
        ZoneCheckBoxes._instance_count += 1
    

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


