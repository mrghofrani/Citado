from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.lang import Builder
from database import insert, query

Builder.load_file('insert/ingredient/ingredient.kv')


class InsertIngredientPopUp(BoxLayout):
    def enable_submit(self):
        self.ids.submit.disabled = False

    def submit(self):
        name = self.ids.name.text
        price = self.ids.price.text
        price_start_time = self.ids.price_start_time.text
        price_end_time = self.ids.price_end_time.text
        store = self.ids.store_selector.text
        if store:
            postgres_insert_query = """ INSERT INTO ingredient(name, price, start_time, end_time)
                                                    VALUES (%s, %s, %s, %s) """
            values = (name, price, price_start_time, price_end_time)
            insert(postgres_insert_query, values, "ingredient")

            store_start_time = ""
            for row in self.store_list:
                if row[0] == store:
                    store_start_time = row[1]
                    break
            postgres_insert_query = """INSERT INTO store_ingredient(store_name, store_start_time, ingredient_name, ingredient_start_time) 
                                       VALUES  (%s, %s, %s,%s)
                                       ON CONFLICT DO NOTHING """
            values = (store, store_start_time, name, price_start_time)
            insert(postgres_insert_query, values, "store_ingredient")

    def store_lister(self):
        postgres_query = """SELECT * 
                            FROM store 
                            WHERE start_time < current_date 
                            AND   end_time > current_date"""
        self.store_list = query(postgres_query, "store")
        store_list = []
        if self.store_list:
            for row in self.store_list:
                store_list.append(row[0])
        return store_list


def show_insert_ingredient_popup():
    show = InsertIngredientPopUp()
    popup_window = Popup(title="Insert ingredient", content=show)
    show.ids.cancel.bind(on_press=popup_window.dismiss)
    popup_window.open()