from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.lang import Builder
from database import insert, query, delete
from datetime import date

Builder.load_file('order/food/food.kv')


class FoodOrderPopUp(BoxLayout):

    def __init__(self):
        super().__init__()
        self.factor_list = []
        self.customer_list = []
        self.address_list = []
        self.biker_list = []
        self.customer_set = False
        self.customer = "unregistered user"

    def pick_factor(self):
        postgres_query = """SELECT * FROM factor_of_food"""
        factor_id_list = []
        self.factor_list = query(postgres_query, "factor")
        for row in self.factor_list:
            factor_id_list.append(str(row[0]))
        return factor_id_list

    def new(self):
        today = date.today()
        postgres_insert_query = """INSERT INTO factor_of_food(date)
                                   VALUES (%s) RETURNING  id"""
        values = (today,)
        new_factor_id = insert(postgres_insert_query, values, "factor")
        self.ids.factor_id_selector.values = self.pick_factor()

    def pick_food(self):
        postgres_query = """SELECT * FROM food WHERE name_start_time < current_date AND current_date < name_end_time
                                               AND  price_start_time < current_date AND current_date < price_end_time"""
        food_list = []
        self.food_list = query(postgres_query, "food")
        for row in self.food_list:
            food_list.append(row[0])
        return food_list

    def customer_lister(self):
        factor_id = self.ids.factor_id_selector.text
        postgres_query = f"""SELECT * FROM factor_customer"""
        customer_query = query(postgres_query, "factor_customer")
        self.ids.customer_selector.text = "unregistered user"
        for row in customer_query:
            if row[0] == int(factor_id):
                self.ids.customer_selector.text = str(row[1])
                self.customer = str(row[1])

        postgres_query = f"""SELECT * FROM customer"""
        self.customer_list = query(postgres_query, "customer")
        # self.customer_list.append("unregistered user")
        customer_list = ["unregistered user"]
        for row in self.customer_list:
            customer_list.append(str(row[0]))
        self.ids.customer_selector.values = customer_list

    def enable_customer_selector(self):
        self.ids.customer_selector.disabled = False

    def set_factor_customer(self):
        factor_id = self.ids.factor_id_selector.text
        customer = self.ids.customer_selector.text
        if customer == "unregistered user":
            postgres_insert_query = """DELETE FROM factor_customer
                                       WHERE factor_customer.factor_id = %s"""
            values = (factor_id)
            delete(postgres_insert_query, values, "factor_customer")
        else:
            postgres_insert_query = """INSERT INTO factor_customer(factor_id, customer_national_code) VALUES (%s, %s)
                                       ON CONFLICT (factor_id)
                                       DO UPDATE 
                                       SET customer_national_code = %s
                                       WHERE factor_customer.factor_id = %s"""
            values = (factor_id, customer, customer, factor_id)
            insert(postgres_insert_query, values, "factor_customer")
        self.address_lister()
        self.ids.customer_selector.disabled = True

    def enable_proper(self):
        address = self.ids.address_selector.text
        if address != "Restaurant":
            self.ids.biker_selector.disabled = False
            self.ids.set_biker.disabled = False
        else:
            self.ids.biker_selector.disabled = True
            self.ids.set_biker.disabled = True

    def address_lister(self):
        factor_id = self.ids.factor_id_selector.text
        customer = self.ids.customer_selector.text
        print(customer)
        if customer != "unregistered user":
            self.ids.address_selector.disabled = False
            postgres_query = f"""SELECT * FROM factor_address WHERE factor_id=%s"""
            values = (factor_id,)
            self.address_list = query(postgres_query, "factor_address", values)
            if self.address_list:
                address = self.address_list[0][1]
            else:
                address = "Restaurant"
        else:
            address = "Restaurant"
        self.address = address
        self.ids.address_selector.text = str(address)

        address_list = ["Restaurant"]
        postgres_query = f"""SELECT * FROM address WHERE customer = %s"""
        values = (customer,)
        address_query = query(postgres_query, "address", values)
        if address_query:
            for row in address_query:
                address_list.append(str(row[0]))
        self.ids.address_selector.values = address_list

    def set_factor_address(self):
        factor_id = self.ids.factor_id_selector.text
        address = self.ids.address_selector.text
        customer = self.ids.customer_selector.text
        if customer != "unregistered user":
            if address == "Restaurant":
                postgres_delete_query = """DELETE FROM factor_address
                                           WHERE factor_id = %s"""
                values = (factor_id,)
                delete(postgres_delete_query, values, "factor_address")
                self.address = address

                postgres_delete_query = """DELETE FROM delivery
                                            WHERE  factor_id= %s"""
                values = (factor_id,)
                delete(postgres_delete_query, values, "delivery")
                self.ids.biker_selector.disabled = True
                self.ids.set_biker.disabled = True
            else:
                postgres_insert_query = """INSERT INTO factor_address(factor_id, address_phone) 
                                            VALUES (%s, %s) ON CONFLICT (factor_id) 
                                            DO UPDATE 
                                            SET address_phone = %s 
                                            WHERE factor_address.factor_id = %s"""
                values = (factor_id, address, address, factor_id)
                insert(postgres_insert_query, values, "factor_customer")
                self.ids.biker_selector.disabled = False
                self.ids.set_biker.disabled = False
            self.address = address
        else:
            self.address = "Restaurant"

    def biker_lister(self):
        factor_id = self.ids.factor_id_selector.text
        if self.customer != "unregistered user":
            postgres_query = f"""SELECT * FROM delivery WHERE factor_id={factor_id}"""
            biker_query = query(postgres_query, "delivery")
            if biker_query:
                biker = str(biker_query[0][0])
            else:
                biker = "None"
        else:
            biker = "None"
        self.ids.biker_selector.text = biker

        postgres_query = """SELECT * FROM bike"""
        self.biker_list = query(postgres_query, "biker")
        biker_list = []
        if self.biker_list:
            for row in self.biker_list:
                biker_list.append(str(row[0]))
        self.ids.biker_selector.values = biker_list

    def set_factor_biker(self):
        factor_id = self.ids.factor_id_selector.text
        customer = self.ids.customer_selector.text
        address = self.ids.customer_selector.text
        biker = self.ids.biker_selector.text
        print(self.address)
        if customer != "unregistered user" and address != "Restaurant" and self.address != "Restaurant":
            postgres_insert_query = """INSERT INTO delivery(factor_id, address_phone, bike_delivery_national_code)
                                           VALUES (%s, %s, %s) ON CONFLICT (factor_id)
                                           DO UPDATE 
                                           SET address_phone = %s, bike_delivery_national_code = %s"""
            values = (factor_id, self.address, biker, self.address, biker)
            print(values)
            insert(postgres_insert_query, values, "delivery")

    def update_form(self):
        self.ids.set_address.disabled = False
        self.customer_lister()

    def add(self):
        factor_id = self.ids.factor_id_selector.text
        food = self.ids.food_selector.text

        postgres_insert_query = """INSERT INTO food_factor(factor_int, food_name, food_name_start_time, food_price_start_time, quantity)
                                    VALUES (%s, %s, %s, %s, 1) 
                                    ON CONFLICT (factor_int, food_name, food_name_start_time)
                                    DO UPDATE 
                                    SET quantity = food_factor.quantity + 1
                                    WHERE excluded.factor_int = %s"""
        food_name_start_time = None
        food_price_start_time = None
        for f in self.food_list:
            if f[0] == food:
                food_name_start_time = f[2]  # food name start time index
                food_price_start_time = f[4]
                break
        values = (factor_id, food, food_name_start_time, food_price_start_time, factor_id)
        insert(postgres_insert_query, values, "food_fact")


def show_food_order_popup():
    show = FoodOrderPopUp()
    popup_window = Popup(title="Order Food", content=show)
    show.ids.exit.bind(on_press=popup_window.dismiss)
    popup_window.open()