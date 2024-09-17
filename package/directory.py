import os
from pathlib import Path
from time import time # type: ignore
from colorama import Fore, Style

def initDirectory():
    start = time()
    src_directory = 'src'
    main_file = os.path.join(src_directory, 'main.py')
    package_directory = os.path.join(src_directory, 'package')
    init_file = os.path.join(package_directory, '__init__.py')
    content = """import esp\nesp.osdebug(0)\n#import module micropython\n\nwhile True:\n\t'''code'''\n\tpass"""
    Path(src_directory).mkdir(parents=True, exist_ok=True)
    Path(package_directory).mkdir(parents=True, exist_ok=True)
    with open(main_file, 'w', encoding='utf-8') as file:
        file.write(content)
    print("SUCCESS create file main.py", flush=True)
    with open(init_file, 'w', encoding='utf-8') as file:
        file.write('#__init__.py\n')
    print("SUCCESS create directory package", flush=True)
    end = time()
    total = end - start
    print(f"\n========================= [{Fore.GREEN}SUCCESS{Fore.RESET}] Took {total:.2f} seconds =========================", flush=True)