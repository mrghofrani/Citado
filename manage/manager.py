from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from database import query
from kivy.uix.popup import Popup
from database import file_executer

Builder.load_file('manage/manager.kv')


class ManagePopup(BoxLayout):
    def drop_customer(self):
        file_executer(file_path='table_instructions/customer/drop.sql')

    def create_customer(self):
        file_executer('table_instructions/customer/create.sql')

    def drop_address(self):
        file_executer('table_instructions/address/drop.sql')

    def create_address(self):
        file_executer('table_instructions/address/create.sql')

    def drop_food(self):
        file_executer('table_instructions/food/drop.sql')

    def create_food(self):
        file_executer('table_instructions/food/create.sql')

    def drop_ingredient(self):
        file_executer('table_instructions/ingredient/drop.sql')

    def create_ingredient(self):
        file_executer('table_instructions/ingredient/create.sql')

    def drop_store(self):
        file_executer('table_instructions/store/drop.sql')

    def create_store(self):
        file_executer('table_instructions/food/create.sql')

    def return_query(self, table_name):
        self.ids[table_name].clear_widgets()
        postgres_insert_query = f"SELECT * FROM {table_name} "
        values = (table_name,)
        log_query = query(postgres_insert_query, table_name)
        if log_query:
            layout = self.ids[table_name]
            for item in log_query:
                box = BoxLayout(orientation='horizontal')
                for column in item[1:]:
                    box.add_widget(Label(text=str(column)))
                layout.add_widget(box)


def show_manager_popup():
    show = ManagePopup()
    popup_window = Popup(title="Manage", content=show)
    show.ids.exit.bind(on_press=popup_window.dismiss)
    popup_window.open()
