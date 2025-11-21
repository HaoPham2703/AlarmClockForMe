# ⏰ Alarm Clock (Báo Thức)

A Python-based alarm clock application with an interactive analog clock interface and math challenge feature to turn off the alarm.

## 📋 Features

- **Interactive Analog Clock**: Drag the hour and minute hands to set the alarm time
- **AM/PM Toggle**: Switch between AM and PM modes
- **Custom Alarm Sound**: Choose your own audio file (MP3, WAV, OGG)
- **Math Challenge**: Solve a math problem to turn off the alarm (prevents accidentally turning it off)
- **Real-time Clock Display**: Shows current time in digital format
- **Scrollable Interface**: Responsive UI that adapts to different screen sizes

## 🛠️ Requirements

- Python 3.7 or higher
- tkinter (usually included with Python)
- pygame 2.6.1
- pyinstaller 6.3.0 (optional, for building executable)

## 📦 Installation

1. Clone or download this repository

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install pygame==2.6.1
```

## 🚀 Usage

### Running the Application

Run the Python script:
```bash
python alarm_clock.py
```

### Setting an Alarm

1. **Set the time**: 
   - Drag the hour hand (black) to set the hour
   - Drag the minute hand (red) to set the minutes
   - Click the AM/PM button to toggle between morning and afternoon

2. **Select alarm sound**:
   - Click "Chọn file nhạc" (Select music file) button
   - Choose an audio file (MP3, WAV, or OGG format)

3. **Activate alarm**:
   - Click "Bật Báo Thức" (Turn On Alarm) button
   - The alarm will trigger at the set time

### Turning Off the Alarm

When the alarm goes off:
- A math challenge window will appear
- Solve the arithmetic problem (addition or subtraction)
- Enter the correct answer to turn off the alarm
- The alarm will continue playing until you solve the problem correctly

## 🔨 Building Executable (Optional)

To create a standalone executable file:

1. Install PyInstaller:
```bash
pip install pyinstaller
```

2. Build the executable:
```bash
pyinstaller --onefile --windowed alarm_clock.py
```

The executable will be created in the `dist` folder.

## 📝 Notes

- The alarm will automatically set for the next day if the selected time has already passed today
- The math challenge prevents accidental alarm dismissal
- The application supports scrolling for smaller screens
- Audio files must be in supported formats (MP3, WAV, OGG)

## 🐛 Troubleshooting

- **No sound**: Make sure you've selected a valid audio file and pygame is properly installed
- **Window not appearing**: Check if tkinter is installed (usually comes with Python)
- **Math challenge keeps appearing**: Make sure to enter the correct answer as a number

---

# ⏰ Báo Thức

Ứng dụng báo thức được xây dựng bằng Python với giao diện đồng hồ kim tương tác và tính năng giải toán để tắt báo thức.

## 📋 Tính năng

- **Đồng hồ kim tương tác**: Kéo kim giờ và kim phút để đặt thời gian báo thức
- **Chuyển đổi AM/PM**: Chuyển đổi giữa chế độ sáng và chiều
- **Nhạc chuông tùy chỉnh**: Chọn file âm thanh của riêng bạn (MP3, WAV, OGG)
- **Thử thách toán học**: Giải bài toán để tắt báo thức (ngăn việc tắt nhầm)
- **Hiển thị thời gian thực**: Hiển thị thời gian hiện tại ở định dạng số
- **Giao diện có thể cuộn**: UI linh hoạt, thích ứng với các kích thước màn hình khác nhau

## 🛠️ Yêu cầu

- Python 3.7 trở lên
- tkinter (thường được bao gồm với Python)
- pygame 2.6.1
- pyinstaller 6.3.0 (tùy chọn, để tạo file thực thi)

## 📦 Cài đặt

1. Clone hoặc tải repository này

2. Cài đặt các thư viện cần thiết:
```bash
pip install -r requirements.txt
```

Hoặc cài đặt thủ công:
```bash
pip install pygame==2.6.1
```

## 🚀 Sử dụng

### Chạy ứng dụng

Chạy file Python:
```bash
python alarm_clock.py
```

### Đặt báo thức

1. **Đặt thời gian**: 
   - Kéo kim giờ (màu đen) để đặt giờ
   - Kéo kim phút (màu đỏ) để đặt phút
   - Click nút AM/PM để chuyển đổi giữa sáng và chiều

2. **Chọn nhạc chuông**:
   - Click nút "Chọn file nhạc"
   - Chọn file âm thanh (định dạng MP3, WAV hoặc OGG)

3. **Kích hoạt báo thức**:
   - Click nút "Bật Báo Thức"
   - Báo thức sẽ kêu vào thời gian đã đặt

### Tắt báo thức

Khi báo thức kêu:
- Cửa sổ thử thách toán học sẽ xuất hiện
- Giải bài toán số học (cộng hoặc trừ)
- Nhập đáp án đúng để tắt báo thức
- Báo thức sẽ tiếp tục kêu cho đến khi bạn giải đúng

## 🔨 Tạo file thực thi (Tùy chọn)

Để tạo file thực thi độc lập:

1. Cài đặt PyInstaller:
```bash
pip install pyinstaller
```

2. Tạo file thực thi:
```bash
pyinstaller --onefile --windowed alarm_clock.py
```

File thực thi sẽ được tạo trong thư mục `dist`.

## 📝 Lưu ý

- Báo thức sẽ tự động đặt cho ngày hôm sau nếu thời gian đã chọn đã qua trong ngày hôm nay
- Thử thách toán học ngăn việc tắt báo thức nhầm
- Ứng dụng hỗ trợ cuộn cho màn hình nhỏ hơn
- File âm thanh phải ở định dạng được hỗ trợ (MP3, WAV, OGG)

## 🐛 Khắc phục sự cố

- **Không có âm thanh**: Đảm bảo bạn đã chọn file âm thanh hợp lệ và pygame đã được cài đặt đúng cách
- **Cửa sổ không hiển thị**: Kiểm tra xem tkinter đã được cài đặt chưa (thường đi kèm với Python)
- **Thử thách toán học cứ xuất hiện**: Đảm bảo nhập đáp án đúng dưới dạng số


