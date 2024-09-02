@echo off

rem Hướng dẫn command line interface
if "%1" == "" (
    goto help
) else if "%1" == "--help" (
    goto help
)

rem Tạo project MicroPython cho ESP32
if "%1" == "mkdir" (
    if "%2" == "esp32" (
        mkdir src && cd src && copy "E:\build_system_esp32\micropython\main\main.py" main.py && python E:/build_system_esp32/micropython/esp32.py && mkdir package && cd ..
    ) else if "%2" == "esp32s2" (
        mkdir src && cd src && copy "E:\build_system_esp32\micropython\main\main.py" main.py && python E:/build_system_esp32/micropython/esp32s2.py && mkdir package && cd ..
    ) else if "%2" == "esp32s3" (
        mkdir src && cd src && copy "E:\build_system_esp32\micropython\main\main.py" main.py && python E:/build_system_esp32/micropython/esp32s3.py && mkdir package && cd ..
    ) else (
        echo Invalid project type. Use esp32, esp32s2, or esp32s3.
    )
    goto eof
)

rem Kiểm tra số công COM trong máy tính
if "%1" == "port" (
    python E:/build_system_esp32/micropython/port/port.py
    goto eof
)

rem Xóa bộ nhớ flash của ESP32 và download firmware
if "%1" == "esp32" (
    esptool --chip esp32 --port %2 erase_flash && esptool --chip esp32 --port %2 --baud 460800 write_flash -z 0x1000 src/ESP32_GENERIC-20240602-v1.23.0.bin
    goto eof
) else if "%1" == "esp32s2" (
    esptool --chip esp32s2 --port %2 erase_flash && esptool --chip esp32s2 --port %2 write_flash -z 0x1000 src/LOLIN_S2_MINI-20240602-v1.23.0.bin
    goto eof
) else if "%1" == "esp32s3" (
    esptool --chip esp32s3 --port %2 erase_flash && esptool --chip esp32s3 --port %2 write_flash -z 0 src/ESP32_GENERIC_S3-20240602-v1.23.0.bin
    goto eof
)

rem Upload file main.py tới ESP32
if "%1" == "put" (
    ampy --port %2 put src/main.py
    goto eof
)

rem Remove source main.y để upload file mới, tránh lỗi ghi đè
if "%1" == "rm" (
    ampy --port %2 rm main.py
    goto eof
)

rem Chạy serial monitor MicroPython
if "%1" == "serial" (
    python -m serial.tools.miniterm %2 115200
    goto eof
)



goto help

:help
echo Usage: micropython [command] [options]
echo.
echo Commands:
echo   mkdir [esp32 or esp32s2 or esp32s3]               Create a new MicroPython project
echo   esp32s3 [PORT]                                    Erase flash and download firmware for ESP32-S3
echo   esp32 [PORT]                                      Erase flash and download firmware for ESP32
echo   esp32s2 [PORT]                                    Erase flash and download firmware for ESP32-S2
echo   put [PORT]                                        Upload main.py to ESP32 using ampy
echo   rm [PORT]                                         Remove main.py in firmware ESP32
echo   serial [PORT]                                     Start serial monitor for MicroPython
echo   port                                              Check COM number serial monitor for device manager
echo.
goto eof

:eof
