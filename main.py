import psycopg2

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.lang import Builder
from datetime import date


def get_connection():
    return psycopg2.connect(user="engmrgh", password="h3ll9db", host="localhost", port="5432", database="citado")

# ----------------------------- #
#          Order Part           #
# ----------------------------- #


# ---------- Food Order ---------- #
Builder.load_file('order/food.kv')


class FoodOrderPopUp(BoxLayout):

    def __init__(self):
        super().__init__()
        self.factor_list = []
        self.food_list = []
        self.customer_list = []
        self.address_list = []
        self.biker_list = []

    def pick_customer(self):
        factor_id = self.ids.factor_id_selector.text
        try:
            factor_id = int(factor_id)
        except:
            return ['Set customer']
        if self.disable_list[factor_id]:
            postgres_query = f"""SELECT * FROM factor_customer WHERE factor_id={factor_id}"""
            customer_list = []
            connection, cursor = None, None
            try:
                connection = get_connection()
                cursor = connection.cursor()
                cursor.execute(postgres_query)
                self.customer_list = cursor.fetchall()
                if self.customer_list:
                    for row in self.customer_list:
                        customer_list.append(str(row[0]))
                    print(customer_list)
                    print(self.customer_list)
                    self.ids.customer_selector.text = self.customer_list[0][1]
                    self.ids.customer_selector.disabled = True

            except (Exception, psycopg2.Error) as error:
                if connection:
                    print("Failed to fetch record from factor_customer table ", error)
            finally:
                # closing database connection.
                if connection:
                    cursor.close()
                    connection.close()
        else:
            postgres_query = """SELECT * FROM customer"""
            customer_list = []
            connection, cursor = None, None
            try:
                connection = get_connection()
                cursor = connection.cursor()
                cursor.execute(postgres_query)
                self.customer_list = cursor.fetchall()
                for row in self.customer_list:
                    customer_list.append(row[0])
                customer_list.append("Unknown")
                self.ids.customer_selector.values = customer_list
                self.ids.customer_selector.disabled = False

            except (Exception, psycopg2.Error) as error:
                if connection:
                    print("Failed to fetch record from customer table ", error)
            finally:
                # closing database connection.
                if connection:
                    cursor.close()
                    connection.close()

    def pick_factor(self):
        postgres_query = """SELECT * FROM factor"""
        factor_id_list = []
        connection, cursor = None, None
        try:
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute(postgres_query)
            self.factor_list = cursor.fetchall()
            self.disable_list = dict()
            for row in self.factor_list:
                factor_id_list.append(str(row[0]))
                self.disable_list[row[0]] = True

        except (Exception, psycopg2.Error) as error:
            if connection:
                print("Failed to fetch record into food order table ", error)
        finally:
            # closing database connection.
            if connection:
                cursor.close()
                connection.close()
        return factor_id_list

    def pick_food(self):
        postgres_query = """SELECT * FROM food WHERE name_start_time < current_date AND current_date < name_end_time
                                            AND  price_start_time < current_date AND current_date < price_end_time"""
        food_list = []
        connection, cursor = None, None
        try:
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute(postgres_query)
            self.food_list = cursor.fetchall()
            for row in self.food_list:
                food_list.append(row[0])
        except (Exception, psycopg2.Error) as error:
            if connection:
                print("Failed to fetch record into food order table ", error)
        finally:
            # closing database connection.
            if connection:
                cursor.close()
                connection.close()
        return food_list

    def pick_address(self):
        customer = self.ids.customer_selector.text
        if customer:
            postgres_query = f"""SELECT * FROM customer JOIN address WHERE national_code = {customer}"""
            address_list = []
            connection, cursor = None, None
            try:
                connection = get_connection()
                cursor = connection.cursor()
                cursor.execute(postgres_query)
                self.address_list = cursor.fetchall()
                for row in self.address_list:
                    address_list.append(row[0])
                address_list.append("Restaurant")
            except (Exception, psycopg2.Error) as error:
                if connection:
                    print("Failed to fetch record into food order table ", error)
            finally:
                # closing database connection.
                if connection:
                    cursor.close()
                    connection.close()
            return address_list
        return ['Choose a customer']

    def pick_biker(self):
        postgres_query = """SELECT * FROM biker"""
        biker_list = []
        connection, cursor = None, None
        try:
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute(postgres_query)
            self.biker_list = cursor.fetchall()
            for row in self.biker_list:
                biker_list.append(row[0])

        except (Exception, psycopg2.Error) as error:
            if connection:
                print("Failed to fetch record into food order table ", error)
        finally:
            # closing database connection.
            if connection:
                cursor.close()
                connection.close()
        return biker_list

    def new(self):
        today = date.today()
        postgres_insert_query = """INSERT INTO factor(date)
                                   VALUES (%s) RETURNING  id"""
        values = (today,)
        connection, cursor = None, None
        try:
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute(postgres_insert_query, values)
            new_factor_id = cursor.fetchone()[0]
            connection.commit()
            count = cursor.rowcount
            print(count, "Record inserted successfully into factor table")
            print(f"new_factor id {new_factor_id}")
            self.ids.factor_id_selector.values = self.pick_factor()
            self.disable_list[new_factor_id] = False
        except (Exception, psycopg2.Error) as error:
            if connection:
                print("Failed to insert record into factor table", error)
        finally:
            # closing database connection.
            if connection:
                cursor.close()
                connection.close()

    def set_customer(self):
        factor_id = self.ids.factor_id_selector.text
        customer = self.ids.customer_selector.text
        postgres_insert_query = """INSERT INTO factor_customer(factor_id, customer_national_code) VALUES (%s, %s)"""
        values = (factor_id, customer)
        connection, cursor = None, None
        if customer != "Unknown":
            try:
                connection = get_connection()
                cursor = connection.cursor()
                cursor.execute(postgres_insert_query, values)
                connection.commit()
                count = cursor.rowcount
                print(count, "Record inserted successfully into factor_customer table")

            except (Exception, psycopg2.Error) as error:
                if connection:
                    print("Failed to insert record into factor_customer table", error)
            finally:
                # closing database connection.
                if connection:
                    cursor.close()
                    connection.close()
        self.ids.customer_selector.disabled = True

    def submit(self):
        factor_id = self.ids.factor_id_selector.text
        food = self.ids.food_selector.text
        customer = self.ids.customer_selector.text
        address = self.ids.address_selector.text
        biker = self.ids.biker_selector.text

        connection, cursor = None, None
        postgres_insert_query = """ INSERT INTO food_fact(factor_int, food_name, food_name_start_time, food_price_start_time)
                                           VALUES (%s, %s, %s, %s) """
        food_start_time = None
        for f in self.food_list:
            if f[0] == food:
                food_start_time = f[2] # food name start time index
        values = (factor_id, food, food_start_time, )
        try:
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute(postgres_insert_query, values)

            connection.commit()
            count = cursor.rowcount
            print(count, "Record inserted successfully into factor table")

        except (Exception, psycopg2.Error) as error:
            if connection:
                print("Failed to insert record into factor table", error)
        finally:
            # closing database connection.
            if connection:
                cursor.close()
                connection.close()


def show_food_order_popup():
    show = FoodOrderPopUp()
    popup_window = Popup(title="Order Food", content=show)
    show.ids['cancel'].bind(on_press=popup_window.dismiss)
    popup_window.open()


# ---- Raw Material Order -----#
class RawMaterialOrderPopUp(BoxLayout):
    pass


def show_raw_material_order_popup():
    show = RawMaterialOrderPopUp()
    popup_window = Popup(title="Order Raw Material", content=show)
    show.ids['raw_material_order_cancel'].bind(on_press=popup_window.dismiss)
    popup_window.open()


# ----------------------------- #
#          Insert Part          #
# ----------------------------- #

# ------ Insert Customer ------ #
Builder.load_file('Insert/customer.kv')


class InsertCustomerPopUp(BoxLayout):
    def submit(self):
        national_code = self.ids.customerNationalCodeInput.text
        first_name = self.ids.customerFirstName.text
        last_name = self.ids.customerLastName.text
        mobile_number = self.ids.customerMobileNumber.text
        age = self.ids.customerAge.text
        postgres_insert_query = " INSERT INTO customer(national_code, first_name, last_name, mobile_number, age) " \
                                " VALUES (%s, %s, %s, %s, %s) "
        values = (national_code, first_name, last_name, mobile_number, age)
        connection, cursor = None, None
        try:
            connection = get_connection()
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
Builder.load_file('Insert/biker.kv')


class InsertBikerPopUp(BoxLayout):
    def submit(self):
        national_code = self.ids.bikerNationalCodeInput.text
        first_name = self.ids.bikerFirstName.text
        last_name = self.ids.bikerLastName.text
        mobile_number = self.ids.bikerMobileNumber.text
        connection = get_connection()
        postgres_insert_query = " INSERT INTO biker(national_code, first_name, last_name, mobile_number) " \
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
Builder.load_file('Insert/address.kv')


class InsertAddressPopUp(BoxLayout):
    def submit(self):
        phone_number = self.ids.addressPhoneNumber.text
        name = self.ids.addressName.text
        address = self.ids.addressAddress.text

        postgres_insert_query = " INSERT INTO address(phone, name, address) VALUES (%s,%s,%s) "
        values = (phone_number, name, address)

        connection, cursor = None, None
        try:
            connection = get_connection()
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


# ----------    Insert Food    ----------
Builder.load_file('Insert/food.kv')


class InsertFoodPopUp(BoxLayout):
    def submit(self):
        name = self.ids.name.text
        name_start_time = self.ids.food_start_time.text
        name_end_time = self.ids.food_end_time.text
        price = self.ids.price.text
        price_start_time = self.ids.price_start_time.text
        price_end_time = self.ids.price_end_time.text

        postgres_insert_query = """ INSERT INTO food(name, price, name_start_time, name_end_time, price_start_time, price_end_time)
                                    VALUES (%s, %s, %s, %s, %s, %s) """

        values = (name, price, name_start_time, name_end_time, price_start_time, price_end_time)
        connection, cursor = None, None
        try:
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute(postgres_insert_query, values)

            connection.commit()
            count = cursor.rowcount
            print(count, "Record inserted successfully into food table")

        except (Exception, psycopg2.Error) as error:
            if connection:
                print("Failed to insert record into food table", error)
        finally:
            # closing database connection.
            if connection:
                cursor.close()
                connection.close()


def show_insert_food_popup():
    show = InsertFoodPopUp()
    popup_window = Popup(title="Insert food", content=show)
    show.ids['insert_food_cancel'].bind(on_press=popup_window.dismiss)
    popup_window.open()


# ----------    Insert Store    ----------
Builder.load_file('Insert/store.kv')


class InsertStorePopUp(BoxLayout):
    def submit(self):
        name = self.ids.name.text
        start_time = self.ids.start_time.text
        end_time = self.ids.end_time.text

        postgres_insert_query = """ INSERT INTO store(name, start_time, end_time)
                                    VALUES (%s, %s, %s) """

        values = (name, start_time, end_time)
        connection, cursor = None, None
        try:
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute(postgres_insert_query, values)

            connection.commit()
            count = cursor.rowcount
            print(count, "Record inserted successfully into food table")

        except (Exception, psycopg2.Error) as error:
            if connection:
                print("Failed to insert record into food table", error)
        finally:
            # closing database connection.
            if connection:
                cursor.close()
                connection.close()


def show_insert_store_popup():
    show = InsertStorePopUp()
    popup_window = Popup(title="Insert store", content=show)
    show.ids['insert_store_cancel'].bind(on_press=popup_window.dismiss)
    popup_window.open()

# ------------------------------ #
#         Update Part            #
# -------------------------------#

# ------ update Customer --------

Builder.load_file('update/customer.kv')


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
Builder.load_file('update/address.kv')


class UpdateAddressPopUp(BoxLayout):

    def __int__(self):
        super(BoxLayout, self).__init__()
        self.address_list = []

    def pick_values(self):
        address_id_list = []
        connection, cursor = None, None
        try:
            connection = get_connection()
            cursor = connection.cursor()
            postgres_query = "SELECT * FROM address"
            cursor.execute(postgres_query)
            self.address_list = cursor.fetchall()
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
Builder.load_file('delete/customer.kv')


class DeleteCustomerPopUp(BoxLayout):

    def __int__(self):
        super(BoxLayout, self).__init__()
        self.customer_list = []

    def pick_values(self):
        connection = get_connection()
        postgres_insert_query = "SELECT * FROM customer"
        connection, cursor = None, None
        customer_id_list = []
        try:
            cursor = connection.cursor()
            cursor.execute(postgres_insert_query)
            self.customer_list = cursor.fetchall()
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
Builder.load_file('delete/address.kv')


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

# ------- Insert ------
    def insert_customer_button(self):
        show_insert_customer_popup()

    def insert_biker_button(self):
        show_insert_biker_popup()

    def insert_address_button(self):
        show_insert_address_popup()

    def insert_food_button(self):
        show_insert_food_popup()

    def insert_store_button(self):
        show_insert_store_popup()

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