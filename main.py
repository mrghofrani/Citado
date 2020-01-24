from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup


class MainLayout(BoxLayout):
    def btn(self):
        show_order_popup()


class OrderPopUp(BoxLayout):
    pass


class MainPage(App):
    def build(self):
        return MainLayout()


def show_order_popup():
    show = OrderPopUp()
    popup_window = Popup(title="Order Food", content=show)
    if show is None:
        print("yes")
    show.ids['order_cancel'].bind(on_press=popup_window.dismiss)
    popup_window.open()


if __name__ == "__main__":
    MainPage().run()