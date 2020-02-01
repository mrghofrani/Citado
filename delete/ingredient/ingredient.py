from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.lang import Builder
from database import query, update

Builder.load_file('delete/ingredient/ingredient.kv')


class DeleteIngredientPopUp(BoxLayout):
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
        if ingredient != "Choose A Food":
            selected_row = tuple()
            for row in self.ingredient_list:
                if row[0] == ingredient:
                    selected_row = row
            self.ids.price.text = str(selected_row[1])
            self.ids.start_time.text = str(selected_row[2])
            self.ids.end_time.text = str(selected_row[3])
            self.ids.delete.disabled = False

    def delete(self):
        name = self.ids.ingredient_selector.text
        start_time = self.ids.start_time.text
        postgres_delete_query = """UPDATE ingredient
                                   SET end_time = current_date
                                    WHERE name = %s
                                    AND start_time = %s"""
        values = (name, start_time)
        update(postgres_delete_query, values, "ingredient")
        self.ids.ingredient_selector.values = self.pick_values()


def show_delete_ingredient_popup():
    show = DeleteIngredientPopUp()
    popup_window = Popup(title="Delete Ingredient", content=show)
    show.ids.cancel.bind(on_press=popup_window.dismiss)
    popup_window.open()
