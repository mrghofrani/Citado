from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.lang import Builder
from database import query, update

Builder.load_file('delete/ingredient/ingredient.kv')


class DeleteIngredientPopUp(BoxLayout):
    def update_ingredient_selector(self):
        self.ids.ingredient_selector.values = self.pick_values()

    def pick_values(self):
        postgres_query = """SELECT * FROM ingredient NATURAL JOIN store_ingredient 
                            WHERE ingredient.start_time < current_date AND ingredient.end_time > current_date"""
        self.food_list = query(postgres_query, "food")
        food_list = []
        if self.food_list:
            for row in self.food_list:
                food_list.append(row[0])
        return food_list

    def update_form(self):
        food = self.ids.food_selector.text
        if food != "Choose A Food":
            selected_row = tuple()
            for row in self.food_list:
                if row[0] == food:
                    selected_row = row
            self.ids.price.text = str(selected_row[1])
            self.ids.name_start_time.text = str(selected_row[2])
            self.ids.name_end_time.text = str(selected_row[3])
            self.ids.price_start_time.text = str(selected_row[4])
            self.ids.price_end_time.text = str(selected_row[5])
            self.ids.delete.disabled = False

    def delete(self):
        name = self.ids.food_selector.text
        name_start_time = self.ids.name_start_time.text
        price_start_time = self.ids.price_start_time.text
        postgres_delete_query = """UPDATE food
                                   SET name_end_time = current_date,
                                       price_end_time = current_date
                                    WHERE name = %s 
                                    AND name_start_time = %s 
                                    AND price_start_time = %s"""
        values = (name, name_start_time, price_start_time)
        update(postgres_delete_query, values, "food")
        self.ids.food_selector.values = self.pick_values()


def show_delete_food_popup():
    show = DeleteFoodPopUp()
    popup_window = Popup(title="Delete Food", content=show)
    show.ids.cancel.bind(on_press=popup_window.dismiss)
    popup_window.open()
