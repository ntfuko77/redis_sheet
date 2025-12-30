import rich
import logging



class PageGerator:
    def __init__(self, service):
        self.service = service
    def print_welecome(self):
        rich.print(self.service.welecome)
    def view_data_form(self):
        rich.print('Data Form:')
        rich.print(self.service.data_form)
    def function_menu(self):
        rich.print(self.service.function_menu)
        rich.print('Please select a function:')

