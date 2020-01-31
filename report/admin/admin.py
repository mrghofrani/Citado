from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.lang import Builder
from database import query, update

Builder.load_file('report/admin/admin.kv')


class AdminReport(BoxLayout):
    def pick_dates(self):
        postgres_qeury = """SELECT DISTINCT date
                            FROM factor_of_food 
                            UNION 
                            SELECT DISTINCT date
                            FROM factor_of_ingredient"""
        self.dates = query(postgres_qeury, "factor_of_food")
        dates = []
        if self.dates:
            for row in self.dates:
                dates.append(str(row[0]))
        if dates:
            self.ids.date_selector.text = dates[0]
        return dates

    def update(self):
        if self.ids.buy.state == "down":
            date = self.ids.date_selector.text
            postgres_query = """SELECT factor_int, food_name, price, quantity
                                FROM food_factor INNER JOIN food ON food_factor.food_name = food.name and food_factor.food_name_start_time = food.name_start_time and food_factor.food_price_start_time = food.price_start_time
                                WHERE factor_int
                                IN (SELECT id
                                    FROM factor_of_food
                                    WHERE date = %s)"""
            values = (date,)
            list_of_food = query(postgres_query, "food_factor", values)
            sum = 0
            for row in list_of_food:
                sum += row[2] * row[3]
            self.ids.result.text = str(list_of_food)
            self.ids.value.text = str(sum)
        elif self.ids.sold.state == "down":
            date = self.ids.date_selector.text
            postgres_query = """SELECT factor_id, ingredient_name, price, quantity
                                FROM ingredient INNER JOIN factor_ingredient fi on ingredient.name = fi.ingredient_name and ingredient.start_time = fi.ingredient_start_time
                                WHERE factor_id
                                IN (SELECT id
                                    FROM factor_of_ingredient
                                    WHERE date = %s)"""
            values = (date,)
            list_of_food = query(postgres_query, "ingredient_factor", values)
            sum = 0
            for row in list_of_food:
                sum += row[2] * row[3]
            self.ids.result.text = str(list_of_food)
            self.ids.value.text = str(sum)
        elif self.ids.total.state == "down":
            date = self.ids.date_selector.text
            postgres_query = """SELECT factor_int, food_name, price, quantity
                                           FROM food_factor INNER JOIN food ON food_factor.food_name = food.name and food_factor.food_name_start_time = food.name_start_time and food_factor.food_price_start_time = food.price_start_time
                                           WHERE factor_int
                                           IN (SELECT id
                                               FROM factor_of_food
                                               WHERE date = %s)"""
            values = (date,)
            list_of_food = query(postgres_query, "food_factor", values)
            food_sum = 0
            for row in list_of_food:
                food_sum += row[2] * row[3]

            postgres_query = """SELECT factor_id, ingredient_name, price, quantity
                                            FROM ingredient INNER JOIN factor_ingredient fi on ingredient.name = fi.ingredient_name and ingredient.start_time = fi.ingredient_start_time
                                            WHERE factor_id
                                            IN (SELECT id
                                                FROM factor_of_ingredient
                                                WHERE date = %s)"""
            values = (date,)
            list_of_ingredient = query(postgres_query, "ingredient_factor", values)
            ingredient_sum = 0
            for row in list_of_ingredient:
                ingredient_sum += row[2] * row[3]
                print(ingredient_sum)
            alist = list_of_ingredient + list_of_food
            self.ids.result.text = str(alist)
            print(food_sum - ingredient_sum)
            self.ids.value.text = str(food_sum - ingredient_sum)


def show_admin_report_popup():
    show = AdminReport()
    popup_window = Popup(title="Admin Report", content=show)
    show.ids.exit.bind(on_press=popup_window.dismiss)
    popup_window.open()