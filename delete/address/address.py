from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.lang import Builder
from database import query, delete

Builder.load_file('delete/address/address.kv')


class DeleteAddressPopUp(BoxLayout):

    def __int__(self):
        super(BoxLayout, self).__init__()
        self.address_list = []

    def pick_values(self):
        postgres_query = "SELECT * FROM address"
        self.address_list = query(postgres_query, "address")
        address_id_list = []
        for row in self.address_list:
            address_id_list.append(row[0])
        return address_id_list

    def update_form(self):
        phone = self.ids.address_selector.text
        row = tuple()
        for i, v in enumerate(self.address_list):
            if v[0] == phone:
                row = v
        self.ids.addressName.text = row[1]
        self.ids.addressAddress.text = row[2]

    def delete(self):
        phone = self.ids.address_selector.text
        postgres_delete_query = """DELETE FROM address
                                   WHERE phone = %s"""
        values = (phone, )
        delete(postgres_delete_query, values, "address")


def show_delete_address_popup():
    show = DeleteAddressPopUp()
    popup_window = Popup(title="Delete Address", content=show)
    show.ids.cancel.bind(on_press=popup_window.dismiss)
    popup_window.open()