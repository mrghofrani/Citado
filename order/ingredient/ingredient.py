from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.lang import Builder
from database import insert, query, delete
from datetime import date

Builder.load_file('order/ingredient/ingredient.kv')


class IngredientOrderPopUp(BoxLayout):

    def pick_factor(self):
        postgres_query = """SELECT * FROM factor_of_ingredient"""
        factor_list = []
        self.factor_list = query(postgres_query, "factor_of_ingredient")
        for row in self.factor_list:
            factor_list.append(str(row[0]))
        return factor_list

    def new(self):
        postgres_insert_query = """INSERT INTO factor_of_ingredient(date) VALUES (%s)"""
        today = date.today()
        values = (today,)
        insert(postgres_insert_query, values, "factor_of_ingredient")
        self.ids.factor_selector.values = self.pick_factor()

    def ingredient_lister(self):
        store = self.ids.store_selector.text
        store_start_time = ""
        for row in self.store_list:
            if row[0] == store:
                store_start_time = row[1]
        postgres_query = """SELECT * 
                            FROM store_ingredient NATURAL JOIN ingredient
                            WHERE store_name = %s 
                            AND store_start_time = %s 
                            AND ingredient.start_time < current_date 
                            AND ingredient.end_time > current_date"""
        values = (store, store_start_time)
        self.ingredient_list = query(postgres_query, "store_ingredient", values=values)
        ingredient_list = []
        if self.ingredient_list:
            for row in self.ingredient_list:
                ingredient_list.append(row[2])
        self.ids.ingredient_selector.text = "choose"
        self.ids.ingredient_selector.values = ingredient_list


    def set_store(self):
        factor_id = self.ids.factor_selector.text
        store = self.ids.store_selector.text
        if store != "Not set":
            postgres_insert_query = """INSERT INTO store_factor(factor_id, store_name, store_start_time) VALUES (%s, %s, %s)
                                       ON CONFLICT (factor_id)
                                       DO UPDATE
                                       SET store_name = %s,
                                           store_start_time = %s
                                       WHERE store_factor.factor_id = %s"""
            store_start_time = None
            for row in self.store_list:
                if row[0] == store:
                    store_start_time = row[1]
            values = (factor_id, store, store_start_time, store, store_start_time, factor_id)
            insert(postgres_insert_query, values, "store_factor")
            self.ids.store_selector.disabled = True
            self.ingredient_lister()

    def enable_store_selector(self):
        self.ids.store_selector.disabled = False

    def store_lister(self):
        postgres_query = """SELECT * FROM store WHERE start_time < current_date AND current_date < end_time"""
        store_list = []
        self.store_list = query(postgres_query, "store")
        for row in self.store_list:
            store_list.append(str(row[0]))
        self.ids.store_selector.values = store_list

        factor_id = self.ids.factor_selector.text
        postgres_query = """SELECT * FROM store_factor WHERE factor_id = %s """
        values = (factor_id,)
        self.store_text = query(postgres_query, "store_factor", values=values)
        store_text = "Not set"
        if self.store_text:
            for val in self.store_text:
                store_text = str(val[1])
        self.ids.store_selector.text = store_text

    def enable_add(self):
        self.ids.ingredient_selector.disabled = False

    def add(self):
        factor_id = self.ids.factor_selector.text
        ingredient = self.ids.ingredient_selector.text
        ingredient_start_time = ""
        for row in self.ingredient_list:
            if row[2] == ingredient:
                ingredient_start_time = row[3]
        postgres_insert_query = """INSERT INTO factor_ingredient(factor_id, ingredient_name, ingredient_start_time)
                                           VALUES (%s, %s, %s) 
                                           ON CONFLICT (factor_id, ingredient_name, ingredient_start_time)
                                           DO UPDATE 
                                           SET ingredient_name = %s,
                                               ingredient_start_time = %s
                                           WHERE excluded.factor_id = %s"""
        values = (factor_id, ingredient, ingredient_start_time, ingredient, ingredient_start_time, factor_id)
        insert(postgres_insert_query, values, "factor_ingredient")
        self.ids.ingredient_selector.disabled = True

    def update_form(self):
        self.ids.store_selector.disabled = True
        self.store_lister()


def show_ingredient_order_popup():
    show = IngredientOrderPopUp()
    popup_window = Popup(title="Order Ingredient", content=show)
    show.ids.exit.bind(on_press=popup_window.dismiss)
    popup_window.open()
