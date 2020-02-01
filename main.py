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
from update.biker.biker import show_update_biker_popup
from update.food.food import show_update_food_popup

from delete.address.address import show_delete_address_popup
from delete.customer.customer import show_delete_customer_popup
from delete.biker.biker import show_delete_biker_popup
from delete.food.food import show_delete_food_popup
from delete.ingredient.ingredient import show_delete_ingredient_popup

from order.food.food import show_food_order_popup
from order.ingredient.ingredient import show_ingredient_order_popup

from report.admin.admin import show_admin_report_popup
from report.user.user import show_user_report_popup

from log.log import show_log_popup


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

    def update_biker_button(self):
        show_update_biker_popup()

    def update_food_button(self):
        show_update_food_popup()

# -------- Delete -------
    def delete_customer_button(self):
        show_delete_customer_popup()

    def delete_address_button(self):
        show_delete_address_popup()

    def delete_biker_button(self):
        show_delete_biker_popup()

    def delete_food_button(self):
        show_delete_food_popup()

    def delete_ingredient_button(self):
        show_delete_ingredient_popup()

# ---------- Report ----------
    def admin_report_button(self):
        show_admin_report_popup()

    def user_report_button(self):
        show_user_report_popup()

    def log_button(self):
        show_log_popup()
        

class MainPage(App):
    def build(self):
        return MainLayout()


if __name__ == "__main__":
    MainPage().run()