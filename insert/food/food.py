from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.lang import Builder
from database import insert

Builder.load_file('insert/food/food.kv')


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

        insert(postgres_insert_query, values, "food")


def show_insert_food_popup():
    show = InsertFoodPopUp()
    popup_window = Popup(title="Insert food", content=show)
    show.ids.cancel.bind(on_press=popup_window.dismiss)
    popup_window.open()