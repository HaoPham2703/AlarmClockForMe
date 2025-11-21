import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pygame
import threading
import random
from datetime import datetime, timedelta
import time
import math
import uuid
import json
import os
try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False

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
        self.root.geometry("700x600")
        self.root.minsize(600, 500)
        self.root.resizable(True, True)
        
        # Khởi tạo pygame mixer
        pygame.mixer.init()
        
        # Khởi tạo text-to-speech engine
        self.tts_engine = None
        if TTS_AVAILABLE:
            try:
                self.tts_engine = pyttsx3.init()
                # Thiết lập tốc độ đọc
                self.tts_engine.setProperty('rate', 150)
                # Tự động chọn voice phù hợp (ưu tiên tiếng Việt nếu có)
                voices = self.tts_engine.getProperty('voices')
                if voices:
                    # Tìm voice tiếng Việt hoặc dùng voice đầu tiên
                    for voice in voices:
                        if 'vietnamese' in voice.languages or 'vi' in str(voice.languages).lower():
                            self.tts_engine.setProperty('voice', voice.id)
                            break
                    else:
                        # Nếu không tìm thấy, dùng voice đầu tiên
                        self.tts_engine.setProperty('voice', voices[0].id)
            except Exception as e:
                print(f"Không thể khởi tạo TTS engine: {e}")
                self.tts_engine = None
        
        # Quản lý nhiều báo thức
        self.alarms = {}  # {alarm_id: alarm_data}
        
        # File lưu trữ dữ liệu
        self.data_file = "alarms_data.json"
        
        # Trạng thái báo thức đang kêu
        self.active_alarm_id = None
        self.is_alarm_playing = False
        self.alarm_thread = None
        
        # Trạng thái view hiện tại
        self.current_view = 'list'  # 'list' hoặc 'detail'
        self.editing_alarm_id = None  # None nếu là tạo mới
        self.sleep_cycle_result = None  # Kết quả tính toán chu kỳ ngủ
        
        # Load dữ liệu từ file
        self.load_alarms()
        
        self.setup_ui()
        self.update_time()
        self.start_alarm_checker()
        
        # Lưu dữ liệu khi đóng ứng dụng
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_ui(self):
        # Frame container chính
        self.main_container = ttk.Frame(self.root)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Tạo cả 2 view nhưng chỉ hiển thị 1 cái
        self.setup_list_view()
        self.setup_detail_view()
        
        # Hiển thị list view mặc định
        self.show_list_view()
    
    def setup_list_view(self):
        """Thiết lập giao diện danh sách báo thức"""
        self.list_view_frame = ttk.Frame(self.main_container, padding="20")
        
        # Tiêu đề
        title_label = ttk.Label(self.list_view_frame, text="⏰ DANH SÁCH BÁO THỨC", 
                               font=("Arial", 24, "bold"))
        title_label.pack(pady=5)
        
        # Hiển thị thời gian hiện tại
        self.time_label = ttk.Label(self.list_view_frame, text="00:00:00", 
                                    font=("Arial", 28, "bold"))
        self.time_label.pack(pady=10)
        
        # Frame chứa các nút
        button_frame = ttk.Frame(self.list_view_frame)
        button_frame.pack(pady=10)
        
        # Nút thêm báo thức mới
        add_button = ttk.Button(button_frame, text="➕ Thêm Báo Thức Mới", 
                               command=self.add_new_alarm)
        add_button.pack(side=tk.LEFT, padx=5)
        
        # Nút đọc thời gian (chỉ hiển thị nếu TTS khả dụng)
        if self.tts_engine:
            speak_button = ttk.Button(button_frame, text="🔊 Đọc Thời Gian", 
                                     command=self.read_current_time)
            speak_button.pack(side=tk.LEFT, padx=5)
        
        # Frame danh sách báo thức với scroll
        list_frame = ttk.LabelFrame(self.list_view_frame, text="Danh sách báo thức", padding="10")
        list_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Canvas với scrollbar cho danh sách
        self.list_canvas = tk.Canvas(list_frame, highlightthickness=0)
        list_scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.list_canvas.yview)
        self.list_scrollable_frame = ttk.Frame(self.list_canvas)
        
        def configure_list_scroll(event=None):
            self.list_canvas.configure(scrollregion=self.list_canvas.bbox("all"))
        
        self.list_scrollable_frame.bind("<Configure>", configure_list_scroll)
        
        self.list_canvas_window = self.list_canvas.create_window((0, 0), window=self.list_scrollable_frame, anchor="nw")
        self.list_canvas.configure(yscrollcommand=list_scrollbar.set)
        
        def configure_list_canvas_width(event):
            canvas_width = event.width
            self.list_canvas.itemconfig(self.list_canvas_window, width=canvas_width)
        self.list_canvas.bind('<Configure>', configure_list_canvas_width)
        
        self.list_canvas.pack(side="left", fill="both", expand=True)
        list_scrollbar.pack(side="right", fill="y")
        
        # Bind mouse wheel
        def _on_mousewheel(event):
            if event.num == 4 or event.delta > 0:
                self.list_canvas.yview_scroll(-1, "units")
            elif event.num == 5 or event.delta < 0:
                self.list_canvas.yview_scroll(1, "units")
        
        self.list_canvas.bind_all("<MouseWheel>", _on_mousewheel)
        self.list_canvas.bind_all("<Button-4>", _on_mousewheel)
        self.list_canvas.bind_all("<Button-5>", _on_mousewheel)
        
        # Container để chứa các item báo thức
        self.alarms_container = self.list_scrollable_frame
    
    def setup_detail_view(self):
        """Thiết lập giao diện chi tiết báo thức"""
        self.detail_view_frame = ttk.Frame(self.main_container, padding="20")
        
        # Frame chính với scroll
        detail_canvas = tk.Canvas(self.detail_view_frame, highlightthickness=0)
        detail_scrollbar = ttk.Scrollbar(self.detail_view_frame, orient="vertical", command=detail_canvas.yview)
        detail_scrollable_frame = ttk.Frame(detail_canvas)
        
        def configure_detail_scroll(event=None):
            detail_canvas.configure(scrollregion=detail_canvas.bbox("all"))
        
        detail_scrollable_frame.bind("<Configure>", configure_detail_scroll)
        
        detail_canvas_window = detail_canvas.create_window((0, 0), window=detail_scrollable_frame, anchor="nw")
        detail_canvas.configure(yscrollcommand=detail_scrollbar.set)
        
        def configure_detail_canvas_width(event):
            canvas_width = event.width
            detail_canvas.itemconfig(detail_canvas_window, width=canvas_width)
        detail_canvas.bind('<Configure>', configure_detail_canvas_width)
        
        detail_canvas.pack(side="left", fill="both", expand=True)
        detail_scrollbar.pack(side="right", fill="y")
        
        # Bind mouse wheel
        def _on_mousewheel_detail(event):
            if event.num == 4 or event.delta > 0:
                detail_canvas.yview_scroll(-1, "units")
            elif event.num == 5 or event.delta < 0:
                detail_canvas.yview_scroll(1, "units")
        
        detail_canvas.bind_all("<MouseWheel>", _on_mousewheel_detail)
        detail_canvas.bind_all("<Button-4>", _on_mousewheel_detail)
        detail_canvas.bind_all("<Button-5>", _on_mousewheel_detail)
        
        # Frame chính trong scrollable
        main_detail_frame = ttk.Frame(detail_scrollable_frame, padding="20")
        main_detail_frame.pack(fill=tk.BOTH, expand=True)
        
        # Nút Back
        back_button = ttk.Button(main_detail_frame, text="← Quay lại", 
                                command=self.show_list_view)
        back_button.pack(anchor=tk.W, pady=5)
        
        # Tiêu đề
        self.detail_title_label = ttk.Label(main_detail_frame, text="➕ Thêm báo thức mới", 
                               font=("Arial", 20, "bold"))
        self.detail_title_label.pack(pady=10)
        
        # Hiển thị thời gian hiện tại (giống như trang list)
        self.detail_time_label = ttk.Label(main_detail_frame, text="00:00:00", 
                                          font=("Arial", 28, "bold"))
        self.detail_time_label.pack(pady=10)
        
        # Tên báo thức (tùy chọn)
        name_frame = ttk.LabelFrame(main_detail_frame, text="Tên báo thức (tùy chọn)", padding="10")
        name_frame.pack(fill=tk.X, pady=5)
        
        self.name_var = tk.StringVar()
        name_entry = ttk.Entry(name_frame, textvariable=self.name_var, font=("Arial", 11))
        name_entry.pack(fill=tk.X, pady=3)
        
        # Frame tính toán chu kỳ ngủ
        sleep_cycle_frame = ttk.LabelFrame(main_detail_frame, text="💤 Tính toán chu kỳ ngủ (90 phút/chu kỳ)", padding="15")
        sleep_cycle_frame.pack(fill=tk.X, pady=5)
        
        # Chọn mode tính toán
        mode_frame = ttk.Frame(sleep_cycle_frame)
        mode_frame.pack(fill=tk.X, pady=5)
        
        self.sleep_mode_var = tk.StringVar(value="wake")
        ttk.Radiobutton(mode_frame, text="Tính từ thời gian muốn dậy", 
                       variable=self.sleep_mode_var, value="wake",
                       command=self.update_sleep_cycle_ui).pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(mode_frame, text="Tính từ thời gian muốn ngủ", 
                       variable=self.sleep_mode_var, value="sleep",
                       command=self.update_sleep_cycle_ui).pack(side=tk.LEFT, padx=10)
        
        # Frame nhập thời gian
        time_input_frame = ttk.Frame(sleep_cycle_frame)
        time_input_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(time_input_frame, text="Giờ:", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        self.sleep_hour_var = tk.StringVar(value="07")
        hour_spinbox = ttk.Spinbox(time_input_frame, from_=0, to=23, width=5,
                                   textvariable=self.sleep_hour_var, format="%02.0f")
        hour_spinbox.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(time_input_frame, text="Phút:", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        self.sleep_minute_var = tk.StringVar(value="00")
        minute_spinbox = ttk.Spinbox(time_input_frame, from_=0, to=59, width=5,
                                     textvariable=self.sleep_minute_var, format="%02.0f")
        minute_spinbox.pack(side=tk.LEFT, padx=5)
        
        # Nút tính toán
        calc_button = ttk.Button(sleep_cycle_frame, text="Tính toán", 
                                command=self.calculate_sleep_cycle)
        calc_button.pack(pady=5)
        
        # Frame chứa kết quả các chu kỳ
        self.sleep_results_frame = ttk.Frame(sleep_cycle_frame)
        self.sleep_results_frame.pack(fill=tk.X, pady=5)
        
        # Label hướng dẫn
        self.sleep_result_label = ttk.Label(sleep_cycle_frame, text="", 
                                           font=("Arial", 10), 
                                           foreground="gray")
        self.sleep_result_label.pack(pady=3)
        
        # Frame chọn thời gian báo thức với đồng hồ kim
        time_frame = ttk.LabelFrame(main_detail_frame, text="Thiết lập thời gian báo thức", padding="15")
        time_frame.pack(fill=tk.X, pady=5)
        
        # Tạo đồng hồ analog
        clock_container = ttk.Frame(time_frame)
        clock_container.pack(pady=5)
        self.analog_clock = AnalogClock(clock_container, size=200)
        
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
        music_frame = ttk.LabelFrame(main_detail_frame, text="Chọn nhạc chuông", padding="15")
        music_frame.pack(fill=tk.X, pady=5)
        
        self.music_label = ttk.Label(music_frame, text="Chưa chọn file nhạc", 
                                     foreground="gray")
        self.music_label.pack(pady=3)
        
        ttk.Button(music_frame, text="Chọn file nhạc", 
                  command=self.select_music_file).pack(pady=3)
        
        # Cài đặt số lượng bài toán
        math_frame = ttk.LabelFrame(main_detail_frame, text="🔢 Cài đặt thử thách toán học", padding="15")
        math_frame.pack(fill=tk.X, pady=5)
        
        math_setting_frame = ttk.Frame(math_frame)
        math_setting_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(math_setting_frame, text="Số lượng bài toán cần giải đúng:", 
                 font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        self.math_count_var = tk.IntVar(value=1)
        math_spinbox = ttk.Spinbox(math_setting_frame, from_=1, to=10, width=5,
                                   textvariable=self.math_count_var)
        math_spinbox.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(math_setting_frame, text="(Phải giải đúng tất cả mới tắt được báo thức)", 
                 font=("Arial", 9), foreground="gray").pack(side=tk.LEFT, padx=5)
        
        # Nút lưu và hủy
        button_frame = ttk.Frame(main_detail_frame)
        button_frame.pack(pady=15)
        
        ttk.Button(button_frame, text="Lưu", 
                  command=self.save_alarm, width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Hủy", 
                  command=self.show_list_view, width=15).pack(side=tk.LEFT, padx=5)
        
        # Padding cuối
        ttk.Label(main_detail_frame, text="").pack(pady=10)
        
        # Lưu reference để có thể truy cập sau
        self.detail_alarm_file = None
    
    def show_list_view(self):
        """Hiển thị view danh sách"""
        self.current_view = 'list'
        self.detail_view_frame.pack_forget()
        self.list_view_frame.pack(fill=tk.BOTH, expand=True)
        self.refresh_alarm_list()
    
    def show_detail_view(self, alarm_id=None, alarm_data=None):
        """Hiển thị view chi tiết"""
        self.current_view = 'detail'
        self.editing_alarm_id = alarm_id
        self.list_view_frame.pack_forget()
        self.detail_view_frame.pack(fill=tk.BOTH, expand=True)
        
        # Cập nhật tiêu đề
        if alarm_id:
            self.detail_title_label.config(text="✏️ Chỉnh sửa báo thức")
        else:
            self.detail_title_label.config(text="➕ Thêm báo thức mới")
        
        # Reset form
        self.name_var.set("")
        self.analog_clock.set_time(7, 0)
        self.analog_clock.is_am = True
        self.analog_clock.draw_clock()
        self.music_label.config(text="Chưa chọn file nhạc", foreground="gray")
        self.detail_alarm_file = None
        self.math_count_var.set(1)  # Mặc định 1 bài toán
        self.update_am_pm_button()
        
        # Reset tính toán chu kỳ ngủ
        self.sleep_mode_var.set("wake")
        self.sleep_hour_var.set("07")
        self.sleep_minute_var.set("00")
        self.clear_sleep_results()
        self.sleep_cycle_result = None
        
        # Load dữ liệu nếu đang chỉnh sửa
        if alarm_data:
            self.load_alarm_data_to_form(alarm_data)
    
    def load_alarm_data_to_form(self, alarm_data):
        """Load dữ liệu báo thức vào form"""
        # Load tên
        if 'name' in alarm_data and alarm_data['name']:
            self.name_var.set(alarm_data['name'])
        
        # Load thời gian
        if 'time' in alarm_data:
            hour, minute = alarm_data['time']
            self.analog_clock.set_time(hour, minute)
        
        # Load file nhạc
        if 'file' in alarm_data and alarm_data['file']:
            self.detail_alarm_file = alarm_data['file']
            filename = self.detail_alarm_file.split("/")[-1] if "/" in self.detail_alarm_file else self.detail_alarm_file.split("\\")[-1]
            self.music_label.config(text=f"✓ {filename}", foreground="green")
        
        # Load số lượng bài toán
        if 'math_count' in alarm_data:
            self.math_count_var.set(alarm_data['math_count'])
        else:
            self.math_count_var.set(1)  # Mặc định 1 nếu không có
        
        self.update_am_pm_button()
    
    def toggle_am_pm(self):
        self.analog_clock.toggle_am_pm()
        self.update_am_pm_button()
    
    def update_am_pm_button(self):
        am_pm_text = "AM" if self.analog_clock.is_am else "PM"
        self.am_pm_button.config(text=am_pm_text)
    
    def update_sleep_cycle_ui(self):
        """Cập nhật UI khi đổi mode tính toán chu kỳ ngủ"""
        # Reset kết quả khi đổi mode
        self.clear_sleep_results()
        self.sleep_cycle_result = None
    
    def clear_sleep_results(self):
        """Xóa tất cả kết quả hiển thị"""
        for widget in self.sleep_results_frame.winfo_children():
            widget.destroy()
        self.sleep_result_label.config(text="")
    
    def calculate_sleep_cycle(self):
        """Tính toán chu kỳ ngủ - hiển thị tất cả các option"""
        try:
            hour = int(self.sleep_hour_var.get())
            minute = int(self.sleep_minute_var.get())
            
            if hour < 0 or hour > 23 or minute < 0 or minute > 59:
                raise ValueError("Giờ hoặc phút không hợp lệ")
            
            # Xóa kết quả cũ
            self.clear_sleep_results()
            
            # Tạo datetime từ thời gian nhập
            now = datetime.now()
            target_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            
            mode = self.sleep_mode_var.get()
            
            if mode == "wake":
                # Tính từ thời gian muốn dậy -> tính thời gian nên ngủ
                # Nếu thời gian dậy là hôm nay và đã qua, tính cho ngày mai
                if target_time <= now:
                    target_time += timedelta(days=1)
                
                # Hiển thị tiêu đề
                title_text = f"⏰ Để dậy lúc {hour:02d}:{minute:02d}, bạn có thể ngủ vào các thời gian sau:"
                self.sleep_result_label.config(text=title_text, foreground="blue", font=("Arial", 11, "bold"))
                
                # Tính toán và hiển thị tất cả các chu kỳ (3-8)
                for cycles in range(3, 9):
                    cycle_minutes = cycles * 90
                    cycle_delta = timedelta(minutes=cycle_minutes)
                    sleep_time = target_time - cycle_delta
                    
                    # Tạo frame cho mỗi option
                    option_frame = ttk.Frame(self.sleep_results_frame, relief=tk.RAISED, borderwidth=1)
                    option_frame.pack(fill=tk.X, pady=3, padx=5)
                    
                    # Nội dung option
                    content_frame = ttk.Frame(option_frame, padding="8")
                    content_frame.pack(fill=tk.X)
                    
                    # Thông tin chu kỳ
                    info_text = f"{cycles} chu kỳ ({cycle_minutes // 60}h{cycle_minutes % 60:02d}p)"
                    if 4 <= cycles <= 6:
                        info_text += " ⭐ Khuyến nghị"
                    
                    info_label = ttk.Label(content_frame, text=info_text, 
                                          font=("Arial", 10, "bold"))
                    info_label.pack(anchor=tk.W)
                    
                    # Thời gian ngủ
                    sleep_time_str = sleep_time.strftime('%H:%M - %d/%m/%Y')
                    time_label = ttk.Label(content_frame, 
                                          text=f"   Ngủ lúc: {sleep_time_str}", 
                                          font=("Arial", 10))
                    time_label.pack(anchor=tk.W)
                    
                    # Nút áp dụng
                    apply_btn = ttk.Button(content_frame, text="Áp dụng", width=12,
                                         command=lambda c=cycles, st=sleep_time, tt=target_time: 
                                         self.apply_sleep_cycle_option(c, st, tt, mode))
                    apply_btn.pack(anchor=tk.E, pady=2)
                    
            else:
                # Tính từ thời gian muốn ngủ -> tính thời gian sẽ dậy
                # Nếu thời gian ngủ là hôm nay và đã qua, tính cho ngày mai
                if target_time <= now:
                    target_time += timedelta(days=1)
                
                # Hiển thị tiêu đề
                title_text = f"⏰ Nếu ngủ lúc {hour:02d}:{minute:02d}, bạn sẽ dậy vào các thời gian sau:"
                self.sleep_result_label.config(text=title_text, foreground="blue", font=("Arial", 11, "bold"))
                
                # Tính toán và hiển thị tất cả các chu kỳ (3-8)
                for cycles in range(3, 9):
                    cycle_minutes = cycles * 90
                    cycle_delta = timedelta(minutes=cycle_minutes)
                    wake_time = target_time + cycle_delta
                    
                    # Tạo frame cho mỗi option
                    option_frame = ttk.Frame(self.sleep_results_frame, relief=tk.RAISED, borderwidth=1)
                    option_frame.pack(fill=tk.X, pady=3, padx=5)
                    
                    # Nội dung option
                    content_frame = ttk.Frame(option_frame, padding="8")
                    content_frame.pack(fill=tk.X)
                    
                    # Thông tin chu kỳ
                    info_text = f"{cycles} chu kỳ ({cycle_minutes // 60}h{cycle_minutes % 60:02d}p)"
                    if 4 <= cycles <= 6:
                        info_text += " ⭐ Khuyến nghị"
                    
                    info_label = ttk.Label(content_frame, text=info_text, 
                                          font=("Arial", 10, "bold"))
                    info_label.pack(anchor=tk.W)
                    
                    # Thời gian dậy
                    wake_time_str = wake_time.strftime('%H:%M - %d/%m/%Y')
                    time_label = ttk.Label(content_frame, 
                                          text=f"   Dậy lúc: {wake_time_str}", 
                                          font=("Arial", 10))
                    time_label.pack(anchor=tk.W)
                    
                    # Nút áp dụng
                    apply_btn = ttk.Button(content_frame, text="Áp dụng", width=12,
                                         command=lambda c=cycles, wt=wake_time, tt=target_time: 
                                         self.apply_sleep_cycle_option(c, tt, wt, mode))
                    apply_btn.pack(anchor=tk.E, pady=2)
            
        except ValueError as e:
            messagebox.showerror("Lỗi", f"Dữ liệu không hợp lệ: {e}")
            self.clear_sleep_results()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {e}")
            self.clear_sleep_results()
    
    def apply_sleep_cycle_option(self, cycles, sleep_time, wake_time, mode):
        """Áp dụng một option chu kỳ ngủ cụ thể"""
        if mode == "wake":
            # Áp dụng thời gian dậy vào báo thức
            hour, minute = wake_time.hour, wake_time.minute
            self.analog_clock.set_time(hour, minute)
            self.update_am_pm_button()
            
            messagebox.showinfo("Đã áp dụng", 
                              f"Đã đặt thời gian báo thức: {hour:02d}:{minute:02d}\n"
                              f"Bạn nên ngủ lúc: {sleep_time.strftime('%H:%M')}\n"
                              f"Tổng: {cycles} chu kỳ ({cycles * 90 // 60}h{cycles * 90 % 60:02d}p)")
        else:
            # Áp dụng thời gian dậy vào báo thức
            hour, minute = wake_time.hour, wake_time.minute
            self.analog_clock.set_time(hour, minute)
            self.update_am_pm_button()
            
            messagebox.showinfo("Đã áp dụng", 
                              f"Đã đặt thời gian báo thức: {hour:02d}:{minute:02d}\n"
                              f"Bạn sẽ dậy sau {cycles} chu kỳ ngủ\n"
                              f"Tổng: {cycles} chu kỳ ({cycles * 90 // 60}h{cycles * 90 % 60:02d}p)")
    
    
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
            self.detail_alarm_file = file_path
            filename = file_path.split("/")[-1] if "/" in file_path else file_path.split("\\")[-1]
            self.music_label.config(text=f"✓ {filename}", foreground="green")
    
    def save_alarm(self):
        """Lưu báo thức"""
        if self.detail_alarm_file is None:
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
            
            # Tạo dữ liệu báo thức
            alarm_data = {
                'name': self.name_var.get().strip() or None,
                'time': (hour, minute),
                'file': self.detail_alarm_file,
                'alarm_time': alarm_time,
                'enabled': True if not self.editing_alarm_id else self.alarms[self.editing_alarm_id].get('enabled', True),
                'math_count': self.math_count_var.get()  # Số lượng bài toán cần giải
            }
            
            # Lưu vào danh sách
            if self.editing_alarm_id:
                # Cập nhật báo thức hiện có
                self.update_alarm(self.editing_alarm_id, alarm_data)
            else:
                # Tạo báo thức mới
                self.add_alarm(alarm_data)
            
            # Quay về list view
            self.show_list_view()
            
        except ValueError as e:
            messagebox.showerror("Lỗi", f"Thời gian không hợp lệ: {e}")
    
    def add_new_alarm(self):
        """Mở view thêm báo thức mới"""
        self.show_detail_view()
    
    def load_alarms(self):
        """Load dữ liệu báo thức từ file JSON"""
        if not os.path.exists(self.data_file):
            return
        
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Chuyển đổi dữ liệu từ JSON về dict với datetime
            now = datetime.now()
            for alarm_id, alarm_data in data.items():
                # Chuyển đổi alarm_time từ string về datetime
                if 'alarm_time' in alarm_data and alarm_data['alarm_time']:
                    alarm_data['alarm_time'] = datetime.fromisoformat(alarm_data['alarm_time'])
                    # Nếu alarm_time đã qua, tính lại cho ngày tiếp theo
                    if alarm_data['alarm_time'] <= now:
                        hour, minute = alarm_data.get('time', (0, 0))
                        if isinstance(hour, list):
                            hour, minute = tuple(hour)
                        new_alarm_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
                        if new_alarm_time <= now:
                            new_alarm_time += timedelta(days=1)
                        alarm_data['alarm_time'] = new_alarm_time
                # Chuyển đổi time từ list về tuple
                if 'time' in alarm_data and isinstance(alarm_data['time'], list):
                    alarm_data['time'] = tuple(alarm_data['time'])
                
                self.alarms[alarm_id] = alarm_data
            
            # Lưu lại nếu có thay đổi alarm_time
            if data:
                self.save_alarms()
                
        except json.JSONDecodeError:
            print(f"Lỗi: File {self.data_file} bị lỗi định dạng JSON")
        except Exception as e:
            print(f"Lỗi khi load dữ liệu: {e}")
    
    def save_alarms(self):
        """Lưu dữ liệu báo thức vào file JSON"""
        try:
            # Chuyển đổi dữ liệu để có thể serialize thành JSON
            data_to_save = {}
            for alarm_id, alarm_data in self.alarms.items():
                alarm_copy = alarm_data.copy()
                
                # Chuyển đổi datetime thành string
                if 'alarm_time' in alarm_copy and isinstance(alarm_copy['alarm_time'], datetime):
                    alarm_copy['alarm_time'] = alarm_copy['alarm_time'].isoformat()
                
                # Chuyển đổi time từ tuple về list (JSON không hỗ trợ tuple)
                if 'time' in alarm_copy and isinstance(alarm_copy['time'], tuple):
                    alarm_copy['time'] = list(alarm_copy['time'])
                
                data_to_save[alarm_id] = alarm_copy
            
            # Lưu vào file
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data_to_save, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f"Lỗi khi lưu dữ liệu: {e}")
            messagebox.showerror("Lỗi", f"Không thể lưu dữ liệu: {e}")
    
    def on_closing(self):
        """Xử lý khi đóng ứng dụng"""
        self.save_alarms()
        self.root.destroy()
    
    def add_alarm(self, alarm_data):
        """Thêm báo thức mới vào danh sách"""
        alarm_id = str(uuid.uuid4())
        self.alarms[alarm_id] = alarm_data
        self.refresh_alarm_list()
        self.save_alarms()  # Lưu sau khi thêm
        return alarm_id
    
    def update_alarm(self, alarm_id, alarm_data):
        """Cập nhật báo thức"""
        if alarm_id in self.alarms:
            self.alarms[alarm_id] = alarm_data
            self.refresh_alarm_list()
            self.save_alarms()  # Lưu sau khi cập nhật
    
    def delete_alarm(self, alarm_id):
        """Xóa báo thức"""
        if alarm_id in self.alarms:
            # Nếu đang kêu, dừng lại
            if self.active_alarm_id == alarm_id:
                self.stop_alarm()
            del self.alarms[alarm_id]
            self.refresh_alarm_list()
            self.save_alarms()  # Lưu sau khi xóa
    
    def toggle_alarm_enabled(self, alarm_id):
        """Bật/tắt báo thức"""
        if alarm_id in self.alarms:
            self.alarms[alarm_id]['enabled'] = not self.alarms[alarm_id].get('enabled', True)
            self.refresh_alarm_list()
            self.save_alarms()  # Lưu sau khi toggle
    
    def edit_alarm(self, alarm_id):
        """Mở view chỉnh sửa báo thức"""
        if alarm_id in self.alarms:
            self.show_detail_view(alarm_id, self.alarms[alarm_id])
    
    def refresh_alarm_list(self):
        """Làm mới danh sách báo thức"""
        # Xóa tất cả widget cũ
        for widget in self.alarms_container.winfo_children():
            widget.destroy()
        
        if not self.alarms:
            # Hiển thị thông báo không có báo thức
            no_alarm_label = ttk.Label(
                self.alarms_container, 
                text="Chưa có báo thức nào.\nNhấn 'Thêm Báo Thức Mới' để tạo báo thức đầu tiên.",
                font=("Arial", 12),
                foreground="gray",
                justify=tk.CENTER
            )
            no_alarm_label.pack(pady=50)
            return
        
        # Hiển thị từng báo thức
        for alarm_id, alarm_data in self.alarms.items():
            self.create_alarm_item(alarm_id, alarm_data)
    
    def create_alarm_item(self, alarm_id, alarm_data):
        """Tạo một item báo thức trong danh sách"""
        # Frame chứa item
        item_frame = ttk.Frame(self.alarms_container, relief=tk.RAISED, borderwidth=1)
        item_frame.pack(fill=tk.X, pady=5, padx=5)
        
        # Frame nội dung
        content_frame = ttk.Frame(item_frame, padding="10")
        content_frame.pack(fill=tk.X)
        
        # Thông tin báo thức
        info_frame = ttk.Frame(content_frame)
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Tên báo thức hoặc thời gian
        name = alarm_data.get('name')
        hour, minute = alarm_data.get('time', (0, 0))
        time_str = f"{hour:02d}:{minute:02d}"
        
        if name:
            name_label = ttk.Label(info_frame, text=name, font=("Arial", 12, "bold"))
            name_label.pack(anchor=tk.W)
            time_label = ttk.Label(info_frame, text=f"⏰ {time_str}", font=("Arial", 10))
            time_label.pack(anchor=tk.W)
        else:
            time_label = ttk.Label(info_frame, text=f"⏰ {time_str}", font=("Arial", 14, "bold"))
            time_label.pack(anchor=tk.W)
        
        # Trạng thái
        enabled = alarm_data.get('enabled', True)
        status_text = "🟢 BẬT" if enabled else "🔴 TẮT"
        status_color = "green" if enabled else "red"
        status_label = ttk.Label(info_frame, text=status_text, 
                                font=("Arial", 10), foreground=status_color)
        status_label.pack(anchor=tk.W, pady=(5, 0))
        
        # Thời gian báo thức sẽ kêu
        if 'alarm_time' in alarm_data:
            alarm_time = alarm_data['alarm_time']
            if isinstance(alarm_time, datetime):
                next_time_str = alarm_time.strftime('%H:%M - %d/%m/%Y')
                next_label = ttk.Label(info_frame, text=f"Kêu lúc: {next_time_str}", 
                                      font=("Arial", 9), foreground="blue")
                next_label.pack(anchor=tk.W)
        
        # Frame nút điều khiển
        button_frame = ttk.Frame(content_frame)
        button_frame.pack(side=tk.RIGHT, padx=5)
        
        # Nút bật/tắt
        toggle_text = "Tắt" if enabled else "Bật"
        toggle_button = ttk.Button(button_frame, text=toggle_text, width=8,
                                   command=lambda: self.toggle_alarm_enabled(alarm_id))
        toggle_button.pack(pady=2)
        
        # Nút chỉnh sửa
        edit_button = ttk.Button(button_frame, text="✏️ Sửa", width=8,
                                command=lambda: self.edit_alarm(alarm_id))
        edit_button.pack(pady=2)
        
        # Nút xóa
        delete_button = ttk.Button(button_frame, text="🗑️ Xóa", width=8,
                                  command=lambda: self.confirm_delete_alarm(alarm_id))
        delete_button.pack(pady=2)
    
    def confirm_delete_alarm(self, alarm_id):
        """Xác nhận xóa báo thức"""
        if alarm_id in self.alarms:
            name = self.alarms[alarm_id].get('name', 'Báo thức này')
            if messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa '{name}'?"):
                self.delete_alarm(alarm_id)
    
    def start_alarm_checker(self):
        """Bắt đầu thread kiểm tra báo thức"""
        if self.alarm_thread is None or not self.alarm_thread.is_alive():
            self.alarm_thread = threading.Thread(target=self.check_alarms, daemon=True)
            self.alarm_thread.start()
    
    def check_alarms(self):
        """Kiểm tra tất cả báo thức đang bật"""
        while True:
            if not self.is_alarm_playing:
                now = datetime.now()
                for alarm_id, alarm_data in self.alarms.items():
                    if not alarm_data.get('enabled', True):
                        continue
                    
                    alarm_time = alarm_data.get('alarm_time')
                    if alarm_time and isinstance(alarm_time, datetime):
                        if now >= alarm_time:
                            self.start_alarm(alarm_id, alarm_data)
                            break
            
            time.sleep(1)
    
    def start_alarm(self, alarm_id, alarm_data):
        """Bắt đầu báo thức"""
        if self.is_alarm_playing:
            return
        
        self.active_alarm_id = alarm_id
        self.is_alarm_playing = True
        
        # Phát nhạc trong thread riêng
        sound_thread = threading.Thread(
            target=self.play_alarm_sound, 
            args=(alarm_data.get('file'),), 
            daemon=True
        )
        sound_thread.start()
        
        # Hiển thị cửa sổ giải toán
        math_count = alarm_data.get('math_count', 1)  # Mặc định 1 nếu không có
        self.show_math_challenge(math_count)
        
        # Cập nhật UI
        self.refresh_alarm_list()
    
    def play_alarm_sound(self, file_path):
        """Phát nhạc báo thức"""
        try:
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play(-1)  # -1 để loop vô hạn
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể phát nhạc: {e}")
            self.is_alarm_playing = False
    
    def show_math_challenge(self, total_count=1, current_count=0, correct_count=0):
        """Hiển thị cửa sổ giải toán
        
        Args:
            total_count: Tổng số bài toán cần giải đúng
            current_count: Số bài toán hiện tại (đã giải)
            correct_count: Số bài toán đã giải đúng
        """
        # Tạo cửa sổ mới để giải toán
        challenge_window = tk.Toplevel(self.root)
        challenge_window.title("Tắt Báo Thức - Phải giải đúng mới tắt được!")
        challenge_window.geometry("400x400")
        challenge_window.resizable(False, False)
        
        # Đặt cửa sổ lên trên cùng
        challenge_window.attributes('-topmost', True)
        challenge_window.grab_set()  # Modal window
        
        # Xử lý khi đóng cửa sổ - tự động hiện lại cửa sổ mới
        def on_closing():
            challenge_window.destroy()
            # Tự động hiện lại cửa sổ giải toán mới
            self.root.after(100, lambda: self.show_math_challenge(total_count, current_count, correct_count))
        
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
        warning_text = f"⚠️ Bạn phải giải đúng {total_count} bài toán để tắt báo thức!"
        warning_label = ttk.Label(
            main_frame, 
            text=warning_text,
            font=("Arial", 10, "bold"),
            foreground="red"
        )
        warning_label.pack(pady=5)
        
        # Hiển thị tiến độ
        if total_count > 1:
            progress_text = f"📊 Tiến độ: {correct_count}/{total_count} bài đã giải đúng"
            progress_label = ttk.Label(
                main_frame,
                text=progress_text,
                font=("Arial", 11, "bold"),
                foreground="blue"
            )
            progress_label.pack(pady=5)
        
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
                    # Đáp án đúng
                    new_correct_count = correct_count + 1
                    new_current_count = current_count + 1
                    
                    if new_correct_count >= total_count:
                        # Đã giải đủ số bài toán yêu cầu - tắt báo thức
                        self.stop_alarm()
                        challenge_window.destroy()
                        messagebox.showinfo("Thành công", 
                                          f"Bạn đã giải đúng {total_count} bài toán!\nBáo thức đã được tắt!")
                    else:
                        # Chưa đủ, tiếp tục với bài toán tiếp theo
                        challenge_window.destroy()
                        messagebox.showinfo("Đúng rồi!", 
                                          f"Bạn đã giải đúng {new_correct_count}/{total_count} bài.\nTiếp tục với bài toán tiếp theo!")
                        self.root.after(100, lambda: self.show_math_challenge(total_count, new_current_count, new_correct_count))
                else:
                    # Đáp án sai - tạo bài toán mới
                    messagebox.showwarning("Sai rồi!", "Hãy thử lại!")
                    challenge_window.destroy()
                    # Tiếp tục với cùng số bài đã giải đúng
                    self.root.after(100, lambda: self.show_math_challenge(total_count, current_count + 1, correct_count))
            except ValueError:
                messagebox.showwarning("Lỗi", "Vui lòng nhập số!")
        
        # Nút xác nhận
        submit_button = ttk.Button(main_frame, text="Xác nhận", 
                                  command=check_answer)
        submit_button.pack(pady=10)
        
        # Cho phép Enter để submit
        answer_entry.bind('<Return>', lambda e: check_answer())
    
    def stop_alarm(self):
        """Dừng báo thức"""
        pygame.mixer.music.stop()
        self.is_alarm_playing = False
        
        # Cập nhật lại thời gian báo thức cho lần sau
        if self.active_alarm_id and self.active_alarm_id in self.alarms:
            alarm_data = self.alarms[self.active_alarm_id]
            hour, minute = alarm_data.get('time', (0, 0))
            now = datetime.now()
            alarm_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            if alarm_time <= now:
                alarm_time += timedelta(days=1)
            alarm_data['alarm_time'] = alarm_time
            self.save_alarms()  # Lưu sau khi cập nhật alarm_time
        
        self.active_alarm_id = None
        self.refresh_alarm_list()
    
    def read_current_time(self):
        """Đọc thời gian hiện tại bằng giọng nói"""
        if not self.tts_engine:
            messagebox.showwarning("Cảnh báo", 
                                  "Tính năng text-to-speech không khả dụng.\n"
                                  "Vui lòng cài đặt pyttsx3: pip install pyttsx3")
            return
        
        def speak_in_thread():
            try:
                now = datetime.now()
                hour = now.hour
                minute = now.minute
                second = now.second
                
                # Tạo văn bản tiếng Việt
                time_text = f"Bây giờ là {hour} giờ {minute} phút {second} giây"
                
                # Đọc trong thread riêng để không block UI
                self.tts_engine.say(time_text)
                self.tts_engine.runAndWait()
            except Exception as e:
                # Hiển thị lỗi trong main thread
                self.root.after(0, lambda: messagebox.showerror("Lỗi", f"Không thể đọc thời gian: {e}"))
        
        # Chạy trong thread riêng để không block UI
        speak_thread = threading.Thread(target=speak_in_thread, daemon=True)
        speak_thread.start()
    
    def update_time(self):
        """Cập nhật thời gian hiện tại"""
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_label.config(text=current_time)
        
        # Cập nhật đồng hồ realtime trong detail view nếu đang ở detail view
        if hasattr(self, 'detail_time_label') and self.current_view == 'detail':
            self.detail_time_label.config(text=current_time)
        
        self.root.after(1000, self.update_time)

def main():
    root = tk.Tk()
    app = AlarmClock(root)
    root.mainloop()

if __name__ == "__main__":
    main()
