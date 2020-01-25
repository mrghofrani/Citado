import psycopg2

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.lang import Builder

Builder.load_file('insert_customer.kv')

global db_connection

def initialize():
    global db_connection
    db_connection = psycopg2.connect(user="engmrgh",
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
        postgres_insert_query = " INSERT INTO customer(national_code, first_name, last_name, mobile_number, age) " \
                                "VALUES (%s, %s, %s, %s, %s) "
        values = (national_code, first_name, last_name, mobile_number, age)
        try:
            c = db_connection.cursor()
            c.execute(postgres_insert_query, values)

            db_connection.commit()
            count = c.rowcount
            print(count, "Record inserted successfully into mobile table")

        except (Exception, psycopg2.Error) as error:
            if db_connection:
                print("Failed to insert record into mobile table", error)
        finally:
            # closing database connection.
            if (db_connection):
                c.close()



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


if __name__ == "__main__":
    initialize()
    MainPage().run()