from package.port.port import testingPortSerial
from package.port.options import sendMain, sendPackage, serialMonitor
from package.firmware.firmware import esp_wroom_32, esp32s3
from package.directory import initDirectory
from package.uploads.uploads import uploadsESP32S3
from argparse import ArgumentParser
import sys

parser = ArgumentParser(description="Micropython")
parser.add_argument("--check", action = "store_true", help = "Check to the device")
parser.add_argument("--init", nargs = '?', const = 'list', help = "Initialize project with device")
parser.add_argument("--uploads", nargs = 2, metavar = ('DEVICE', 'PORT'), help = "Downloads firmware to device")
parser.add_argument("--send", nargs = 2, metavar = ('TYPE', 'PORT'), help = "Downloads firmware to device")
parser.add_argument("--serials", metavar='PORT', help="Open serial monitor on port")
args = parser.parse_args()
if args.init == 'list':
    initDirectory()
elif args.init:
    if args.init == "esp32":
        initDirectory()
        esp_wroom_32()
    elif args.init == "esp32s3":
        initDirectory()
        esp32s3()
    elif args.init == "esp8266":
        pass
    else:
        initDirectory()
if args.check:
    testingPortSerial()
if args.uploads:
    device, port = args.uploads
    if device == "esp32":
        pass
    elif device == "esp32s3":
        uploadsESP32S3(port)
    elif device == "esp8266":
        pass
    else:
        print("[name device]: esp32, esp32s3, esp8266")
if args.send:
    type, port = args.send
    if type == "main":
        sendMain(port)
    elif type == "package":
        sendPackage(port)
    else:
        print("[type]: main, package")
if args.serials:
    port = args.serials
    serialMonitor(port)