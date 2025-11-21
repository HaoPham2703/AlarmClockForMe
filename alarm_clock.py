import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pygame
import threading
import random
from datetime import datetime, timedelta
import time
import math

class AnalogClock:
    def __init__(self, parent, size=200):
        self.size = size
        self.center_x = size // 2
        self.center_y = size // 2
        self.radius = size // 2 - 20
        
        # Canvas để vẽ đồng hồ
        self.canvas = tk.Canvas(parent, width=size, height=size, 
                                bg="white", highlightthickness=0)
        self.canvas.pack()
        
        # Giờ và phút hiện tại (12h format)
        self.hour_12 = 7
        self.minute = 0
        self.is_am = True  # True = AM, False = PM
        
        # Trạng thái kéo kim
        self.dragging = False
        self.drag_type = None  # 'hour' hoặc 'minute'
        
        # Bind events
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        
        self.draw_clock()
        
    def draw_clock(self):
        self.canvas.delete("all")
        
        # Vẽ vòng tròn ngoài
        self.canvas.create_oval(
            self.center_x - self.radius,
            self.center_y - self.radius,
            self.center_x + self.radius,
            self.center_y + self.radius,
            outline="#333", width=3, fill="#f8f8f8"
        )
        
        # Vẽ các số giờ
        for i in range(1, 13):
            angle = math.radians(i * 30 - 90)  # 12 giờ ở trên
            x = self.center_x + (self.radius - 25) * math.cos(angle)
            y = self.center_y + (self.radius - 25) * math.sin(angle)
            self.canvas.create_text(x, y, text=str(i), 
                                   font=("Arial", 14, "bold"), fill="#333")
        
        # Vẽ các vạch phút
        for i in range(60):
            angle = math.radians(i * 6 - 90)
            if i % 5 == 0:
                # Vạch lớn cho giờ
                start_radius = self.radius - 10
                end_radius = self.radius - 5
            else:
                # Vạch nhỏ cho phút
                start_radius = self.radius - 5
                end_radius = self.radius - 2
            
            x1 = self.center_x + start_radius * math.cos(angle)
            y1 = self.center_y + start_radius * math.sin(angle)
            x2 = self.center_x + end_radius * math.cos(angle)
            y2 = self.center_y + end_radius * math.sin(angle)
            self.canvas.create_line(x1, y1, x2, y2, fill="#666", width=1)
        
        # Vẽ kim giờ
        hour_angle = math.radians(self.hour_12 * 30 + self.minute * 0.5 - 90)
        hour_length = self.radius * 0.5
        hour_x = self.center_x + hour_length * math.cos(hour_angle)
        hour_y = self.center_y + hour_length * math.sin(hour_angle)
        self.canvas.create_line(
            self.center_x, self.center_y, hour_x, hour_y,
            fill="#333", width=4, arrow=tk.LAST, arrowshape=(10, 12, 3),
            tags="hour_hand"
        )
        
        # Vẽ kim phút
        minute_angle = math.radians(self.minute * 6 - 90)
        minute_length = self.radius * 0.7
        minute_x = self.center_x + minute_length * math.cos(minute_angle)
        minute_y = self.center_y + minute_length * math.sin(minute_angle)
        self.canvas.create_line(
            self.center_x, self.center_y, minute_x, minute_y,
            fill="#d32f2f", width=3, arrow=tk.LAST, arrowshape=(12, 15, 3),
            tags="minute_hand"
        )
        
        # Vẽ tâm đồng hồ
        self.canvas.create_oval(
            self.center_x - 8, self.center_y - 8,
            self.center_x + 8, self.center_y + 8,
            fill="#333", outline="#333"
        )
        
        # Hiển thị thời gian dạng số với AM/PM
        am_pm = "AM" if self.is_am else "PM"
        time_str = f"{self.hour_12}:{self.minute:02d} {am_pm}"
        self.canvas.create_text(
            self.center_x, self.center_y + self.radius + 20,
            text=time_str, font=("Arial", 14, "bold"), fill="#333"
        )
        
    def on_click(self, event):
        dx = event.x - self.center_x
        dy = event.y - self.center_y
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance < 10:  # Click vào tâm
            return
            
        angle = math.degrees(math.atan2(dy, dx)) + 90
        if angle < 0:
            angle += 360
            
        # Xác định click vào kim nào (dựa vào khoảng cách)
        minute_angle = self.minute * 6
        hour_angle = self.hour_12 * 30 + self.minute * 0.5
        
        # Tính góc từ tâm đến điểm click
        click_angle = angle
        
        # Tính khoảng cách góc
        minute_diff = min(abs(click_angle - minute_angle), 
                         360 - abs(click_angle - minute_angle))
        hour_diff = min(abs(click_angle - hour_angle), 
                       360 - abs(click_angle - hour_angle))
        
        if minute_diff < hour_diff and distance > self.radius * 0.4:
            self.dragging = True
            self.drag_type = 'minute'
        elif distance > self.radius * 0.3:
            self.dragging = True
            self.drag_type = 'hour'
            
    def on_drag(self, event):
        if not self.dragging:
            return
            
        dx = event.x - self.center_x
        dy = event.y - self.center_y
        angle = math.degrees(math.atan2(dy, dx)) + 90
        if angle < 0:
            angle += 360
            
        if self.drag_type == 'minute':
            self.minute = int(angle / 6) % 60
        elif self.drag_type == 'hour':
            self.hour_12 = int(angle / 30) % 12
            if self.hour_12 == 0:
                self.hour_12 = 12
                
        self.draw_clock()
        
    def on_release(self, event):
        self.dragging = False
        self.drag_type = None
        
    def get_time(self):
        # Chuyển đổi từ 12h sang 24h
        hour_24 = self.hour_12
        if not self.is_am and self.hour_12 != 12:
            hour_24 = self.hour_12 + 12
        elif self.is_am and self.hour_12 == 12:
            hour_24 = 0
        return hour_24, self.minute
        
    def set_time(self, hour, minute):
        # Chuyển đổi từ 24h sang 12h
        if hour == 0:
            self.hour_12 = 12
            self.is_am = True
        elif hour < 12:
            self.hour_12 = hour
            self.is_am = True
        elif hour == 12:
            self.hour_12 = 12
            self.is_am = False
        else:
            self.hour_12 = hour - 12
            self.is_am = False
        self.minute = minute
        self.draw_clock()
        
    def toggle_am_pm(self):
        self.is_am = not self.is_am
        self.draw_clock()

class AlarmClock:
    def __init__(self, root):
        self.root = root
        self.root.title("Báo Thức Python")
        self.root.geometry("600x700")
        self.root.minsize(500, 600)  # Kích thước tối thiểu
        self.root.resizable(True, True)  # Cho phép resize
        
        # Khởi tạo pygame mixer
        pygame.mixer.init()
        self.alarm_sound = None
        self.is_alarm_playing = False
        self.alarm_thread = None
        
        # Biến lưu trữ
        self.alarm_time = None
        self.alarm_file = None
        
        self.setup_ui()
        self.update_time()
        self.update_am_pm_button()
        
    def setup_ui(self):
        # Tạo Canvas với Scrollbar để có thể scroll
        self.canvas = tk.Canvas(self.root, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        scrollable_frame = ttk.Frame(self.canvas)
        
        # Cấu hình scroll
        def configure_scroll_region(event=None):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
        scrollable_frame.bind("<Configure>", configure_scroll_region)
        
        self.canvas_window = self.canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        # Đảm bảo canvas window mở rộng với canvas
        def configure_canvas_width(event):
            canvas_width = event.width
            self.canvas.itemconfig(self.canvas_window, width=canvas_width)
        self.canvas.bind('<Configure>', configure_canvas_width)
        
        # Pack canvas và scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mouse wheel để scroll (hỗ trợ cả Windows và Linux)
        def _on_mousewheel(event):
            # Windows và MacOS
            if event.num == 4 or event.delta > 0:
                self.canvas.yview_scroll(-1, "units")
            elif event.num == 5 or event.delta < 0:
                self.canvas.yview_scroll(1, "units")
        
        # Windows
        self.canvas.bind_all("<MouseWheel>", _on_mousewheel)
        # Linux
        self.canvas.bind_all("<Button-4>", _on_mousewheel)
        self.canvas.bind_all("<Button-5>", _on_mousewheel)
        
        # Frame chính trong scrollable_frame
        main_frame = ttk.Frame(scrollable_frame, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Tiêu đề
        title_label = ttk.Label(main_frame, text="⏰ BÁO THỨC", 
                               font=("Arial", 24, "bold"))
        title_label.pack(pady=5)
        
        # Hiển thị thời gian hiện tại
        self.time_label = ttk.Label(main_frame, text="00:00:00", 
                                    font=("Arial", 32, "bold"))
        self.time_label.pack(pady=10)
        
        # Frame chọn thời gian báo thức với đồng hồ kim
        time_frame = ttk.LabelFrame(main_frame, text="Thiết lập thời gian báo thức", padding="15")
        time_frame.pack(fill=tk.X, pady=5)
        
        # Tạo đồng hồ analog
        clock_container = ttk.Frame(time_frame)
        clock_container.pack(pady=5)
        self.analog_clock = AnalogClock(clock_container, size=220)
        
        # Nút chuyển đổi AM/PM
        am_pm_frame = ttk.Frame(time_frame)
        am_pm_frame.pack(pady=5)
        ttk.Label(am_pm_frame, text="Chế độ:", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        self.am_pm_button = ttk.Button(
            am_pm_frame, 
            text="AM", 
            command=self.toggle_am_pm,
            width=8
        )
        self.am_pm_button.pack(side=tk.LEFT, padx=5)
        
        # Hướng dẫn sử dụng
        instruction_label = ttk.Label(
            time_frame, 
            text="💡 Kéo kim giờ/phút để đặt thời gian | Click AM/PM để chuyển đổi",
            font=("Arial", 9),
            foreground="gray"
        )
        instruction_label.pack(pady=5)
        
        # Chọn file nhạc
        music_frame = ttk.LabelFrame(main_frame, text="Chọn nhạc chuông", padding="15")
        music_frame.pack(fill=tk.X, pady=5)
        
        self.music_label = ttk.Label(music_frame, text="Chưa chọn file nhạc", 
                                     foreground="gray")
        self.music_label.pack(pady=3)
        
        ttk.Button(music_frame, text="Chọn file nhạc", 
                  command=self.select_music_file).pack(pady=3)
        
        # Nút bật/tắt báo thức
        self.alarm_button = ttk.Button(main_frame, text="Bật Báo Thức", 
                                      command=self.toggle_alarm)
        self.alarm_button.pack(pady=15)
        
        # Hiển thị trạng thái báo thức
        self.status_label = ttk.Label(main_frame, text="Báo thức: TẮT", 
                                      font=("Arial", 12))
        self.status_label.pack(pady=3)
        
        # Hiển thị thời gian báo thức đã set
        self.alarm_time_label = ttk.Label(main_frame, text="", 
                                          font=("Arial", 10), foreground="blue")
        self.alarm_time_label.pack(pady=3)
        
        # Thêm padding ở cuối để đảm bảo scroll được hết
        ttk.Label(main_frame, text="").pack(pady=10)
        
    def toggle_am_pm(self):
        self.analog_clock.toggle_am_pm()
        self.update_am_pm_button()
        
    def update_am_pm_button(self):
        am_pm_text = "AM" if self.analog_clock.is_am else "PM"
        self.am_pm_button.config(text=am_pm_text)
        
    def select_music_file(self):
        file_path = filedialog.askopenfilename(
            title="Chọn file nhạc",
            filetypes=[
                ("Audio files", "*.mp3 *.wav *.ogg"),
                ("MP3 files", "*.mp3"),
                ("WAV files", "*.wav"),
                ("OGG files", "*.ogg"),
                ("All files", "*.*")
            ]
        )
        if file_path:
            self.alarm_file = file_path
            filename = file_path.split("/")[-1] if "/" in file_path else file_path.split("\\")[-1]
            self.music_label.config(text=f"✓ {filename}", foreground="green")
            
    def toggle_alarm(self):
        if self.is_alarm_playing:
            # Đang báo thức, không cho tắt từ đây
            messagebox.showinfo("Thông báo", 
                              "Báo thức đang kêu! Hãy giải bài toán để tắt.")
            return
            
        if self.alarm_file is None:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn file nhạc trước!")
            return
            
        try:
            hour, minute = self.analog_clock.get_time()
            
            if hour < 0 or hour > 23 or minute < 0 or minute > 59:
                raise ValueError("Giờ hoặc phút không hợp lệ")
                
            # Tính thời gian báo thức
            now = datetime.now()
            alarm_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            
            # Nếu thời gian đã qua trong ngày hôm nay, set cho ngày mai
            if alarm_time <= now:
                alarm_time += timedelta(days=1)
                
            self.alarm_time = alarm_time
            self.status_label.config(text="Báo thức: BẬT", foreground="green")
            self.alarm_time_label.config(
                text=f"Báo thức sẽ kêu lúc: {alarm_time.strftime('%H:%M:%S - %d/%m/%Y')}"
            )
            self.alarm_button.config(text="Hủy Báo Thức")
            
            # Bắt đầu thread kiểm tra báo thức
            if self.alarm_thread is None or not self.alarm_thread.is_alive():
                self.alarm_thread = threading.Thread(target=self.check_alarm, daemon=True)
                self.alarm_thread.start()
                
        except ValueError as e:
            messagebox.showerror("Lỗi", f"Thời gian không hợp lệ: {e}")
            
    def check_alarm(self):
        while self.alarm_time is not None:
            now = datetime.now()
            if now >= self.alarm_time and not self.is_alarm_playing:
                self.start_alarm()
                break
            time.sleep(1)
            
    def start_alarm(self):
        self.is_alarm_playing = True
        self.status_label.config(text="Báo thức: ĐANG KÊU!", foreground="red")
        
        # Phát nhạc trong thread riêng
        sound_thread = threading.Thread(target=self.play_alarm_sound, daemon=True)
        sound_thread.start()
        
        # Hiển thị cửa sổ giải toán
        self.show_math_challenge()
        
    def play_alarm_sound(self):
        try:
            pygame.mixer.music.load(self.alarm_file)
            pygame.mixer.music.play(-1)  # -1 để loop vô hạn
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể phát nhạc: {e}")
            self.is_alarm_playing = False
            
    def show_math_challenge(self):
        # Tạo cửa sổ mới để giải toán
        challenge_window = tk.Toplevel(self.root)
        challenge_window.title("Tắt Báo Thức - Phải giải đúng mới tắt được!")
        challenge_window.geometry("400x350")
        challenge_window.resizable(False, False)
        
        # Đặt cửa sổ lên trên cùng
        challenge_window.attributes('-topmost', True)
        challenge_window.grab_set()  # Modal window
        
        # Xử lý khi đóng cửa sổ - tự động hiện lại cửa sổ mới
        def on_closing():
            challenge_window.destroy()
            # Tự động hiện lại cửa sổ giải toán mới
            self.root.after(100, self.show_math_challenge)
        
        challenge_window.protocol("WM_DELETE_WINDOW", on_closing)
        
        # Tạo bài toán
        num1 = random.randint(1, 50)
        num2 = random.randint(1, 50)
        operation = random.choice(['+', '-'])
        
        if operation == '+':
            correct_answer = num1 + num2
            question = f"{num1} + {num2} = ?"
        else:
            # Đảm bảo kết quả không âm
            if num1 < num2:
                num1, num2 = num2, num1
            correct_answer = num1 - num2
            question = f"{num1} - {num2} = ?"
            
        # Frame chính
        main_frame = ttk.Frame(challenge_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Cảnh báo
        warning_label = ttk.Label(
            main_frame, 
            text="⚠️ Bạn phải giải đúng bài toán để tắt báo thức!",
            font=("Arial", 10, "bold"),
            foreground="red"
        )
        warning_label.pack(pady=5)
        
        # Hiển thị câu hỏi
        question_label = ttk.Label(main_frame, text=question, 
                                  font=("Arial", 24, "bold"))
        question_label.pack(pady=20)
        
        # Nhập đáp án
        answer_frame = ttk.Frame(main_frame)
        answer_frame.pack(pady=20)
        
        ttk.Label(answer_frame, text="Đáp án:").pack(side=tk.LEFT, padx=5)
        answer_var = tk.StringVar()
        answer_entry = ttk.Entry(answer_frame, textvariable=answer_var, 
                                font=("Arial", 16), width=10)
        answer_entry.pack(side=tk.LEFT, padx=5)
        answer_entry.focus()
        
        # Hàm kiểm tra đáp án
        def check_answer():
            try:
                user_answer = int(answer_var.get())
                if user_answer == correct_answer:
                    # Đáp án đúng - tắt báo thức
                    self.stop_alarm()
                    challenge_window.destroy()
                    messagebox.showinfo("Thành công", "Báo thức đã được tắt!")
                else:
                    # Đáp án sai - tạo bài toán mới
                    messagebox.showwarning("Sai rồi!", "Hãy thử lại!")
                    challenge_window.destroy()
                    self.show_math_challenge()
            except ValueError:
                messagebox.showwarning("Lỗi", "Vui lòng nhập số!")
                
        # Nút xác nhận
        submit_button = ttk.Button(main_frame, text="Xác nhận", 
                                  command=check_answer)
        submit_button.pack(pady=10)
        
        # Cho phép Enter để submit
        answer_entry.bind('<Return>', lambda e: check_answer())
        
    def stop_alarm(self):
        pygame.mixer.music.stop()
        self.is_alarm_playing = False
        self.alarm_time = None
        self.status_label.config(text="Báo thức: TẮT", foreground="black")
        self.alarm_time_label.config(text="")
        self.alarm_button.config(text="Bật Báo Thức")
        
    def update_time(self):
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_label.config(text=current_time)
        self.root.after(1000, self.update_time)

def main():
    root = tk.Tk()
    app = AlarmClock(root)
    root.mainloop()

if __name__ == "__main__":
    main()

