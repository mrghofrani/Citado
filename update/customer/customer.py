from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.lang import Builder
from database import update, query

Builder.load_file('update/customer/customer.kv')


class UpdateCustomerPopUp(BoxLayout):

    def __int__(self):
        super(BoxLayout, self).__init__()
        self.customer_list = []

    def pick_values(self):
        postgres_query = """SELECT * FROM customer"""
        self.customer_list = query(postgres_query, "customer")
        customer_id_list = []
        for row in self.customer_list:
            customer_id_list.append(row[0])
        return customer_id_list

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

    def submit(self):
        national_code = self.ids.customer_selector.text
        first_name = self.ids.customerFirstName.text
        last_name = self.ids.customerLastName.text
        mobile_number = self.ids.customerMobileNumber.text
        age = self.ids.customerAge.text

        postgres_update_query = """UPDATE customer
                              SET first_name = %s, last_name = %s, mobile_number = %s, age = %s
                              WHERE national_code = %s"""
        values = (first_name, last_name, mobile_number, age, national_code)
        update(postgres_update_query, values, "customer")


def show_update_customer_popup():
    show = UpdateCustomerPopUp()
    popup_window = Popup(title="Update Customer", content=show)
    show.cancel.bind(on_press=popup_window.dismiss)
    popup_window.open()
