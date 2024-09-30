from bluetooth import BLE, UUID, FLAG_WRITE
from neopixel import NeoPixel
from machine import Pin
from network import WLAN, STA_IF
from time import sleep
        
class SmartConfigBLE(object):
    _IRQ_CENTRAL_CONNECT                = 1
    _IRQ_CENTRAL_DISCONNECT             = 2
    _IRQ_GATTS_WRITE                    = 3
    _IRQ_GATTS_READ_REQUEST             = 4
    _IRQ_SCAN_RESULT                    = 5
    _IRQ_SCAN_DONE                      = 6
    _IRQ_PERIPHERAL_CONNECT             = 7
    _IRQ_PERIPHERAL_DISCONNECT          = 8
    _IRQ_GATTC_SERVICE_RESULT           = 9
    _IRQ_GATTC_SERVICE_DONE             = 10
    _IRQ_GATTC_CHARACTERISTIC_RESULT    = 11
    _IRQ_GATTC_CHARACTERISTIC_DONE      = 12
    _IRQ_GATTC_DESCRIPTOR_RESULT        = 13
    _IRQ_GATTC_DESCRIPTOR_DONE          = 14
    _IRQ_GATTC_READ_RESULT              = 15
    _IRQ_GATTC_READ_DONE                = 16
    _IRQ_GATTC_WRITE_DONE               = 17
    _IRQ_GATTC_NOTIFY                   = 18
    _IRQ_GATTC_INDICATE                 = 19
    _IRQ_GATTS_INDICATE_DONE            = 20
    _IRQ_MTU_EXCHANGED                  = 21
    _IRQ_L2CAP_ACCEPT                   = 22
    _IRQ_L2CAP_CONNECT                  = 23
    _IRQ_L2CAP_DISCONNECT               = 24
    _IRQ_L2CAP_RECV                     = 25
    _IRQ_L2CAP_SEND_READY               = 26
    _IRQ_CONNECTION_UPDATE              = 27
    _IRQ_ENCRYPTION_UPDATE              = 28
    _IRQ_GET_SECRET                     = 29
    _IRQ_SET_SECRET                     = 30
    def __init__(self, name):
        self.name = name
        self.ble = BLE()
        self.ble.active(True)
        mac = self.ble.config('mac')[1]
        print("device MAC address is: " + mac.hex())
        self.ble.irq(self.ble_irq)
        self.connections = set()
        self.register()
        self.advertise()
        self.turn_error = NeoPixel(Pin(48, Pin.OUT), 1) 
        self.turn_error[0] = (0, 0, 0) 
        self.turn_error.write()
        self.ssid = ""
        self.password = ""
        self.wifiArrays = {"ssid": "", "pass": ""}

    def ble_irq(self, event, data):
        if event == self._IRQ_CENTRAL_CONNECT:
            conn_handle, addr_type, addr = data
            self.connections.add(conn_handle)
            print("BLE device connected successfully")
        elif event == self._IRQ_CENTRAL_DISCONNECT:
            conn_handle, addr_type, addr = data
            self.connections.remove(conn_handle)
            print("BLE device disconnected")
            self.advertise()
        elif event == self._IRQ_GATTS_WRITE:
            conn_handle, attr_handle = data
            value = self.ble.gatts_read(attr_handle).decode('UTF-8').strip()
            print("write event on attr_handle:", attr_handle, "value: ", value)
            self.handle_write(attr_handle, value) 

    def control_led(self, command):
        if command == "ON":
            self.turn_error[0] = (255, 0, 0) 
            print("LED is ON")
        elif command == "OFF":
            self.turn_error[0] = (0, 0, 0) 
            print("LED is OFF")
        self.turn_error.write()
        
    def connectWifi(self, ssid, password):
        print("Connecting to WiFi with SSID:", ssid, "and password:", password)
        if ssid and password:
            wlan = WLAN(STA_IF)
            wlan.active(True)
            wlan.connect(ssid, password)
            while not wlan.isconnected():
                sleep(1)
            ip_address = wlan.ifconfig()[0] 
            print("Device IP Address:", ip_address) 
        else:
            print("Invalid SSID or Password") 
            
    def register(self):
        MY_UUID = UUID("0bd62591-0b10-431a-982e-bd136821f35b")
        self.cmd_char = (UUID("0bd62593-0b10-431a-982e-bd136821f35b"), FLAG_WRITE,)
        self.ssid_char = (UUID("0bd62594-0b10-431a-982e-bd136821f35b"), FLAG_WRITE,)
        self.pass_char = (UUID("0bd62595-0b10-431a-982e-bd136821f35b"), FLAG_WRITE,)
        MY_SERVICE = (MY_UUID, (self.cmd_char, self.ssid_char, self.pass_char))
        SERVICES = (MY_SERVICE,)
        (self.cmd_handle, self.ssid_handle, self.pass_handle) = self.ble.gatts_register_services(SERVICES)[0]
        
    def handle_write(self, attr_handle, value):
        if attr_handle == self.cmd_handle:
            self.control_led(value)
        elif attr_handle == self.ssid_handle:
            self.ssid = value
            self.wifiArrays["ssid"] = self.ssid
            print("SSID set to:", self.ssid)
            self.attempt_wifi_connection()
        elif attr_handle == self.pass_handle:
            self.password = value
            self.wifiArrays["pass"] = self.password
            print("Password set to:", self.password)
            self.attempt_wifi_connection()
        else:
            print("Unknown characteristic written")
            
    def attempt_wifi_connection(self):
        if self.wifiArrays["ssid"] and self.wifiArrays["pass"]:
            self.connectWifi(self.wifiArrays["ssid"], self.wifiArrays["pass"])
        else:
            print("Waiting for SSID and Password...")
            
    def advertise(self):
        name = bytes(self.name, 'UTF-8')
        adv_data = bytearray(b'\x02\x01\x02') + bytearray((len(name) + 1, 0x09)) + name
        self.ble.gap_advertise(100, adv_data)