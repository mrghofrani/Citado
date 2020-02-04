from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.lang import Builder
from database import query, update

Builder.load_file('delete/store/store.kv')


class DeleteStorePopUp(BoxLayout):
    def update_ingredient_selector(self):
        self.ids.store_selector.values = self.pick_values()

    def pick_values(self):
        postgres_query = """SELECT * FROM store  
                            WHERE start_time < current_date AND end_time > current_date"""
        self.store_list = query(postgres_query, "store")
        store_list = []
        if self.store_list:
            for row in self.store_list:
                store_list.append(row[0])
        return store_list

    def update_form(self):
        store = self.ids.store_selector.text
        if store != "Choose A Store":
            selected_row = tuple()
            for row in self.store_list:
                if row[0] == store:
                    selected_row = row
            self.ids.start_time.text = str(selected_row[1])
            self.ids.end_time.text = str(selected_row[2])
            self.ids.delete.disabled = False

    def delete(self):
        store = self.ids.store_selector.text
        for row in self.store_list:
            if row[0] == store:
                start_time = str(row[1])
                break
        postgres_delete_query = """UPDATE store
                                    SET end_time = current_date
                                    WHERE name = %s
                                    AND start_time = %s"""
        values = (store, start_time)
        update(postgres_delete_query, values, "store")
        self.ids.store_selector.values = self.pick_values()


def show_delete_store_popup():
    show = DeleteStorePopUp()
    popup_window = Popup(title="Delete Store", content=show)
    show.ids.cancel.bind(on_press=popup_window.dismiss)
    popup_window.open()
