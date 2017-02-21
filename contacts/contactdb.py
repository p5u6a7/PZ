__version__ = '1.0'
from kivy.lang import Builder
from kivy.app import App
from kivy.utils import platform
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.listview import ListItemButton
from jnius import autoclass


class ContactListButton(ListItemButton):
    pass


class ContactDB(BoxLayout):

    contact_list = ObjectProperty()

    def display_contact(self):
        if platform() == 'android':

            Phone = autoclass("android.provider.ContactsContract$CommonDataKinds$Phone")
            ContactsContract = autoclass("android.provider.ContactsContract$Contacts")

            ContentResolver = autoclass('android.content.Context')
            resolver = ContentResolver.getContentResolver()

            ApplicationContext = autoclass('android.app.Activity')
            app = ApplicationContext.getApplicationContext()

            Toast = autoclass("android.widget.Toast")
            Cursor = autoclass("android.database.Cursor")

            phones = resolver.query(ContactsContract.CommonDataKinds.Phone.CONTENT_URI, None, None, None, None)
            pho = phones.Cursor()

            while (phones.moveToNext()):

                name = pho.getString(pho.getColumnIndex(ContactsContract.CommonDataKinds.Phone.DISPLAY_NAME))
                phoneNumber = pho.getString(pho.getColumnIndex(ContactsContract.CommonDataKinds.Phone.NUMBER))
                Toast.makeText(app, name, Toast.LENGTH_LONG).show()

                #Dodawanie do ListView
                self.contact_list.adapter.data.extend([name])

                # Reset ListView
                #self.contact_list._trigger_reset_populate()

            pho.close()


class ContactDBApp(App):

    Builder.load_file("contactdb.kv")

    def build(self):
        return ContactDB()

dbApp = ContactDBApp()
dbApp.run()