from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.lang import Builder
from database import insert

Builder.load_file('insert/customer/customer.kv')


class InsertCustomerPopUp(BoxLayout):
    def submit(self):
        national_code = self.ids.customerNationalCodeInput.text
        first_name = self.ids.customerFirstName.text
        last_name = self.ids.customerLastName.text
        mobile_number = self.ids.customerMobileNumber.text
        age = self.ids.customerAge.text
        postgres_insert_query = " INSERT INTO customer(national_code, first_name, last_name, mobile_number, age) " \
                                " VALUES (%s, %s, %s, %s, %s) "
        values = (national_code, first_name, last_name, mobile_number, age)
        insert(postgres_insert_query, values, "customer")


def show_insert_customer_popup():
    show = InsertCustomerPopUp()
    popup_window = Popup(title="Insert customer", content=show)
    show.ids.cancel.bind(on_press=popup_window.dismiss)
    popup_window.open()
