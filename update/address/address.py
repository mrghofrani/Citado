from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.lang import Builder
from database import update, query

Builder.load_file('update/address/address.kv')


class UpdateAddressPopUp(BoxLayout):

    def pick_values(self):
        postgres_query = "SELECT * FROM address"
        self.address_list = query(postgres_query, "address")
        address_id_list = []
        for row in self.address_list:
            address_id_list.append(row[0])
        return address_id_list

    def update_form(self):
        if self.address_list:
            selected_id = self.ids.address_selector.text
            row = tuple()
            for i, v in enumerate(self.address_list):
                if v[0] == selected_id:
                    row = v
            self.ids.addressName.text = row[1]
            self.ids.addressAddress.text = row[2]

    def submit(self):
        phone_number = self.ids.address_selector.text
        name = self.ids.addressName.text
        address = self.ids.addressAddress.text

        postgres_update_query = """UPDATE address
                              SET name = %s, address = %s
                              WHERE phone = %s"""
        values = (name, address, phone_number)

        update(postgres_update_query, values, "address")


def show_update_address_popup():
    show = UpdateAddressPopUp()
    popup_window = Popup(title="Update Address", content=show)
    show.ids.cancel.bind(on_press=popup_window.dismiss)
    popup_window.open()