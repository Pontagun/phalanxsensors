import serial

class sensor:
    def __init__(self, connection):
        self.serial_con = None
        self.usb = connection["usb"]
        self.timeout = int(connection["timeout"])
        self.baud_rate = connection["baud_rate"]

    def conect_serial(self):
        self.serial_con = serial.Serial(self.usb, self.baud_rate, timeout=self.timeout)
        return self.serial_con

    def printout(self):
        return self.serial_con.isOpen()

    def write_to_sensor(self, commands):
        pass