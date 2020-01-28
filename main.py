import psycopg2

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.lang import Builder

from datetime import datetime



def get_connection():
    return psycopg2.connect(user="engmrgh",
                                    password="h3ll9db",
                                    host="localhost",
                                    port="5432",
                                    database="citado")

# ------------------- #
#   Ordering Part     #
# ------------------- #


# ---- Food Order ----#
class FoodOrderPopUp(BoxLayout):
    pass


def show_food_order_popup():
    show = FoodOrderPopUp()
    popup_window = Popup(title="Order Food", content=show)
    show.ids['food_order_cancel'].bind(on_press=popup_window.dismiss)
    popup_window.open()


# ---- Raw Material Order -----#
class RawMaterialOrderPopUp(BoxLayout):
    pass


def show_raw_material_order_popup():
    show = RawMaterialOrderPopUp()
    popup_window = Popup(title="Order Raw Material", content=show)
    show.ids['raw_material_order_cancel'].bind(on_press=popup_window.dismiss)
    popup_window.open()


# =================== #
#   Insertion Part    #
# =================== #

# ------ Insert Customer ------ #
Builder.load_file('insert_customer.kv')


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


def show_insert_customer_popup():
    show = InsertCustomerPopUp()
    popup_window = Popup(title="Insert cutomer", content=show)
    show.ids['insert_customer_cancel'].bind(on_press=popup_window.dismiss)
    popup_window.open()


# ---- Insert Biker ---- #
Builder.load_file('insert_biker.kv')


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


def show_insert_biker_popup():
    show = InsertBikerPopUp()
    popup_window = Popup(title="Insert biker", content=show)
    show.ids['insertBikerCancel'].bind(on_press=popup_window.dismiss)
    popup_window.open()


# ---- insert Address ---- #
Builder.load_file('insert_address.kv')


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


def show_insert_address_popup():
    show = InsertAddressPopUp()
    popup_window = Popup(title="Insert Address", content=show)
    show.ids['insertAddressCancel'].bind(on_press=popup_window.dismiss)
    popup_window.open()


# ------------------------------ #
#         Update Part            #
# -------------------------------#

# ------ update Customer --------

Builder.load_file('update_customer.kv')


class UpdateCustomerPopUp(BoxLayout):

    def __int__(self):
        super(BoxLayout, self).__init__()
        self.customer_list = []

    def pick_values(self):
        connection = get_connection()
        postgres_insert_query = "SELECT * FROM customer"
        try:
            cursor = connection.cursor()
            cursor.execute(postgres_insert_query)
            print("Selecting rows from mobile table using cursor.fetchall")
            self.customer_list = cursor.fetchall()
            customer_id_list = []
            for row in self.customer_list:
                customer_id_list.append(row[0])

        except (Exception, psycopg2.Error) as error:
            if connection:
                print("Failed to fetch record into address table ", error)
        finally:
            # closing database connection.
            if connection:
                cursor.close()
                connection.close()
        return customer_id_list

    def update_form(self):
        selected_id = self.ids.customer_selector.text
        row = tuple()
        for i, v in enumerate(self.customer_list):
            if v[0] == selected_id:
                row = v
        self.ids.customerFirstName.text = row[1]  # First Name of Customer
        self.ids.customerLastName.text = row[2]  # Last Name of Customer
        self.ids.customerMobileNumber.text = row[3]  # Mobile number of Customer
        self.ids.customerAge.text = str(row[4])  # Age of Customer

    def submit(self):
        national_code = self.ids.customer_selector.text
        first_name = self.ids.customerFirstName.text
        last_name = self.ids.customerLastName.text
        mobile_number = self.ids.customerMobileNumber.text
        age = self.ids.customerAge.text
        try:
            connection = get_connection()
            cursor = connection.cursor()
            sql_update_query = """UPDATE customer
                                  SET first_name = %s, last_name = %s, mobile_number = %s, age = %s
                                  WHERE national_code = %s"""
            cursor.execute(sql_update_query, (first_name, last_name, mobile_number, age, national_code))
            connection.commit()
            count = cursor.rowcount
            print(count, "Record Updated successfully ")

        except (Exception, psycopg2.Error) as error:
            if connection:
                print("Failed to update record into address table ", error)
        finally:
            # closing database connection.
            if connection:
                cursor.close()
                connection.close()


def show_update_customer_popup():
    show = UpdateCustomerPopUp()
    popup_window = Popup(title="Update Customer", content=show)
    show.ids['update_customer_cancel'].bind(on_press=popup_window.dismiss)
    popup_window.open()


# ---------- Update Address -------------
Builder.load_file('update_address.kv')


class UpdateAddressPopUp(BoxLayout):

    def __int__(self):
        super(BoxLayout, self).__init__()
        self.address_list = []

    def pick_values(self):
        connection = get_connection()
        postgres_insert_query = "SELECT * FROM address"
        address_id_list = []
        try:
            cursor = connection.cursor()
            cursor.execute(postgres_insert_query)
            self.address_list = cursor.fetchall()
            address_id_list = []
            for row in self.address_list:
                address_id_list.append(row[0])

        except (Exception, psycopg2.Error) as error:
            if connection:
                print("Failed to fetch record into address table ", error)
        finally:
            # closing database connection.
            if connection:
                cursor.close()
                connection.close()
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
        connection, cursor = None, None
        try:
            connection = get_connection()
            cursor = connection.cursor()
            sql_update_query = """UPDATE address
                                  SET name = %s, address = %s
                                  WHERE phone = %s"""
            cursor.execute(sql_update_query, (name, address, phone_number))
            connection.commit()
            count = cursor.rowcount
            print(count, "Record Updated successfully ")

        except (Exception, psycopg2.Error) as error:
            if connection:
                print("Failed to update record into address table ", error)
        finally:
            # closing database connection.
            if connection:
                cursor.close()
                connection.close()


def show_update_address_popup():
    show = UpdateAddressPopUp()
    popup_window = Popup(title="Update Address", content=show)
    show.ids['update_address_cancel'].bind(on_press=popup_window.dismiss)
    popup_window.open()


# ------------------------------ #
#         Deletion Part          #
# ------------------------------ #

# ---------- Delete Customer -------------
Builder.load_file('delete_customer.kv')


class DeleteCustomerPopUp(BoxLayout):

    def __int__(self):
        super(BoxLayout, self).__init__()
        self.customer_list = []

    def pick_values(self):
        connection = get_connection()
        postgres_insert_query = "SELECT * FROM customer"
        try:
            cursor = connection.cursor()
            cursor.execute(postgres_insert_query)
            self.customer_list = cursor.fetchall()
            customer_id_list = []
            for row in self.customer_list:
                customer_id_list.append(row[0])

        except (Exception, psycopg2.Error) as error:
            if connection:
                print("Failed to fetch record into address table ", error)
        finally:
            # closing database connection.
            if connection:
                cursor.close()
                connection.close()
        return customer_id_list

    def update_form(self):
        selected_id = self.ids.customer_selector.text
        row = tuple()
        for i, v in enumerate(self.customer_list):
            if v[0] == selected_id:
                row = v
        self.ids.customerFirstName.text = row[1]  # First Name of Customer
        self.ids.customerLastName.text = row[2]  # Last Name of Customer
        self.ids.customerMobileNumber.text = row[3]  # Mobile number of Customer
        self.ids.customerAge.text = str(row[4])  # Age of Customer

    def delete(self):
        national_code = self.ids.customer_selector.text
        connection, cursor = None, None
        try:
            connection = get_connection()
            cursor = connection.cursor()
            sql_delete_query = """DELETE FROM customer
                                  WHERE national_code = %s"""
            cursor.execute(sql_delete_query, (national_code, ))
            connection.commit()
            count = cursor.rowcount
            print(count, "Record Deleted successfully ")

        except (Exception, psycopg2.Error) as error:
            if connection:
                print("Failed to update record into address table ", error)
        finally:
            # closing database connection.
            if connection:
                cursor.close()
                connection.close()


def show_delete_customer_popup():
    show = DeleteCustomerPopUp()
    popup_window = Popup(title="Delete Customer", content=show)
    show.ids['delete_customer_cancel'].bind(on_press=popup_window.dismiss)
    popup_window.open()


# ---------- Delete Address -------------
Builder.load_file('delete_address.kv')


class DeleteAddressPopUp(BoxLayout):

    def __int__(self):
        super(BoxLayout, self).__init__()
        self.address_list = []

    def pick_values(self):
        connection = get_connection()
        postgres_insert_query = "SELECT * FROM address"
        cursor = None
        try:
            cursor = connection.cursor()
            cursor.execute(postgres_insert_query)
            self.address_list = cursor.fetchall()
            address_id_list = []
            for row in self.address_list:
                address_id_list.append(row[0])

        except (Exception, psycopg2.Error) as error:
            if connection:
                print("Failed to fetch record into address table ", error)
        finally:
            # closing database connection.
            if connection:
                cursor.close()
                connection.close()
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
        cursor = None

        try:
            connection = get_connection()
            cursor = connection.cursor()
            sql_delete_query = """DELETE FROM address
                                  WHERE phone = %s"""
            cursor.execute(sql_delete_query, (phone, ))
            connection.commit()
            count = cursor.rowcount
            print(count, "Record Deleted successfully ")

        except (Exception, psycopg2.Error) as error:
            if connection:
                print("Failed to update record into address table ", error)
        finally:
            # closing database connection.
            if connection:
                cursor.close()
                connection.close()


def show_delete_address_popup():
    show = DeleteAddressPopUp()
    popup_window = Popup(title="Delete Address", content=show)
    show.ids['delete_address_cancel'].bind(on_press=popup_window.dismiss)
    popup_window.open()


# ---- Main Page -------- #
class MainLayout(BoxLayout):
    def order_food_button(self):
        show_food_order_popup()

    def order_raw_material_button(self):
        show_raw_material_order_popup()

# ------- Insertion ------
    def insert_customer_button(self):
        show_insert_customer_popup()

    def insert_biker_button(self):
        show_insert_biker_popup()

    def insert_address_button(self):
        show_insert_address_popup()

# ------- Update -------
    def update_customer_button(self):
        show_update_customer_popup()

    def update_address_button(self):
        show_update_address_popup()

# -------- Delete -------
    def delete_customer_button(self):
        show_delete_customer_popup()

    def delete_address_button(self):
        show_delete_address_popup()


class MainPage(App):
    def build(self):
        return MainLayout()


if __name__ == "__main__":
    MainPage().run()