from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.lang import Builder
from database import insert, update, delete, query
from datetime import date

Builder.load_file('order/food/food.kv')


class FoodOrderPopUp(BoxLayout):

    def __init__(self):
        super().__init__()
        self.factor_list = []
        self.food_list = []
        self.customer_list = []
        self.address_list = []
        self.biker_list = []
        self.customer_set = False

    def pick_factor(self):
        postgres_query = """SELECT * FROM factor"""
        factor_id_list = []
        self.factor_list = query(postgres_query, "factor")
        self.disable_list = dict()
        for row in self.factor_list:
            factor_id_list.append(str(row[0]))
            self.disable_list[row[0]] = True

        return factor_id_list

    def new(self):
        today = date.today()
        postgres_insert_query = """INSERT INTO factor(date)
                                   VALUES (%s) RETURNING  id"""
        values = (today,)
        new_factor_id = insert(postgres_insert_query, values, "factor")
        self.ids.factor_id_selector.values = self.pick_factor()
        self.disable_list[new_factor_id] = False

    def pick_food(self):
        postgres_query = """SELECT * FROM food WHERE name_start_time < current_date AND current_date < name_end_time
                                               AND  price_start_time < current_date AND current_date < price_end_time"""
        food_list = []
        self.food_list = query(postgres_query, "food")
        for row in self.food_list:
            food_list.append(row[0])
        return food_list

    def set_customer(self):
        factor_id = self.ids.factor_id_selector.text
        factor_id = int(factor_id)
        postgres_query = f"""SELECT * FROM factor_customer WHERE factor_id={factor_id}"""
        self.customer_list = query(postgres_query, "factor_customer")
        if self.customer_list:
            customer = self.customer_list[0][0]
        else:
            customer = "unregistered user"
        self.ids.customer_selector.text = str(customer)

    def set_address(self):
        factor_id = self.ids.factor_id_selector.text
        customer = self.ids.customer_selector.text
        if customer != "unregistered user":
            postgres_query = f"""SELECT * FROM factor_address WHERE factor_id={factor_id}"""
            self.address_list = query(postgres_query, "factor_address")
            if self.address_list:
                address = self.address_list[0][1]
            else:
                address = "Restaurant"
        else:
            address = "Restaurant"
        self.ids.address_selector.text = str(address)

    def set_biker(self):
        factor_id = self.ids.factor_id_selector.text
        customer = self.ids.customer_selector.text
        if customer != "unregistered user":
            postgres_query = f"""SELECT * FROM delivery WHERE factor_id={factor_id}"""
            self.biker_list = query(postgres_query, "delivery")
            if self.biker_list:
                biker = str(self.biker_list[0][0])
            else:
                biker = "None"
        else:
            biker = "None"
        self.ids.biker_selector.text = biker

    def update_form(self):
        factor_id = self.ids.factor_id_selector.text
        factor_id = int(factor_id)
        if self.disable_list[factor_id]:
            self.set_customer()
            self.set_address()
            self.set_biker()
        else:
            self.populate_customer()

    def set_food_customer(self):
        factor_id = self.ids.factor_id_selector.text
        factor_id = int(factor_id)
        customer = self.ids.customer_selector.text
        postgres_insert_query = """INSERT INTO factor_customer(factor_id, customer_national_code) VALUES (%s, %s)"""
        values = (factor_id, customer)
        if customer != "unregistered user":
            insert(postgres_insert_query, values, "factor_customer")
        self.customer_set = True
        self.disable_list[factor_id] = True
        self.ids.customer_selector.disabled = True
        self.ids.set_customer.disabled = True

    def submit(self):
        factor_id = self.ids.factor_id_selector.text
        food = self.ids.food_selector.text
        customer = self.ids.customer_selector.text
        address = self.ids.address_selector.text
        biker = self.ids.biker_selector.text

        postgres_insert_query = """ INSERT INTO food_fact(factor_int, food_name, food_name_start_time, food_price_start_time)
                                           VALUES (%s, %s, %s, %s) """
        food_start_time = None
        for f in self.food_list:
            if f[0] == food:
                food_start_time = f[2] # food name start time index
        values = (factor_id, food, food_start_time, )
        insert(postgres_insert_query, values, "food_fact")


def show_food_order_popup():
    show = FoodOrderPopUp()
    popup_window = Popup(title="Order Food", content=show)
    show.ids.cancel.bind(on_press=popup_window.dismiss)
    popup_window.open()