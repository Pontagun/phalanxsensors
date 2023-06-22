import configparser
import struct
from serialsensor import sensor as sensor


def byte_to_float(line):
    data = [line[3], line[2], line[1], line[0]]
    return struct.unpack('f', bytearray(data))


if __name__ == "__main__":
    reading = []
    config = configparser.ConfigParser()
    config.read("configuration.ini")

    marg_sensor = config["WiredMARGSensor"]
    connection = config["CONNECTION"]

    interval = (int(70000)).to_bytes(4, "big")
    delay = (0).to_bytes(4, "big")
    duration = (0xFFFFFFFF).to_bytes(4, "big")

    tare_command = [0xF7, 0x60, 0x60]
    start_command = [0xF7, 0x55, 0x55]
    stop_command = [0xF8, 0x00, 0x56, 0x56]

    CALCULATED_BYTES_RETURNED = 56

    marg = sensor(connection)
    connected_marg = marg.conect_serial()

    readline = []

    try:
        print("A connection status is {0}".format(marg.printout))
    except Exception as e:
        print(e)

    # YOST lab commands, for which sensor will be read
    commands = [0xF7, 0x50, 0x2D, 0x26, 0x27, 0x28, 0x00, 0xFF, 0xFF, 0xFF]
    commands.append(sum(commands[1:]) % 256)
    connected_marg.write(commands)

    # Set basic configuration of sensor's streaming.
    commands.clear()
    commands.append(0xF7)
    commands.append(0x52)
    commands.extend(interval)
    commands.extend(delay)
    commands.extend(duration)
    commands.append(sum(commands[1:]) % 256)

    connected_marg.write(commands)

    # Tare MARG sensor preparing for streaming.
    connected_marg.write(tare_command)

    # Start streaming ...
    connected_marg.write(start_command)

    while True:

        word = connected_marg.read()  # TODO change "word" to other names, it reads a byte(not 4).
        readline.append(int.from_bytes(word, byteorder="big", signed=False))

        if len(readline) == CALCULATED_BYTES_RETURNED:
            reading.append(byte_to_float(readline[0:4]))
            reading.append(byte_to_float(readline[4:8]))
            reading.append(byte_to_float(readline[8:12]))
            reading.append(byte_to_float(readline[12:16]))
            reading.append(byte_to_float(readline[16:20]))
            reading.append(byte_to_float(readline[20:24]))
            reading.append(byte_to_float(readline[24:28]))
            reading.append(byte_to_float(readline[28:32]))
            reading.append(byte_to_float(readline[32:36]))
            reading.append(byte_to_float(readline[36:40]))
            reading.append(byte_to_float(readline[40:44]))
            reading.append(byte_to_float(readline[44:48]))
            reading.append(byte_to_float(readline[48:52]))
            reading.append(byte_to_float(readline[52:56]))

            readline.clear()  # Streaming 56 bytes from command.
            reading.clear()  # Real readings (number)
