from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.lang import Builder
from database import insert

Builder.load_file('insert/address/address.kv')


class InsertAddressPopUp(BoxLayout):
    def submit(self):
        phone_number = self.ids.addressPhoneNumber.text
        name = self.ids.addressName.text
        address = self.ids.addressAddress.text

        postgres_insert_query = """INSERT INTO address(phone, name, address) VALUES (%s,%s,%s)"""
        values = (phone_number, name, address)
        insert(postgres_insert_query, values, "address") # adding to database


def show_insert_address_popup():
    show = InsertAddressPopUp()
    popup_window = Popup(title="Insert Address", content=show)
    show.ids.cancel.bind(on_press=popup_window.dismiss)
    popup_window.open()
