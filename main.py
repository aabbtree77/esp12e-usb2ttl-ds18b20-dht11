import machine
import ds18x20
import onewire
import time
import dht

#Disable WIFI
import network
sta_if = network.WLAN(network.STA_IF)
sta_if.active(False)
ap_if = network.WLAN(network.AP_IF)
ap_if.active(False)


#ds18x20
def rom_to_hex(rom):
    """Convert rom bytearray to hex string."""
    return ''.join('{:02x}'.format(x) for x in rom)

ds = ds18x20.DS18X20(onewire.OneWire(machine.Pin(2)))
def read_ds18b20():
    ds.convert_temp()
    time.sleep_ms(1000)
    tdict = {rom_to_hex(rom): ds.read_temp(rom) for rom in ds.scan()}
    tval = list(tdict.values())
    return int(tval[0])


#DHT11
dht_sensor = dht.DHT11(machine.Pin(4))
def read_dht11():
    dht_sensor.measure()
    time.sleep_ms(2000)
    return (dht_sensor.temperature(), dht_sensor.humidity())


#Heat output, on/off reversed!!! On means inactive, LED=0.
pin_heat = machine.Pin(13, machine.Pin.OUT)
pin_heat.on()

T_ds18b20 = 0
T_dht11 = 0
H_dht11 = 0

while True:
    try:
        T_ds18b20 = read_ds18b20()
    except Exception as e:
        print("Ignoring DS18b20 error, code {}.".format(e))
    
    try:
        T_dht11, H_dht11 = read_dht11()
    except Exception as e:
        print("Ignoring DHT11 error, code {}.".format(e)) 
    
    if T_ds18b20 > T_dht11:
        pin_heat.off()
    else:
        pin_heat.on()
    
    time.sleep_ms(10000)    
    #print(T_ds18b20,T_dht11,H_dht11, pin_heat.value())
            
