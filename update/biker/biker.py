from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.lang import Builder
from database import update, query

Builder.load_file('update/biker/biker.kv')


class UpdateBikerPopUp(BoxLayout):
    def pick_values(self):
        postgres_query = "SELECT * FROM bike"
        self.biker_list = query(postgres_query, "bike")
        biker_list = []
        for row in self.biker_list:
            biker_list.append(row[0])
        return biker_list

    def update_form(self):
        if self.biker_list:
            national_code = self.ids.biker_selector.text
            selected_row = tuple()
            for row in self.biker_list:
                if int(row[0]) == int(national_code):
                    selected_row = row
            self.ids.first_name.text = selected_row[1]
            self.ids.last_name.text = selected_row[2]
            self.ids.mobile_number.text = selected_row[3]
            self.ids.submit.disabled = False

    def submit(self):
        national_code = self.ids.biker_selector.text
        first_name = self.ids.first_name.text
        last_name = self.ids.last_name.text
        mobile_number = self.ids.mobile_number.text

        postgres_update_query = """UPDATE bike
                              SET first_name = %s, last_name = %s, mobile_number = %s
                              WHERE national_code = %s"""
        values = (first_name, last_name, mobile_number, national_code)
        update(postgres_update_query, values, "address")


def show_update_biker_popup():
    show = UpdateBikerPopUp()
    popup_window = Popup(title="Update Biker", content=show)
    show.ids.cancel.bind(on_press=popup_window.dismiss)
    popup_window.open()
