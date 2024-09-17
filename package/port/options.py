import subprocess
import sys
from time import time, sleep
from colorama import Fore, Style

def helpCommands():
    print("micropython v1.0.0")
    print("usage: micropython [--help]")
    print("                   [--check]")
    print("                   [--init]")
    print("                   [--init] [device]")
    print("                   [--uploads] [device] [port]")
    print("                   [--send] [type] [port]")
    print("                   [--serials] [port]")
    print("positional arguments: {device, type, port}")
    print("     device  :       [esp32, esp32s3, esp8266]")
    print("     type    :       [main, package]")
    print("     port    :       [COMx]")
    print("                     x is number")
    print("optional arguments: {--help, --check, --init, --uploads, --send, --serials}")
    print("     --help          show this help message and guide")
    print("     --check         check port COMx")
    print("     --init          init directory or init derectory to device")
    print("     --uploads       uploads file to device with port COMx")
    print("     --send          send file to device with port COMx")
    print("     --serials       monitor serial port with port COMx")
    print("")
    
def processing(iteration, total, length = 40):
    percent = ("{0:.1f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = '<' + Fore.GREEN + '=' * filled_length + Fore.WHITE + '-' * (length - filled_length) + Fore.RESET + '>'
    sys.stdout.write(f'\r[{bar}] {percent}% Complete')
    sys.stdout.flush()

def sendMain(port):
    start = time()
    try:
        command = [
            'ampy', '--port', port, 'put', 'src/main.py'
        ]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        total_lines = 100
        for i in range(total_lines):
            sleep(0.1)
            processing(i + 1, total_lines)
        process.wait()
        if process.returncode != 0:
            raise subprocess.CalledProcessError(process.returncode, command)
        end = time()
        total = end - start
        print(f"\n========================= [{Fore.GREEN}SUCCESS{Fore.RESET}] Took {total:.2f} seconds =========================", flush=True)
    except subprocess.CalledProcessError as e:
        print("\nERROR\n", e, flush=True)
        print("ERROR\n", e.stderr, flush=True)
        end = time()
        total = end - start
        print(f"\n========================= [{Fore.RED}FAILED{Fore.RESET}] Took {total:.2f} seconds =========================", flush=True)

def sendPackage(port):
    start = time()
    try:
        command = [
            'ampy', '--port', port, 'put', 'src/package/'
        ]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        total_lines = 100
        for i in range(total_lines):
            sleep(0.1)
            processing(i + 1, total_lines)
        process.wait()
        if process.returncode != 0:
            raise subprocess.CalledProcessError(process.returncode, command)
        end = time()
        total = end - start
        print(f"\n========================= [{Fore.GREEN}SUCCESS{Fore.RESET}] Took {total:.2f} seconds =========================", flush=True)
    except subprocess.CalledProcessError as e:
        print("\nERROR\n", e, flush=True)
        print("ERROR\n", e.stderr, flush=True)
        end = time()
        total = end - start
        print(f"\n========================= [{Fore.RED}FAILED{Fore.RESET}] Took {total:.2f} seconds =========================", flush=True)
        
def serialMonitor(port):
    start = time()
    try:
        command = [
            'python', '-m', 'serial.tools.miniterm', port, '115200'
        ]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        end = time()
        total = end - start
        print(f"\n========================= [{Fore.GREEN}SUCCESS{Fore.RESET}] Took {total:.2f} seconds =========================", flush=True)
        for line in iter(process.stdout.readline, b''):
            print(line.decode('utf-8').strip())
        process.wait()
    except FileNotFoundError:
        print("Error: 'serial.tools.miniterm' module not found. Please install pyserial.")
    except Exception as e:
        print(f"An error occurred: {e}")