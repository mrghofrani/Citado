from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from database import query
from kivy.uix.popup import Popup

Builder.load_file('log/log.kv')


class LogPopup(BoxLayout):
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


def show_log_popup():
    show = LogPopup()
    popup_window = Popup(title="Logs", content=show)
    show.ids.cancel.bind(on_press=popup_window.dismiss)
    popup_window.open()
