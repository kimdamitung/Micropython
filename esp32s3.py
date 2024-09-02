import requests
from bs4 import BeautifulSoup
import os
import sys
import time

url = "https://micropython.org/download/ESP32_GENERIC_S3/"
download_dir = os.getcwd()
start_time = time.time()
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
        bin_path = os.path.join(download_dir, bin_filename)
        print(f"Downloading firmware from: {bin_url}...", flush=True)
        with requests.get(bin_url, stream=True) as r:
            r.raise_for_status()
            with open(bin_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        end_time = time.time()
        total_time = end_time - start_time
        print(f"Downloaded Firmware SUCCESS: {bin_path}", flush=True)
        print(f"========================= [SUCCESS] Took {total_time:.2f} seconds =========================", flush=True)
    else:
        raise Exception("Download Firmware FAILED: No download link found for .bin")
except Exception as e:
    end_time = time.time()
    total_time = end_time - start_time
    print(f"ERROR: {e}", flush=True)
    print(f"========================= [FAILED] Took {total_time:.2f} seconds =========================", flush=True)
