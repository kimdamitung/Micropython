import subprocess
import sys
from time import time

def uploadsESP32S3(port):
    start = time()
    try:
        uploads = [
            'python', '-m', 'esptool',
            '--chip', 'esp32s3',
            '--port', port,
            'erase_flash'
        ]
        with subprocess.Popen(uploads, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as process:
            for line in process.stdout:
                print(line, end='', flush=True)
            stderr = process.stderr.read()
            if stderr:
                print(stderr, end='', flush=True)
            process.wait()
            if process.returncode != 0:
                raise subprocess.CalledProcessError(process.returncode, uploads)
        pushOS = [
            'python', '-m', 'esptool',
            '--chip', 'esp32s3',
            '--port', port,
            'write_flash', '-z', '0', 'src/firmware/ESP32_GENERIC_S3-20240602-v1.23.0.bin'
        ]
        with subprocess.Popen(pushOS, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as process:
            for line in process.stdout:
                print(line, end='', flush=True)
            stderr = process.stderr.read()
            if stderr:
                print(stderr, end='', flush=True)
            process.wait()
            if process.returncode != 0:
                raise subprocess.CalledProcessError(process.returncode, pushOS)
        end = time()
        total = end - start
        print(f"========================= [SUCCESS] Took {total:.2f} seconds =========================", flush=True)
    except subprocess.CalledProcessError as e:
        print("ERROR\n", e, flush=True)
        print("ERROR\n", e.stderr, flush=True)
        end = time()
        total = end - start
        print(f"========================= [FAILED] Took {total:.2f} seconds =========================", flush=True)