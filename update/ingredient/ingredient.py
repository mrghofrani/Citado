from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.lang import Builder
from database import query, update

Builder.load_file('update/ingredient/ingredient.kv')


class UpdateIngredientPopUp(BoxLayout):
    def update_ingredient_selector(self):
        self.ids.ingredient_selector.values = self.pick_values()

    def pick_values(self):
        postgres_query = """SELECT * FROM ingredient  
                            WHERE start_time < current_date AND end_time > current_date"""
        self.ingredient_list = query(postgres_query, "ingredient")
        ingredient_list = []
        if self.ingredient_list:
            for row in self.ingredient_list:
                ingredient_list.append(row[0])
        return ingredient_list

    def update_form(self):
        ingredient = self.ids.ingredient_selector.text
        print(ingredient)
        if ingredient != "Choose An Ingredient":
            selected_row = tuple()
            for row in self.ingredient_list:
                if row[0] == ingredient:
                    selected_row = row
            self.ids.price.text = str(selected_row[1])
            self.ids.update_btn.disabled = False

    def update(self):
        name = self.ids.ingredient_selector.text
        price = self.ids.price.text
        start_time = ""
        for row in self.ingredient_list:
            if name == row[0]:
                start_time = row[2]
        postgres_delete_query = """UPDATE ingredient
                                   SET price = %s
                                   WHERE name = %s
                                   AND start_time = %s"""
        values = (price, name, start_time)
        update(postgres_delete_query, values, "ingredient")


def show_update_ingredient_popup():
    show = UpdateIngredientPopUp()
    popup_window = Popup(title="Update Ingredient", content=show)
    show.ids.cancel.bind(on_press=popup_window.dismiss)
    popup_window.open()
