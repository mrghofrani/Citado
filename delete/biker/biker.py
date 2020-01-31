from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.lang import Builder
from database import query, delete

Builder.load_file('delete/biker/biker.kv')


class DeleteBikerPopUp(BoxLayout):

    def update_biker_selector(self):
        self.ids.biker_selector.values = self.pick_values()


    def pick_values(self):
        postgres_query = "SELECT * FROM bike"
        self.biker_list = query(postgres_query, "bike")
        biker_list = []
        for row in self.biker_list:
            biker_list.append(row[0])
        return biker_list

    def update_form(self):
        national_code = self.ids.biker_selector.text
        if national_code != "Choose A Biker":
            selected_row = tuple()
            for row in self.biker_list:
                if int(row[0]) == int(national_code):
                    selected_row = row
            self.ids.first_name.text = selected_row[1]
            self.ids.last_name.text = selected_row[2]
            self.ids.mobile_number.text = selected_row[3]
            self.ids.delete.disabled = False

    def delete(self):
        national_code = self.ids.biker_selector.text
        postgres_delete_query = """DELETE FROM bike
                                   WHERE national_code = %s"""
        values = (national_code, )
        delete(postgres_delete_query, values, "bike")
        self.update_biker_selector()


def show_delete_biker_popup():
    show = DeleteBikerPopUp()
    popup_window = Popup(title="Delete Biker", content=show)
    show.ids.cancel.bind(on_press=popup_window.dismiss)
    popup_window.open()