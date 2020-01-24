from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup


class MainLayout(BoxLayout):
    def order_food_button(self):
        show_food_order_popup()

    def order_raw_material_button(self):
        show_raw_material_order_popup()


class FoodOrderPopUp(BoxLayout):
    pass


class RawMaterialOrderPopUp(BoxLayout):
    pass


class MainPage(App):
    def build(self):
        return MainLayout()


def show_food_order_popup():
    show = FoodOrderPopUp()
    popup_window = Popup(title="Order Food", content=show)
    show.ids['food_order_cancel'].bind(on_press=popup_window.dismiss)
    popup_window.open()


def show_raw_material_order_popup():
    show = RawMaterialOrderPopUp()
    popup_window = Popup(title="Order Raw Material", content=show)
    show.ids['raw_material_order_cancel'].bind(on_press=popup_window.dismiss)
    popup_window.open()


if __name__ == "__main__":
    MainPage().run()