import os
import logging

from tkinter import *

from settings import (
    LOCAL_APPLICATION_PATH,
    LOCAL_MABX_CHANNEL,
    LOCAL_VEHICLE_CHANNEL,
    MAX_ODOMETER_VALUE,
    MODE,
    RPI_MABX_CHANNEL,
    RPI_VEHICLE_CHANNEL
)


class SessionTable(Frame):
    def __init__(self, parent, rows=7, columns=2):
        Frame.__init__(self, parent, background="grey")

        self.widgets = []
        headers = ["start_datetime", "end_datetime", "distance", "mode", "user", "car", "gps_points"]

        for row in range(rows):
            current_row = []

            label = Label(self, text="%s" % (headers[row]), borderwidth=0, width=15)
            label.grid(row=row, column=0, sticky="wns", padx=1, pady=1)
            current_row.append(label)

            label = Label(self, text="N/A", borderwidth=0, width=20)
            label.grid(row=row, column=1, sticky="wns", padx=1, pady=1)
            current_row.append(label)

            self.widgets.append(current_row)

        for column in range(columns):
            self.grid_columnconfigure(column, weight=2)

    def set(self, row, column, value):
        widget = self.widgets[row][column]
        widget.configure(text=value)

    def refresh(self, new_session):
        self.set(0, 1, new_session.start_datetime)
        self.set(1, 1, new_session.end_datetime)
        self.set(2, 1, new_session.distance)
        self.set(3, 1, new_session.mode)
        self.set(4, 1, new_session.user)
        self.set(5, 1, new_session.car)
        self.set(6, 1, new_session.gps_points)


class WidgetLogger(logging.Handler):
    def __init__(self, widget):
        logging.Handler.__init__(self)
        self.widget = widget

    def emit(self, record):
        self.widget.config(state=NORMAL)
        self.widget.insert(INSERT, record + '\n')
        self.widget.config(state=DISABLED)


class Interface(Frame):
    def __init__(self, window, main, can_manager, sessions_reader, mabx_ready, vehicle_ready):
        Frame.__init__(self, window, width=2000, height=1800)
        self.grid()

        self.can_manager = can_manager
        self.sessions_reader = sessions_reader
        self.main = main
        self.mabx_ready = mabx_ready
        self.vehicle_ready = vehicle_ready
        self.test_type = StringVar()

        # Device interface
        test_type_group = LabelFrame(self, text="Select the test type", font="bold")
        test_type_group.grid(row=0, column=0)

        local_rb = Radiobutton(test_type_group, text="Local", variable=self.test_type, value="local", command=self.change_test_type)
        local_rb.pack(anchor=W)
        rpi_rb = Radiobutton(test_type_group, text="Raspberry Pi", variable=self.test_type, value="rpi", command=self.change_test_type)
        rpi_rb.pack(anchor=W)
        self.test_type.set("local")

        # Send message interface
        send_message_group = LabelFrame(self, text="Send a new message", font="bold")
        send_message_group.grid(row=1, column=0)

        if vehicle_ready:
            # Odometer interface
            odometer_group = LabelFrame(send_message_group, text="Odometer", font="bold")
            odometer_group.pack()

            self.odometer_spinbox = Spinbox(odometer_group, from_=0, to=MAX_ODOMETER_VALUE)
            self.odometer_spinbox.pack(side="left")
            self.odometer_spinbox.delete(0, "end")
            self.odometer_spinbox.insert(END, 45987)

            odometer_button = Button(odometer_group, text="SEND", command=self.send_odometer)
            odometer_button.pack(side="right")

        if mabx_ready:
            # Mode interface
            mode_group = LabelFrame(send_message_group, text="Mode", font="bold")
            mode_group.pack()

            self.mode_listbox = Listbox(mode_group, height=3)
            self.mode_listbox.pack(side="left")
            for item in MODE:
                self.mode_listbox.insert(END, item.value)

            send_mode_button = Button(mode_group, text="SEND", command=self.send_mode)
            send_mode_button.pack(side="right")

        # Session interface
        session_group = LabelFrame(self, text="Last saved session", font="bold")
        session_group.grid(row=2, column=0)

        self.session_table = SessionTable(session_group, 7, 2)
        self.session_table.pack(side="left")

        refresh_button = Button(session_group, text="REFRESH", command=self.refresh_last_session)
        refresh_button.pack(side="right")

        # Logger interface
        logger_group = LabelFrame(self, text="Logger", font="bold")
        logger_group.grid(row=1, column=1)

        logger = Text(logger_group, state=DISABLED)
        logger_scrollbar = Scrollbar(logger_group, orient="vertical", command=logger.yview)
        logger.configure(yscrollcommand=logger_scrollbar.set)
        logger_scrollbar.pack(side="right", fill="y")
        logger.pack(side="left", fill="both", expand=True)
        self.text_logger = WidgetLogger(logger)

        # Launch interface
        launch_group = LabelFrame(self, text="Launch programs", font="bold")
        launch_group.grid(row=0, column=1)

        local_app_button = Button(launch_group, text="RaspiClient (locally)", command=self.launch_local_application)
        local_app_button.grid(row=0, column=0)

        rpi_app_button = Button(launch_group, text="RaspiClient (rpi)", command=self.launch_rpi_application)
        rpi_app_button.grid(row=0, column=1)


        if mabx_ready:
            if self.test_type.get() == "local":
                self.candump_mabx_button = Button(launch_group, text="Candump mabx", command=self.candump_mabx_bus)
                self.candump_mabx_button.grid(row=1, column=0)
            play_mabx_button = Button(launch_group, text="Play mabx log", command=self.play_mabx_log)
            play_mabx_button.grid(row=1, column=1)
            stop_mabx_button = Button(launch_group, text="Stop mabx log", command=self.stop_mabx_log)
            stop_mabx_button.grid(row=1, column=2)

        if vehicle_ready:
            if self.test_type.get() == "local":
                self.candump_vehicle_button = Button(launch_group, text="Candump vehicle", command=self.candump_vehicle_bus)
                self.candump_vehicle_button.grid(row=2, column=0)
            play_vehicle_button = Button(launch_group, text="Play vehicle log", command=self.play_vehicle_log)
            play_vehicle_button.grid(row=2, column=1)
            stop_vehicle_button = Button(launch_group, text="Stop vehicle log", command=self.stop_vehicle_log)
            stop_vehicle_button.grid(row=2, column=2)


    def candump_mabx_bus(self):
        os.system("gnome-terminal -e 'candump %s'" % LOCAL_MABX_CHANNEL)
        self.text_logger.emit("'candump %s' running on a new terminal." % LOCAL_MABX_CHANNEL)

    def candump_vehicle_bus(self):
        os.system("gnome-terminal -e 'candump %s'" % LOCAL_VEHICLE_CHANNEL)
        self.text_logger.emit("'candump %s' running on a new terminal." % LOCAL_VEHICLE_CHANNEL)

    def change_test_type(self):
        self.text_logger.emit("Changed test type to " + self.test_type.get() + ".")
        self.main.change_test_type(self.test_type.get())

        if self.test_type.get() == "local":
            if self.mabx_ready:
                self.candump_mabx_button.grid(row=1, column=0)
            if self.vehicle_ready:
                self.candump_vehicle_button.grid(row=2, column=0)
        else:
            self.candump_mabx_button.grid_remove()
            self.candump_vehicle_button.grid_remove()

    def launch_local_application(self):
        os.system("gnome-terminal -e 'bash -c \"python %s; exec bash\"'" % LOCAL_APPLICATION_PATH)
        self.text_logger.emit("RaspiClient launched locally.")

    def launch_rpi_application(self):
        self.text_logger.emit("Not implemented yet.")

    def play_mabx_log(self):
        self.can_manager.play_mabx_log()
        self.text_logger.emit("CAN logs of the mabx bus are currently being replayed.")

    def play_vehicle_log(self):
        self.can_manager.play_vehicle_log()
        self.text_logger.emit("CAN logs of the vehicle bus are currently being replayed.")

    def refresh_last_session(self):
        try:
            new_session = self.sessions_reader.get_last_session()
            self.session_table.refresh(new_session)
            self.text_logger.emit("Last " + self.test_type.get() + " session refreshed !")
        except FileNotFoundError:
            self.text_logger.emit("The session file doesn't exist.")

    def send_mode(self):
        new_mode = self.mode_listbox.get(ACTIVE)
        self.can_manager.set_mode(new_mode)
        if self.test_type.get() == "local":
            channel = LOCAL_MABX_CHANNEL
        else:
            channel = RPI_MABX_CHANNEL
        self.text_logger.emit("Message sent on %s (mode = %s)." % (channel, new_mode))

    def send_odometer(self):
        new_odometer = int(self.odometer_spinbox.get())
        if new_odometer <= MAX_ODOMETER_VALUE:
            self.can_manager.set_odometer(new_odometer)
            if self.test_type.get() == "local":
                channel = LOCAL_VEHICLE_CHANNEL
            else:
                channel = RPI_VEHICLE_CHANNEL
            self.text_logger.emit("Message sent on %s. (odometer = %s)." % (channel, new_odometer))
        else:
            self.text_logger.emit("This odometer value is too high (max = %s)." % MAX_ODOMETER_VALUE)

    def stop_mabx_log(self):
        self.can_manager.stop_playing_mabx_log()
        self.text_logger.emit("Stopped playing CAN logs from the mabx bus.")

    def stop_vehicle_log(self):
        self.can_manager.stop_playing_vehicle_log()
        self.text_logger.emit("Stopped playing CAN logs from the vehicle bus.")
