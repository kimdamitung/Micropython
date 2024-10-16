import requests
from bs4 import BeautifulSoup
import os
import sys
import time  # type: ignore
from colorama import Fore, Style

def esp8266():
    pass

def esp_wroom_32(url = "https://micropython.org/download/ESP32_GENERIC/"):
    directory = os.path.join('src', 'firmware')
    os.makedirs(directory, exist_ok=True)
    start = time.time()
    try:
        print("Sending request to MicroPython download page...", flush=True)
        response = requests.get(url)
        response.raise_for_status()
        print("Parsing HTML...", flush = True)
        soup = BeautifulSoup(response.text, "html.parser")
        bin_link = soup.find("a", href=True, string="v1.23.0 (2024-06-02) .bin")
        if bin_link:
            print("Found download link for firmware...", flush = True)
            bin_url = f"https://micropython.org{bin_link['href']}"
            bin_filename = bin_url.split("/")[-1]
            bin_path = os.path.join(directory, bin_filename)
            print(f"Downloading firmware from: {bin_url}...", flush = True)
            with requests.get(bin_url, stream=True) as r:
                r.raise_for_status()
                with open(bin_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
            end = time.time()
            total = end - start
            print(f"Downloaded Firmware SUCCESS: {bin_path}", flush = True)
            print(f"\n========================= [{Fore.GREEN}SUCCESS{Fore.RESET}] Took {total:.2f} seconds =========================", flush=True)
        else:
            raise Exception("Download Firmware FAILED: No download link found for .bin")
    except Exception as e:
        end = time.time()
        total = end - start
        print(f"ERROR: {e}", flush = True)
        print(f"\n========================= [{Fore.RED}FAILED{Fore.RESET}] Took {total:.2f} seconds =========================", flush=True)
        
def esp32s3(url = "https://micropython.org/download/ESP32_GENERIC_S3/"):
    directory = os.path.join('src', 'firmware')
    os.makedirs(directory, exist_ok=True)
    start = time.time()
    try:
        print("Sending request to MicroPython download page...", flush=True)
        response = requests.get(url)
        response.raise_for_status()
        print("Parsing HTML...", flush=True)
        soup = BeautifulSoup(response.text, 'html.parser')
        bin_link = soup.find('a', href=True, string="[.bin]")
        if bin_link:
            print("Found download link for firmware...", flush=True)
            bin_url = f"https://micropython.org{bin_link['href']}"
            bin_filename = bin_url.split("/")[-1]
            bin_path = os.path.join(directory, bin_filename)
            print(f"Downloading firmware from: {bin_url}...", flush=True)
            with requests.get(bin_url, stream=True) as r:
                r.raise_for_status()
                with open(bin_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
            end = time.time()
            total = end - start
            print(f"Downloaded Firmware SUCCESS: {bin_path}", flush=True)
            print(f"\n========================= [{Fore.GREEN}SUCCESS{Fore.RESET}] Took {total:.2f} seconds =========================", flush=True)
        else:
            raise Exception("Download Firmware FAILED: No download link found for .bin")
    except Exception as e:
        end = time.time()
        total = end - start
        print(f"ERROR: {e}", flush=True)
        print(f"\n========================= [{Fore.RED}FAILED{Fore.RESET}] Took {total:.2f} seconds =========================", flush=True)
        
def esp32s3_spiram(url = "https://micropython.org/download/ESP32_GENERIC_S3/"):
    directory = os.path.join('src', 'firmware')
    os.makedirs(directory, exist_ok=True)
    start = time.time()
    try:
        print("Sending request to MicroPython download page...", flush=True)
        response = requests.get(url)
        response.raise_for_status()
        print("Parsing HTML...", flush=True)
        soup = BeautifulSoup(response.text, 'html.parser')
        bin_link = soup.find('a', href=True, string="[.bin]")
        if bin_link:
            print("Found download link for firmware...", flush=True)
            bin_url = f"https://micropython.org{bin_link['href']}"
            bin_filename = bin_url.split("/")[-1]
            bin_path = os.path.join(directory, bin_filename)
            print(f"Downloading firmware from: {bin_url}...", flush=True)
            with requests.get(bin_url, stream=True) as r:
                r.raise_for_status()
                with open(bin_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
            end = time.time()
            total = end - start
            print(f"Downloaded Firmware SUCCESS: {bin_path}", flush=True)
            print(f"\n========================= [{Fore.GREEN}SUCCESS{Fore.RESET}] Took {total:.2f} seconds =========================", flush=True)
        else:
            raise Exception("Download Firmware FAILED: No download link found for .bin")
    except Exception as e:
        end = time.time()
        total = end - start
        print(f"ERROR: {e}", flush=True)
        print(f"\n========================= [{Fore.RED}FAILED{Fore.RESET}] Took {total:.2f} seconds =========================", flush=True)