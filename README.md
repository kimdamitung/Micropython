# Hướng dẫn thiết lập môi trường cho Micropython trên hệ điều hành Windows
## 1. Tải những module quan trọng cho môi trường Micropython
```bash
pip install -r requirements.txt
```
> Nhớ dẫn tới thư mục chứa requirements.txt để kích hoạt
## 2. Thiết lập môi trường

### 2.1. Download file hoặc git clone về

```bash
git clone https://github.com/kimdamitung/Micropython
```

> Hoặc

![1726629029100](image/README/1726629029100.png)

Sau khi download xong thì giải nén thông qua phần mền WinRAR nếu chưa có lo mà cài !!!

### 2.2. Add path cho micropython

Bước 1: Nút Window, search variables

![1726629174205](image/README/1726629174205.png)

Bước 2: Cửa sổ xuất hiện

![1726629204244](image/README/1726629204244.png)

> Chọn Environments Variables...

![1726629259803](image/README/1726629259803.png)

Bước 3: Trỏ con chuột vào path ở mục System variables, chọn Edit

![1726629348135](image/README/1726629348135.png)

Bước 4: New > Micropython-master/dist

![1726629406791](image/README/1726629406791.png)

Bước 5: Ok mọi giao diện 

### 2.3. Kiểm thử môi trường micropython trên máy tính windows

Bước 1: Nút Windows, search cmd, chọn Command Prompt

![1726629516008](image/README/1726629516008.png)

Bước 2: Gõ micropython và ấn Enter

![1726629605759](image/README/1726629605759.png)

> Nếu hiện như vậy là đã chạy thành công, còn nếu kết quả như sau

![1726629679492](image/README/1726629679492.png)

> Thì hảy thực hiện lại từ mục 2

## 3. Sử dụng Visual Studio Code để viết tạo chương trình micropython

### 3.1. Tải phần mền Visual Studio Code

> Tải bản Window để và cài đặt theo hướng dẫn từ hãng đã đề ra

![1725378375904](image/README/1725378375904.png)

> Giao diện: vào Extensions (Ctrl + Shift + x) để mở

![1725378480739](image/README/1725378480739.png)

> Giao diện: gõ "python" vào thanh search và ấn Install

![1725378550215](image/README/1725378550215.png)

> Giao diện: tải python hoàn tất gõ Ctrl + Shift + p

![1725378601917](image/README/1725378601917.png)

> Giao diện: tiếp tục gõ Open User Setting (JSON) và ấn Enter

```json
"python.autoComplete.extraPaths": [
    "Micropython-master/snippets/micropython-stubs-main/stubs/micropython-v1_20_0-esp32",
],
"python.analysis.extraPaths": [
    "Micropython-master/snippets/micropython-stubs-main/stubs/micropython-v1_20_0-esp32",
],
```

> Giao diện: đó là đường dẫn cục bộ, hãy thay thế nó thành đường dẫn ở máy tính của bạn