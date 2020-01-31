from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

from insert.address.address import *
from insert.customer.customer import show_insert_customer_popup
from insert.biker.biker import show_insert_biker_popup
from insert.food.food import show_insert_food_popup
from insert.store.store import show_insert_store_popup
from insert.ingredient.ingredient import show_insert_ingredient_popup

from update.customer.customer import show_update_customer_popup
from update.address.address import show_update_address_popup

from delete.address.address import show_delete_address_popup
from delete.customer.customer import show_delete_customer_popup

from order.food.food import show_food_order_popup
from order.ingredient.ingredient import show_ingredient_order_popup


class MainLayout(BoxLayout):
    def order_food_button(self):
        show_food_order_popup()

    def order_ingredient_button(self):
        show_ingredient_order_popup()

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

    def insert_ingredient_button(self):
        show_insert_ingredient_popup()

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