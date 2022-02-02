import bluetooth

def scan():

    print("Scanning for bluetooth devices:")

    devices = bluetooth.discover_devices(
                            duration=20,
                            flush_cache=True,
                            lookup_names = True,
                            lookup_class = True)

    number_of_devices = len(devices)

    print(number_of_devices,"devices found")

    for addr, name, device_class in devices:

        print("\n")

        print("Device Name: %s" % (name))

        print("Device MAC Address: %s" % (addr))

        print("Device Class: %s" % (device_class))

        # check for services
        print('scanning for services ...')
        services = bluetooth.find_service(address=addr)
        if len(services) <=0:
            print("zero services found on", addr)
        else:
            for serv in services:
                print('Service:', serv['name'])

        #print("\n")

    return

if __name__ == '__main__':
    scan()
