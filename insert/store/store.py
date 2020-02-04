from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.lang import Builder
from database import insert

Builder.load_file('insert/store/store.kv')


class InsertStorePopUp(BoxLayout):
    def submit(self):
        name = self.ids.name.text
        start_time = self.ids.start_time.text
        end_time = self.ids.end_time.text

        postgres_insert_query = """ INSERT INTO store(name, start_time, end_time)
                                    VALUES (%s, %s, %s) """
        values = (name, start_time, end_time)

        insert(postgres_insert_query, values, "store")


def show_insert_store_popup():
    show = InsertStorePopUp()
    popup_window = Popup(title="Insert store", content=show)
    show.ids.cancel.bind(on_press=popup_window.dismiss)
    popup_window.open()