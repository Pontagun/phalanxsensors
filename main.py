import configparser
import struct
from serialsensor import sensor as sensor

read_bytes0 = []
commands = []

if __name__ == "__main__":
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
        # readline.append(float.from_bytes(connected_marg.read(), byteorder="big", signed=True))
        #readline.append(struct.unpack('f', connected_marg.read()))
        # print(int.from_bytes(connected_marg.read(), byteorder="big", signed=True))

        # a = connected_marg.read(4)
        word = connected_marg.read(4)
        readline.append(int.from_bytes(word, byteorder="big", signed=True))
        # readline.append(struct.unpack('f', connected_marg.read(4)))
        if len(readline) == 16 - 1:
            print("P {0}", readline)
            readline.clear()


    # for i in range(300):
    #     a = connected_marg.read(CALCULATED_BYTES_RETURNED)
    #     aa = [int.from_bytes(a, byteorder="big", signed=True) for x in a]
    #     print(i, aa)


    # print(stream_slot_byte)