from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.lang import Builder
from database import query, delete

Builder.load_file('delete/customer/customer.kv')


class DeleteCustomerPopUp(BoxLayout):

    def __int__(self):
        super(BoxLayout, self).__init__()
        self.customer_list = []

    def pick_values(self):
        postgres_query = "SELECT * FROM customer"
        customer_id_list = []
        self.customer_list = query(postgres_query, "customer")
        for row in self.customer_list:
            customer_id_list.append(row[0])
        return customer_id_list

    def update_customer_selector(self):
        self.ids.customer_selector.values = self.pick_values()

    def update_form(self):
        selected_id = self.ids.customer_selector.text
        row = tuple()
        for i, v in enumerate(self.customer_list):
            if v[0] == selected_id:
                row = v
        self.ids.customerFirstName.text = row[1]  # First Name of Customer
        self.ids.customerLastName.text = row[2]  # Last Name of Customer
        self.ids.customerMobileNumber.text = row[3]  # Mobile number of Customer
        self.ids.customerAge.text = str(row[4])  # Age of Customer

    def delete(self):
        national_code = self.ids.customer_selector.text
        postgres_delete_query = """DELETE FROM customer
                              WHERE national_code = %s"""
        values = (national_code, )
        delete(postgres_delete_query, values, "customer")
        self.update_customer_selector()


def show_delete_customer_popup():
    show = DeleteCustomerPopUp()
    popup_window = Popup(title="Delete Customer", content=show)
    show.ids.cancel.bind(on_press=popup_window.dismiss)
    popup_window.open()
