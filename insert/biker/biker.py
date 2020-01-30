from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.lang import Builder
from database import insert

Builder.load_file('insert/biker/biker.kv')


class InsertBikerPopUp(BoxLayout):
    def submit(self):
        national_code = self.ids.bikerNationalCodeInput.text
        first_name = self.ids.bikerFirstName.text
        last_name = self.ids.bikerLastName.text
        mobile_number = self.ids.bikerMobileNumber.text

        postgres_insert_query = """ INSERT INTO biker(national_code, first_name, last_name, mobile_number) 
                                    VALUES (%s, %s, %s, %s) """
        values = (national_code, first_name, last_name, mobile_number)
        insert(postgres_insert_query, values, "biker")


def show_insert_biker_popup():
    show = InsertBikerPopUp()
    popup_window = Popup(title="Insert biker", content=show)
    show.ids.cancel.bind(on_press=popup_window.dismiss)
    popup_window.open()
