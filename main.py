import psycopg2

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.lang import Builder

from datetime import datetime

Builder.load_file('insert_customer.kv')
Builder.load_file('insert_biker.kv')
Builder.load_file('insert_address.kv')


def get_connection():
    return psycopg2.connect(user="engmrgh",
                                    password="h3ll9db",
                                    host="localhost",
                                    port="5432",
                                    database="citado")


class MainLayout(BoxLayout):
    def order_food_button(self):
        show_food_order_popup()

    def order_raw_material_button(self):
        show_raw_material_order_popup()

    def insert_customer_button(self):
        show_insert_customer_popup()

    def insert_biker_button(self):
        show_insert_biker_popup()

    def insert_address_button(self):
        show_insert_address_popup()


class FoodOrderPopUp(BoxLayout):
    pass


class RawMaterialOrderPopUp(BoxLayout):
    pass


class InsertCustomerPopUp(BoxLayout):
    def submit(self):
        national_code = self.ids.customerNationalCodeInput.text
        first_name = self.ids.customerFirstName.text
        last_name = self.ids.customerLastName.text
        mobile_number = self.ids.customerMobileNumber.text
        age = self.ids.customerAge.text
        connection = get_connection()
        postgres_insert_query = " INSERT INTO customer(national_code, first_name, last_name, mobile_number, age) " \
                                " VALUES (%s, %s, %s, %s, %s) "
        values = (national_code, first_name, last_name, mobile_number, age)
        try:
            cursor = connection.cursor()
            cursor.execute(postgres_insert_query, values)

            connection.commit()
            count = cursor.rowcount
            print(count, "Record inserted successfully into mobile table")

        except (Exception, psycopg2.Error) as error:
            if connection:
                print("Failed to insert record into mobile table", error)
        finally:
            # closing database connection.
            if connection :
                cursor.close()
                connection.close()


class InsertBikerPopUp(BoxLayout):
    def submit(self):
        national_code = self.ids.bikerNationalCodeInput.text
        first_name = self.ids.bikerFirstName.text
        last_name = self.ids.bikerLastName.text
        mobile_number = self.ids.bikerMobileNumber.text
        connection = get_connection()
        postgres_insert_query = " INSERT INTO bike_delivery(national_code, first_name, last_name, mobile_number) " \
                                "VALUES (%s, %s, %s, %s) "
        values = (national_code, first_name, last_name, mobile_number)
        try:
            cursor = connection.cursor()
            cursor.execute(postgres_insert_query, values)

            connection.commit()
            count = cursor.rowcount
            print(count, "Record inserted successfully into bike_delivery table")

        except (Exception, psycopg2.Error) as error:
            if connection:
                print("Failed to insert record into bike_delivery table", error)
        finally:
            # closing database connection.
            if connection:
                cursor.close()
                connection.close()


class InsertAddressPopUp(BoxLayout):
    def submit(self):
        phone_number = self.ids.addressPhoneNumber.text
        name = self.ids.addressName.text
        address = self.ids.addressAddress.text
        connection = get_connection()
        postgres_insert_query = " INSERT INTO address(phone, name, address) VALUES (%s,%s,%s) "

        values = (phone_number, name, address)
        try:
            cursor = connection.cursor()
            cursor.execute(postgres_insert_query, values)

            connection.commit()
            count = cursor.rowcount
            print(count, "Record inserted successfully into address table")

        except (Exception, psycopg2.Error) as error:
            if connection:
                print("Failed to insert record into address table ", error)
        finally:
            # closing database connection.
            if connection:
                cursor.close()
                connection.close()


class MainPage(App):
    def build(self):
        return MainLayout()


def show_food_order_popup():
    show = FoodOrderPopUp()
    popup_window = Popup(title="Order Food", content=show)
    show.ids['food_order_cancel'].bind(on_press=popup_window.dismiss)
    popup_window.open()


def show_raw_material_order_popup():
    show = RawMaterialOrderPopUp()
    popup_window = Popup(title="Order Raw Material", content=show)
    show.ids['raw_material_order_cancel'].bind(on_press=popup_window.dismiss)
    popup_window.open()


def show_insert_customer_popup():
    show = InsertCustomerPopUp()
    popup_window = Popup(title="Insert cutomer", content=show)
    show.ids['insert_customer_cancel'].bind(on_press=popup_window.dismiss)
    popup_window.open()


def show_insert_biker_popup():
    show = InsertBikerPopUp()
    popup_window = Popup(title="Insert biker", content=show)
    show.ids['insertBikerCancel'].bind(on_press=popup_window.dismiss)
    popup_window.open()


def show_insert_address_popup():
    show = InsertAddressPopUp()
    popup_window = Popup(title="Insert Address", content=show)
    show.ids['insertAddressCancel'].bind(on_press=popup_window.dismiss)
    popup_window.open()


if __name__ == "__main__":
    MainPage().run()