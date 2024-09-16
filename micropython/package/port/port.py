import serial.tools.list_ports
    
def testingPortSerial():
    ports = serial.tools.list_ports.comports()
    print(f"Có {len(ports)} cổng COM đang được phát hiện.")
    for port, desc, hwid in sorted(ports):
        print(f"{port}: {desc} ({hwid})") 
    