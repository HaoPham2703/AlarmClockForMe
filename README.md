# ⏰ Alarm Clock (Báo Thức)

A Python-based alarm clock application with an interactive analog clock interface, multiple alarms management, sleep cycle calculator, and math challenge feature to turn off the alarm.

## 📋 Features

- **Multiple Alarms Management**: Create, edit, enable/disable, and delete multiple alarms
- **Interactive Analog Clock**: Drag the hour and minute hands to set the alarm time
- **AM/PM Toggle**: Switch between AM and PM modes
- **Custom Alarm Sound**: Choose your own audio file (MP3, WAV, OGG)
- **Sleep Cycle Calculator**: Calculate optimal sleep/wake times based on 90-minute sleep cycles (3-8 cycles)
- **Math Challenge**: Solve configurable number of math problems to turn off the alarm (prevents accidentally turning it off)
- **Text-to-Speech**: Optional feature to read current time aloud (requires pyttsx3)
- **Real-time Clock Display**: Shows current time in digital format
- **Alarm Persistence**: Alarms are saved to JSON file and persist between sessions
- **Scrollable Interface**: Responsive UI that adapts to different screen sizes
- **Alarm Naming**: Optional custom names for each alarm

## 🛠️ Requirements

- Python 3.7 or higher
- tkinter (usually included with Python)
- pygame 2.6.1
- pyttsx3 2.90 (optional, for text-to-speech feature)
- pyinstaller 6.3.0 (optional, for building executable)

## 📦 Installation

1. Clone or download this repository

2. Create a virtual environment (recommended):

```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

This will install:

- `pygame==2.6.1` - For playing alarm sounds
- `pyttsx3==2.90` - For text-to-speech feature (optional)
- `pyinstaller==6.3.0` - For building executable (optional)

**Note**: If you only want to test pose detection feature, you can also install:

```bash
pip install -r requirements_test.txt
```

## 🚀 Usage

### Running the Application

Run the Python script:

```bash
python alarm_clock.py
```

### Setting an Alarm

1. **Click "➕ Thêm Báo Thức Mới"** to create a new alarm

2. **Set the alarm name** (optional):

   - Enter a custom name for the alarm in the "Tên báo thức" field

3. **Use Sleep Cycle Calculator** (optional):

   - Choose calculation mode:
     - "Tính từ thời gian muốn dậy" - Calculate sleep time from desired wake time
     - "Tính từ thời gian muốn ngủ" - Calculate wake time from desired sleep time
   - Enter the time and click "Tính toán"
   - Review the recommended sleep cycles (4-6 cycles are recommended)
   - Click "Áp dụng" on a cycle option to automatically set the alarm time

4. **Set the time manually**:

   - Drag the hour hand (black) to set the hour
   - Drag the minute hand (red) to set the minutes
   - Click the AM/PM button to toggle between morning and afternoon

5. **Select alarm sound**:

   - Click "Chọn file nhạc" (Select music file) button
   - Choose an audio file (MP3, WAV, or OGG format)

6. **Configure math challenge**:

   - Set the number of math problems (1-10) that must be solved correctly to turn off the alarm

7. **Save the alarm**:
   - Click "Lưu" (Save) button
   - The alarm will be added to your list and will trigger at the set time

### Managing Alarms

- **View all alarms**: The main screen shows all your alarms with their status
- **Enable/Disable**: Click "Bật" or "Tắt" to toggle an alarm on/off
- **Edit**: Click "✏️ Sửa" to modify an existing alarm
- **Delete**: Click "🗑️ Xóa" to remove an alarm

### Turning Off the Alarm

When the alarm goes off:

- A math challenge window will appear (modal, cannot be closed easily)
- Solve the required number of arithmetic problems (addition or subtraction)
- Enter the correct answer for each problem
- The alarm will continue playing until you solve all problems correctly
- Progress is shown: "X/Y bài đã giải đúng"

### Text-to-Speech Feature

- Click "🔊 Đọc Thời Gian" button to hear the current time read aloud
- Requires `pyttsx3` to be installed

## 🔨 Building Executable (Optional)

To create a standalone executable file:

1. PyInstaller should already be installed from `requirements.txt`

2. Build the executable using the spec file:

```bash
pyinstaller alarm_clock.spec
```

Or build directly:

```bash
pyinstaller --onefile --console alarm_clock.py
```

**Note**: The spec file uses `console=True` to show console output. To build without console, change `console=False` in the spec file.

The executable will be created in the `dist` folder.

## 🧪 Testing Pose Detection (Experimental)

The project includes a test file for pose detection using MediaPipe:

```bash
python test_pose_detection.py
```

This feature is currently experimental and not integrated into the main alarm clock application. It requires:

- `opencv-python>=4.5.0`
- `mediapipe>=0.10.0`

Install test dependencies:

```bash
pip install -r requirements_test.txt
```

## 📝 Notes

- **Automatic Date Adjustment**: The alarm will automatically set for the next day if the selected time has already passed today
- **Math Challenge**: Prevents accidental alarm dismissal. You must solve all required problems correctly to turn off the alarm
- **Sleep Cycles**: Based on 90-minute REM cycles. 4-6 cycles (6-9 hours) are recommended for optimal rest
- **Data Persistence**: Alarms are saved to `alarms_data.json` in the project directory
- **Audio Formats**: Supported formats are MP3, WAV, and OGG
- **Multiple Alarms**: You can create unlimited alarms, each with its own settings
- **Text-to-Speech**: Optional feature. If pyttsx3 is not installed, the TTS button will not appear

## 🐛 Troubleshooting

- **No sound**:

  - Make sure you've selected a valid audio file
  - Check that pygame is properly installed: `pip install pygame`
  - Verify the audio file path is correct and accessible

- **Window not appearing**:

  - Check if tkinter is installed (usually comes with Python)
  - On Linux, you may need to install: `sudo apt-get install python3-tk`

- **Math challenge keeps appearing**:

  - Make sure to enter the correct answer as a number
  - You must solve ALL required problems correctly (check the progress indicator)

- **TTS not working**:

  - Install pyttsx3: `pip install pyttsx3`
  - On Linux, you may need additional dependencies: `sudo apt-get install espeak`

- **Alarms not saving**:

  - Check file permissions in the project directory
  - Ensure `alarms_data.json` is not read-only

- **Sleep cycle calculator not working**:
  - Make sure you enter valid time (0-23 for hours, 0-59 for minutes)
  - Click "Tính toán" button after entering the time

---

# ⏰ Báo Thức

Ứng dụng báo thức được xây dựng bằng Python với giao diện đồng hồ kim tương tác, quản lý nhiều báo thức, tính năng tính toán chu kỳ ngủ và giải toán để tắt báo thức.

## 📋 Tính năng

- **Quản lý nhiều báo thức**: Tạo, chỉnh sửa, bật/tắt và xóa nhiều báo thức
- **Đồng hồ kim tương tác**: Kéo kim giờ và kim phút để đặt thời gian báo thức
- **Chuyển đổi AM/PM**: Chuyển đổi giữa chế độ sáng và chiều
- **Nhạc chuông tùy chỉnh**: Chọn file âm thanh của riêng bạn (MP3, WAV, OGG)
- **Tính toán chu kỳ ngủ**: Tính toán thời gian ngủ/thức tối ưu dựa trên chu kỳ ngủ 90 phút (3-8 chu kỳ)
- **Thử thách toán học**: Giải số lượng bài toán có thể cấu hình để tắt báo thức (ngăn việc tắt nhầm)
- **Text-to-Speech**: Tính năng tùy chọn để đọc thời gian hiện tại (yêu cầu pyttsx3)
- **Hiển thị thời gian thực**: Hiển thị thời gian hiện tại ở định dạng số
- **Lưu trữ báo thức**: Báo thức được lưu vào file JSON và giữ nguyên giữa các phiên
- **Giao diện có thể cuộn**: UI linh hoạt, thích ứng với các kích thước màn hình khác nhau
- **Đặt tên báo thức**: Tùy chọn đặt tên tùy chỉnh cho mỗi báo thức

## 🛠️ Yêu cầu

- Python 3.7 trở lên <>
- tkinter (thường được bao gồm với Python)
- pygame 2.6.1
- pyttsx3 2.90 (tùy chọn, cho tính năng text-to-speech)
- pyinstaller 6.3.0 (tùy chọn, để tạo file thực thi)

## 📦 Cài đặt

1. Clone hoặc tải repository này

2. Tạo môi trường ảo (khuyến nghị):

```bash
python -m venv venv
# Trên Windows:
venv\Scripts\activate
# Trên Linux/Mac:
source venv/bin/activate
```

3. Cài đặt các thư viện cần thiết:

```bash
pip install -r requirements.txt
```

Sẽ cài đặt:

- `pygame==2.6.1` - Để phát âm thanh báo thức
- `pyttsx3==2.90` - Cho tính năng text-to-speech (tùy chọn)
- `pyinstaller==6.3.0` - Để tạo file thực thi (tùy chọn)

**Lưu ý**: Nếu bạn chỉ muốn test tính năng nhận diện tư thế, có thể cài đặt:

```bash
pip install -r requirements_test.txt
```

## 🚀 Sử dụng

### Chạy ứng dụng

Chạy file Python:

```bash
python alarm_clock.py
```

### Đặt báo thức

1. **Click "➕ Thêm Báo Thức Mới"** để tạo báo thức mới

2. **Đặt tên báo thức** (tùy chọn):

   - Nhập tên tùy chỉnh cho báo thức vào trường "Tên báo thức"

3. **Sử dụng tính toán chu kỳ ngủ** (tùy chọn):

   - Chọn chế độ tính toán:
     - "Tính từ thời gian muốn dậy" - Tính thời gian ngủ từ thời gian muốn thức dậy
     - "Tính từ thời gian muốn ngủ" - Tính thời gian thức dậy từ thời gian muốn ngủ
   - Nhập thời gian và click "Tính toán"
   - Xem các chu kỳ ngủ được khuyến nghị (4-6 chu kỳ được khuyến nghị)
   - Click "Áp dụng" trên một tùy chọn chu kỳ để tự động đặt thời gian báo thức

4. **Đặt thời gian thủ công**:

   - Kéo kim giờ (màu đen) để đặt giờ
   - Kéo kim phút (màu đỏ) để đặt phút
   - Click nút AM/PM để chuyển đổi giữa sáng và chiều

5. **Chọn nhạc chuông**:

   - Click nút "Chọn file nhạc"
   - Chọn file âm thanh (định dạng MP3, WAV hoặc OGG)

6. **Cấu hình thử thách toán học**:

   - Đặt số lượng bài toán (1-10) phải giải đúng để tắt báo thức

7. **Lưu báo thức**:
   - Click nút "Lưu"
   - Báo thức sẽ được thêm vào danh sách và sẽ kêu vào thời gian đã đặt

### Quản lý báo thức

- **Xem tất cả báo thức**: Màn hình chính hiển thị tất cả báo thức với trạng thái của chúng
- **Bật/Tắt**: Click "Bật" hoặc "Tắt" để bật/tắt báo thức
- **Chỉnh sửa**: Click "✏️ Sửa" để sửa đổi báo thức hiện có
- **Xóa**: Click "🗑️ Xóa" để xóa báo thức

### Tắt báo thức

Khi báo thức kêu:

- Cửa sổ thử thách toán học sẽ xuất hiện (modal, không thể đóng dễ dàng)
- Giải số lượng bài toán số học yêu cầu (cộng hoặc trừ)
- Nhập đáp án đúng cho mỗi bài toán
- Báo thức sẽ tiếp tục kêu cho đến khi bạn giải đúng tất cả bài toán
- Tiến độ được hiển thị: "X/Y bài đã giải đúng"

### Tính năng Text-to-Speech

- Click nút "🔊 Đọc Thời Gian" để nghe thời gian hiện tại được đọc to
- Yêu cầu cài đặt `pyttsx3`

## 🔨 Tạo file thực thi (Tùy chọn)

Để tạo file thực thi độc lập:

1. PyInstaller đã được cài đặt từ `requirements.txt`

2. Tạo file thực thi bằng spec file:

```bash
pyinstaller alarm_clock.spec
```

Hoặc tạo trực tiếp:

```bash
pyinstaller --onefile --console alarm_clock.py
```

**Lưu ý**: Spec file sử dụng `console=True` để hiển thị console output. Để tạo không có console, thay đổi `console=False` trong spec file.

File thực thi sẽ được tạo trong thư mục `dist`.

## 🧪 Test nhận diện tư thế (Thử nghiệm)

Dự án bao gồm file test cho nhận diện tư thế sử dụng MediaPipe:

```bash
python test_pose_detection.py
```

Tính năng này hiện đang thử nghiệm và chưa được tích hợp vào ứng dụng báo thức chính. Yêu cầu:

- `opencv-python>=4.5.0`
- `mediapipe>=0.10.0`

Cài đặt dependencies cho test:

```bash
pip install -r requirements_test.txt
```

## 📝 Lưu ý

- **Tự động điều chỉnh ngày**: Báo thức sẽ tự động đặt cho ngày hôm sau nếu thời gian đã chọn đã qua trong ngày hôm nay
- **Thử thách toán học**: Ngăn việc tắt báo thức nhầm. Bạn phải giải đúng tất cả bài toán yêu cầu để tắt báo thức
- **Chu kỳ ngủ**: Dựa trên chu kỳ REM 90 phút. 4-6 chu kỳ (6-9 giờ) được khuyến nghị để nghỉ ngơi tối ưu
- **Lưu trữ dữ liệu**: Báo thức được lưu vào `alarms_data.json` trong thư mục dự án
- **Định dạng âm thanh**: Các định dạng được hỗ trợ là MP3, WAV và OGG
- **Nhiều báo thức**: Bạn có thể tạo không giới hạn báo thức, mỗi báo thức có cài đặt riêng
- **Text-to-Speech**: Tính năng tùy chọn. Nếu pyttsx3 không được cài đặt, nút TTS sẽ không xuất hiện

## 🐛 Khắc phục sự cố

- **Không có âm thanh**:

  - Đảm bảo bạn đã chọn file âm thanh hợp lệ
  - Kiểm tra pygame đã được cài đặt đúng: `pip install pygame`
  - Xác minh đường dẫn file âm thanh đúng và có thể truy cập

- **Cửa sổ không hiển thị**:

  - Kiểm tra tkinter đã được cài đặt chưa (thường đi kèm với Python)
  - Trên Linux, bạn có thể cần cài đặt: `sudo apt-get install python3-tk`

- **Thử thách toán học cứ xuất hiện**:

  - Đảm bảo nhập đáp án đúng dưới dạng số
  - Bạn phải giải đúng TẤT CẢ bài toán yêu cầu (kiểm tra chỉ báo tiến độ)

- **TTS không hoạt động**:

  - Cài đặt pyttsx3: `pip install pyttsx3`
  - Trên Linux, bạn có thể cần dependencies bổ sung: `sudo apt-get install espeak`

- **Báo thức không lưu**:

  - Kiểm tra quyền file trong thư mục dự án
  - Đảm bảo `alarms_data.json` không ở chế độ chỉ đọc

- **Máy tính chu kỳ ngủ không hoạt động**:
  - Đảm bảo bạn nhập thời gian hợp lệ (0-23 cho giờ, 0-59 cho phút)
  - Click nút "Tính toán" sau khi nhập thời gian
