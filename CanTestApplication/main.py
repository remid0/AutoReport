from tkinter import *

from can_manager import CanManager
from interface import Interface
from sessions_reader import SessionsReader
from settings import INITIAL_TEST_TYPE, IS_MABX_READY, IS_VEHICLE_READY


class Main():

    def __init__(self):
        pass

    def run(self):
        self.can_manager = CanManager(IS_MABX_READY, IS_VEHICLE_READY, INITIAL_TEST_TYPE)
        self.sessions_reader = SessionsReader(INITIAL_TEST_TYPE)

        window = Tk()
        window.title("TX : CanTestApplication")
        interface = Interface(window, self, IS_MABX_READY, IS_VEHICLE_READY)
        interface.mainloop()
        interface.destroy()

    def change_test_type(self, new_type):
        self.can_manager.__del__()
        self.can_manager = CanManager(IS_MABX_READY, IS_VEHICLE_READY, new_type)
        self.sessions_reader.set_test_type(new_type)

if __name__ == '__main__':
    Main().run()