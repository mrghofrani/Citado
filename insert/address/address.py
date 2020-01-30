from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.lang import Builder
from database import insert, query

Builder.load_file('insert/address/address.kv')


class InsertAddressPopUp(BoxLayout):
    def get_customer_list(self):
        postgres_query = """SELECT national_code FROM customer"""
        customer_list_tmp = query(postgres_query, "customer")
        customer_list = []
        for row in customer_list_tmp:
            customer_list.append(row[0])
        return customer_list

    def submit(self):
        phone_number = self.ids.phone_number.text
        name = self.ids.name.text
        address = self.ids.address.text
        customer = self.ids.customer.text

        postgres_insert_query = """INSERT INTO address(phone, name, address) VALUES (%s,%s,%s)"""
        values = (phone_number, name, address)
        insert(postgres_insert_query, values, "address") # adding to database

        postgres_insert_query = """INSERT INTO customer_address(customer_national_code, address_phone) VALUES (%s,%s)"""
        values = (customer, phone_number)
        insert(postgres_insert_query, values, "customer_address")




def show_insert_address_popup():
    show = InsertAddressPopUp()
    popup_window = Popup(title="Insert Address", content=show)
    show.ids.cancel.bind(on_press=popup_window.dismiss)
    popup_window.open()
