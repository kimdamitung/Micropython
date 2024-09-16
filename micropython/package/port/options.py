import subprocess
import sys
from time import time, sleep
import shutil

def processing(iteration, total, length = 40):
    percent = ("{0:.1f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = '<' + '=' * filled_length + '-' * (length - filled_length) + '>'
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
        print("\n========================= [SUCCESS] Took {:.2f} seconds =========================".format(total), flush=True)
    except subprocess.CalledProcessError as e:
        print("\nERROR\n", e, flush=True)
        print("ERROR\n", e.stderr, flush=True)
        end = time()
        total = end - start
        print(f"========================= [FAILED] Took {total:.2f} seconds =========================", flush=True)

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
        print("\n========================= [SUCCESS] Took {:.2f} seconds =========================".format(total), flush=True)
    except subprocess.CalledProcessError as e:
        print("\nERROR\n", e, flush=True)
        print("ERROR\n", e.stderr, flush=True)
        end = time()
        total = end - start
        print(f"========================= [FAILED] Took {total:.2f} seconds =========================", flush=True)
        
def serialMonitor(port):
    start = time()
    try:
        command = [
            'python', '-m', 'serial.tools.miniterm', port, '115200'
        ]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        end = time()
        total = end - start
        print("\n========================= [SUCCESS] Took {:.2f} seconds =========================".format(total), flush=True)
        for line in iter(process.stdout.readline, b''):
            print(line.decode('utf-8').strip())
        process.wait()
    except FileNotFoundError:
        print("Error: 'serial.tools.miniterm' module not found. Please install pyserial.")
    except Exception as e:
        print(f"An error occurred: {e}")