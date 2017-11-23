from tkinter import *

from can_manager import CanManager
from settings import CAN_IS_MABX_AVAILABLE, MODE


class Interface(Frame):
    
    def __init__(self, window, can_manager, mabx_ready, **kwargs):
        Frame.__init__(self, window, width=768, height=576, **kwargs)
        self.pack(fill=BOTH)

        self.can_manager = can_manager

        # Odometer interface
        self.odometer_group = LabelFrame(self, text="Odometer")
        self.odometer_group.pack()

        self.odometer_entry = Entry(self.odometer_group)
        self.odometer_entry.pack(side="left")
        
        self.odometer_button = Button(self.odometer_group, text="SEND", command=self.send_odometer)
        self.odometer_button.pack(side="right")

        if mabx_ready:
            # Mode interface
            self.mode_group = LabelFrame(self, text="Mode")
            self.mode_group.pack()

            self.mode_listbox = Listbox(self.mode_group)
            self.mode_listbox.pack(side="left")
            for item in MODE:
                self.mode_listbox.insert(END, item.value)

            self.send_mode_button = Button(self.mode_group, text="SEND", command=self.send_mode)
            self.send_mode_button.pack(side="right")

    def send_odometer(self):
        self.can_manager.set_odometer(self.odometer_entry.get())

    def send_mode(self):
        self.can_manager.set_mode(self.mode_listbox.get(ACTIVE))
    

class Main():

    def __init__(self):
        pass

    def run(self):

        self.can_manager = CanManager(CAN_IS_MABX_AVAILABLE)

        window = Tk()
        interface = Interface(window, self.can_manager, CAN_IS_MABX_AVAILABLE)

        interface.mainloop()
        interface.destroy()

if __name__ == '__main__':
    Main().run()