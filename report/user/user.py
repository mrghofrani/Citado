from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.lang import Builder
from database import query

Builder.load_file('report/user/user.kv')


class UserReport(BoxLayout):
    def pick_customer(self):
        postgres_qeury = """SELECT * 
                            FROM customer"""
        self.customers = query(postgres_qeury, "customer")
        customers = []
        if self.customers:
            for row in self.customers:
                customers.append(str(row[0]))
        if customers:
            self.ids.customer_selector.text = customers[0]
        return customers

    def determine_favorite_food(self):
        customer = self.ids.customer_selector.text

        postgres_query = """SELECT sum(quantity), food_name 
                            FROM food_factor
                            WHERE factor_int IN (SELECT factor_id
                                                 FROM factor_customer
                                                 WHERE customer_national_code=%s)
                            GROUP BY food_name 
                            ORDER BY sum(quantity) DESC"""
        values = (customer,)
        self.favorite_food = query(postgres_query, "food_factor", values)
        print(self.favorite_food)
        if self.favorite_food:
            self.ids.favorite_food.text = str(self.favorite_food[0][1])
        else:
            self.ids.favorite_food.text = ""


def show_user_report_popup():
    show = UserReport()
    popup_window = Popup(title="User Report", content=show)
    show.ids.exit.bind(on_press=popup_window.dismiss)
    popup_window.open()