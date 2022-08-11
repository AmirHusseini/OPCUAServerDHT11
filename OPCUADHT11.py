from opcua import Server
import RPi.GPIO as GPIO
import dht11
import time
import datetime

server = Server()

url = "opc.tcp://your ip address:4840"
server.set_endpoint(url)

# the name of server
name = "OPCUA_SIMULATION_SERVER"
addspace = server.register_namespace(name)


node = server.get_objects_node()

Param = node.add_object(addspace, "Parameters")

# Values 
Temp = Param.add_variable(addspace, "Temperature", 0)
Hum = Param.add_variable(addspace, "Humidity", 0)
Time = Param.add_variable(addspace, "Time", 0)

Temp.set_writable()
Hum.set_writable()
Time.set_writable()

# Start the server
server.start()
print("Server started at {}".format(url))

# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

# read data using pin 17
instance = dht11.DHT11(pin=17)

while True:
    result = instance.read()
    if result.is_valid():
        # Read the data and put them in the variables
        Temperature = result.temperature
        Humidity = result.humidity
        TIME = datetime.datetime.now()


        print(Temperature, Humidity, TIME)

        Temp.set_value(Temperature)
        Hum.set_value(Humidity)
        Time.set_value(TIME)

    time.sleep(2)

