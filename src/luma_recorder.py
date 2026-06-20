import ctypes
import ctypes.wintypes
import datetime as dt
import json
import os
import queue
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

APP = "Luma Recorder"
PUBLISHER = "albahri.org"
SOURCE_1 = "https://github.com/albahri-org"
SOURCE_2 = "https://github.com/QusaiALBahri?tab=repositories"
ACCENT = "#007AFF"
PANEL = "#F5F5F7"
INK = "#1D1D1F"
MUTED = "#6E6E73"
RED = "#FF3B30"
GREEN = "#34C759"
ORANGE = "#FF9500"

TEXT = {
    "en": {
        "record": "Record", "library": "Library", "tools": "Edit / Export", "privacy": "Privacy",
        "capture": "Capture", "full": "Full screen", "monitor": "Monitor", "area": "Select area", "window": "Window",
        "choose_area": "Choose area", "refresh": "Refresh", "audio": "Audio", "mic": "Microphone",
        "system": "System audio", "webcam": "Webcam overlay", "save": "Save / Quality", "browse": "Browse",
        "name": "Name", "format": "Format", "fps": "FPS", "quality": "Quality", "encoder": "Encoder",
        "countdown": "Countdown", "limit": "Auto-stop min", "cursor": "Cursor", "mini": "Floating bar",
        "minimize": "Minimize", "start": "Record", "stop": "Stop", "pause": "Pause", "resume": "Resume",
        "open": "Open folder", "last": "Play last", "recent": "Recent Recordings", "play": "Play",
        "rename": "Rename", "delete": "Delete", "use": "Use in editor", "video_tools": "Video Tools",
        "choose_video": "Choose video", "trim": "Trim", "convert": "Convert", "compress": "Compress",
        "zoom": "Wheel Zoom / Focus Export", "audio_out": "Extract audio", "shot": "Save screenshot",
        "lang": "Language", "encrypt": "Encrypt recordings folder with Windows EFS", "apply": "Apply encryption",
        "remove": "Remove encryption", "cleanup": "Clean temp files", "uninstall": "Clean uninstall",
        "local": "Local-only portable recorder. No upload, cloud sync, telemetry, or network feature.",
        "source": f"Publisher: {PUBLISHER}. Official source only: {SOURCE_1} and {SOURCE_2}",
    },
    "ar": {
        "record": "تسجيل", "library": "المكتبة", "tools": "تعديل / تصدير", "privacy": "الخصوصية",
        "capture": "منطقة التسجيل", "full": "الشاشة كاملة", "monitor": "شاشة محددة", "area": "تحديد منطقة", "window": "نافذة",
        "choose_area": "اختر المنطقة", "refresh": "تحديث", "audio": "الصوت", "mic": "الميكروفون",
        "system": "صوت النظام", "webcam": "إظهار الكاميرا", "save": "الحفظ / الجودة", "browse": "استعراض",
        "name": "الاسم", "format": "الصيغة", "fps": "الإطارات", "quality": "الجودة", "encoder": "الترميز",
        "countdown": "العد التنازلي", "limit": "إيقاف تلقائي بالدقائق", "cursor": "المؤشر", "mini": "شريط عائم",
        "minimize": "تصغير", "start": "تسجيل", "stop": "إيقاف", "pause": "إيقاف مؤقت", "resume": "متابعة",
        "open": "فتح المجلد", "last": "تشغيل الأخير", "recent": "التسجيلات الأخيرة", "play": "تشغيل",
        "rename": "إعادة تسمية", "delete": "حذف", "use": "استخدم في التعديل", "video_tools": "أدوات الفيديو",
        "choose_video": "اختر فيديو", "trim": "قص", "convert": "تحويل", "compress": "ضغط",
        "zoom": "تكبير بالعجلة / تركيز", "audio_out": "استخراج الصوت", "shot": "حفظ لقطة",
        "lang": "اللغة", "encrypt": "تشفير مجلد التسجيلات بواسطة Windows EFS", "apply": "تفعيل التشفير",
        "remove": "إزالة التشفير", "cleanup": "تنظيف المؤقت", "uninstall": "إزالة نظيفة",
        "local": "مسجل محمول ومحلي فقط. لا يوجد رفع، ولا مزامنة سحابية، ولا تتبع، ولا اتصال بالشبكة.",
        "source": f"الناشر: {PUBLISHER}. المصدر الرسمي فقط: {SOURCE_1} و {SOURCE_2}",
    },
}


def app_root():
    return Path(sys.executable).resolve().parent if getattr(sys, "frozen", False) else Path(__file__).resolve().parents[1]


def resource(name):
    base = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
    item = base / name
    return str(item) if item.exists() else name


def find_ffmpeg():
    bundled = resource("ffmpeg.exe")
    return bundled if Path(bundled).exists() else shutil.which("ffmpeg")


def dpi():
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass


def clean_name(value):
    return re.sub(r"[^\w\- .]", "_", value).strip() or "Recording"


def hms(seconds):
    seconds = max(0, int(seconds))
    return f"{seconds // 3600:02d}:{seconds % 3600 // 60:02d}:{seconds % 60:02d}"


class RegionPicker(tk.Toplevel):
    def __init__(self, master, label):
        super().__init__(master)
        self.result = None
        self.start = (0, 0)
        self.rect = None
        w, h = ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1)
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.attributes("-alpha", 0.35)
        self.geometry(f"{w}x{h}+0+0")
        self.configure(bg="#111")
        self.canvas = tk.Canvas(self, bg="#111", highlightthickness=0, cursor="crosshair")
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_text(w // 2, 52, text=label, fill="white", font=("Segoe UI", 20, "bold"))
        self.canvas.bind("<ButtonPress-1>", self.press)
        self.canvas.bind("<B1-Motion>", self.drag)
        self.canvas.bind("<ButtonRelease-1>", self.release)
        self.bind("<Escape>", lambda _e: self.destroy())
        self.grab_set()
        self.focus_force()

    def press(self, e):
        self.start = (e.x, e.y)
        self.rect = self.canvas.create_rectangle(e.x, e.y, e.x, e.y, outline=ACCENT, width=4, fill="#B7D7FF")

    def drag(self, e):
        if self.rect:
            self.canvas.coords(self.rect, self.start[0], self.start[1], e.x, e.y)

    def release(self, e):
        x1, y1 = self.start
        x2, y2 = e.x, e.y
        x, y, w, h = min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1)
        if w >= 64 and h >= 64:
            self.result = (x, y, w, h)
        self.destroy()


class MiniBar(tk.Toplevel):
    def __init__(self, app):
        super().__init__(app)
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.geometry("+40+40")
        box = tk.Frame(self, bg="#FAFAFA", bd=1, relief="solid")
        box.pack()
        self.label = tk.Label(box, text="00:00:00", bg="#FAFAFA", fg=INK, width=10, font=("Segoe UI", 14, "bold"))
        self.label.pack(side="left", padx=10, pady=8)
        tk.Button(box, text="Pause", command=app.toggle_pause, bg="#E9E9EB", bd=0, padx=12, pady=5).pack(side="left", padx=4)
        tk.Button(box, text="Stop", command=app.stop_recording, bg=RED, fg="white", bd=0, padx=12, pady=5).pack(side="left", padx=(4, 10))
        self.drag_start = (0, 0)
        box.bind("<ButtonPress-1>", lambda e: setattr(self, "drag_start", (e.x, e.y)))
        box.bind("<B1-Motion>", self.move)

    def move(self, e):
        self.geometry(f"+{self.winfo_x() + e.x - self.drag_start[0]}+{self.winfo_y() + e.y - self.drag_start[1]}")


class Hotkeys(threading.Thread):
    def __init__(self, app):
        super().__init__(daemon=True)
        self.app = app
        self.thread_id = None
        self.running = True

    def run(self):
        user32 = ctypes.windll.user32
        self.thread_id = ctypes.windll.kernel32.GetCurrentThreadId()
        mods = 0x0002 | 0x0004
        for i, key in enumerate((ord("R"), ord("S"), ord("P")), 1):
            user32.RegisterHotKey(None, i, mods, key)
        msg = ctypes.wintypes.MSG()
        while self.running and user32.GetMessageW(ctypes.byref(msg), None, 0, 0) != 0:
            if msg.message == 0x0312:
                [self.app.start_recording, self.app.stop_recording, self.app.toggle_pause][msg.wParam - 1]()
        for i in (1, 2, 3):
            user32.UnregisterHotKey(None, i)

    def stop(self):
        self.running = False
        if self.thread_id:
            ctypes.windll.user32.PostThreadMessageW(self.thread_id, 0x0012, 0, 0)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        dpi()
        self.base = app_root()
        self.out = self.base / "recordings"
        self.out.mkdir(exist_ok=True)
        self.settings = self.base / "settings.json"
        self.ffmpeg = find_ffmpeg()
        self.proc = None
        self.current = None
        self.started = None
        self.paused_at = None
        self.paused_total = 0
        self.paused = False
        self.region = None
        self.logq = queue.Queue()
        self.mini = None
        self.hotkeys = None
        self.vars()
        self.load()
        self.setup()
        self.ui()
        self.refresh_devices()
        self.after(300, self.tick)
        try:
            self.hotkeys = Hotkeys(self)
            self.hotkeys.start()
        except Exception:
            pass

    def vars(self):
        self.lang = tk.StringVar(value="en")
        self.mode = tk.StringVar(value="Full screen")
        self.region_text = tk.StringVar(value="No area selected")
        self.output = tk.StringVar(value=str(self.out))
        self.prefix = tk.StringVar(value="Screen Recording")
        self.format = tk.StringVar(value="mp4")
        self.fps = tk.IntVar(value=30)
        self.quality = tk.StringVar(value="Balanced")
        self.encoder = tk.StringVar(value="H.264 CPU")
        self.countdown = tk.IntVar(value=3)
        self.limit = tk.StringVar()
        self.cursor = tk.BooleanVar(value=True)
        self.mini_on = tk.BooleanVar(value=True)
        self.minimize = tk.BooleanVar(value=False)
        self.mic_on = tk.BooleanVar(value=False)
        self.system_on = tk.BooleanVar(value=False)
        self.mic = tk.StringVar()
        self.system_audio = tk.StringVar()
        self.webcam_on = tk.BooleanVar(value=False)
        self.webcam = tk.StringVar()
        self.status = tk.StringVar(value="Ready")
        self.timer = tk.StringVar(value="00:00:00")
        self.log = tk.StringVar()
        self.tool_file = tk.StringVar()
        self.encrypt = tk.BooleanVar(value=False)

    def t(self, key):
        return TEXT.get(self.lang.get(), TEXT["en"]).get(key, key)

    def setup(self):
        self.title(APP)
        self.geometry("1120x760")
        self.minsize(1000, 680)
        self.configure(bg="#FFFFFF")
        self.protocol("WM_DELETE_WINDOW", self.close)
        style = ttk.Style()
        style.theme_use("clam")
        for name, bg in [("TFrame", "#FFFFFF"), ("Panel.TFrame", PANEL)]:
            style.configure(name, background=bg)
        style.configure("TLabel", background="#FFFFFF", foreground=INK, font=("Segoe UI", 10))
        style.configure("Panel.TLabel", background=PANEL, foreground=INK, font=("Segoe UI", 10))
        style.configure("Title.TLabel", background="#FFFFFF", foreground=INK, font=("Segoe UI", 24, "bold"))
        style.configure("Big.TLabel", background="#FFFFFF", foreground=INK, font=("Segoe UI", 38, "bold"))
        style.configure("Primary.TButton", background=ACCENT, foreground="white", padding=(16, 10), font=("Segoe UI", 10, "bold"))
        style.configure("Danger.TButton", background=RED, foreground="white", padding=(16, 10), font=("Segoe UI", 10, "bold"))
        style.configure("Soft.TButton", background="#E9E9EB", foreground=INK, padding=(12, 8))
        style.configure("TCheckbutton", background=PANEL, foreground=INK)
        style.configure("TRadiobutton", background=PANEL, foreground=INK)

    def rebuild_ui(self):
        self.save()
        for child in self.winfo_children():
            child.destroy()
        self.ui()

    def panel(self, parent):
        return ttk.Frame(parent, padding=16, style="Panel.TFrame")

    def title_line(self, parent, text):
        ttk.Label(parent, text=text, style="Panel.TLabel", font=("Segoe UI", 13, "bold")).pack(anchor="w", pady=(0, 10))

    def ui(self):
        root = ttk.Frame(self, padding=22)
        root.pack(fill="both", expand=True)
        head = ttk.Frame(root)
        head.pack(fill="x")
        ttk.Label(head, text=APP, style="Title.TLabel").pack(side="left")
        ttk.Label(head, textvariable=self.timer, style="Big.TLabel").pack(side="right")
        tabs = ttk.Notebook(root)
        tabs.pack(fill="both", expand=True, pady=(18, 0))
        rec, lib, tools, priv = ttk.Frame(tabs), ttk.Frame(tabs), ttk.Frame(tabs), ttk.Frame(tabs)
        tabs.add(rec, text=self.t("record"))
        tabs.add(lib, text=self.t("library"))
        tabs.add(tools, text=self.t("tools"))
        tabs.add(priv, text=self.t("privacy"))
        self.record_ui(rec)
        self.library_ui(lib)
        self.tools_ui(tools)
        self.privacy_ui(priv)
        self.bottom(root)

    def record_ui(self, tab):
        tab.columnconfigure(0, weight=1)
        tab.columnconfigure(1, weight=1)
        left, right = self.panel(tab), self.panel(tab)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=8)
        right.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=8)
        self.title_line(left, self.t("capture"))
        modes = ttk.Frame(left, style="Panel.TFrame")
        modes.pack(fill="x", pady=(0, 10))
        for val, key in [("Full screen", "full"), ("Select area", "area")]:
            ttk.Radiobutton(modes, text=self.t(key), value=val, variable=self.mode).pack(side="left", padx=(0, 14))
        row = ttk.Frame(left, style="Panel.TFrame")
        row.pack(fill="x", pady=6)
        ttk.Button(row, text=self.t("choose_area"), style="Soft.TButton", command=self.pick_region).pack(side="left")
        ttk.Label(row, textvariable=self.region_text, style="Panel.TLabel").pack(side="left", padx=10)
        opts = ttk.Frame(left, style="Panel.TFrame")
        opts.pack(fill="x", pady=(8, 14))
        for text, var in [(self.t("cursor"), self.cursor), (self.t("mini"), self.mini_on), (self.t("minimize"), self.minimize)]:
            ttk.Checkbutton(opts, text=text, variable=var).pack(side="left", padx=(0, 16))
        self.title_line(left, self.t("audio"))
        self.mic_combo = self.device_row(left, self.t("mic"), self.mic_on, self.mic)
        self.system_combo = self.device_row(left, self.t("system"), self.system_on, self.system_audio)
        ttk.Button(left, text=self.t("refresh"), style="Soft.TButton", command=self.refresh_devices).pack(anchor="w", pady=8)
        self.title_line(right, self.t("webcam"))
        self.webcam_combo = self.device_row(right, self.t("webcam"), self.webcam_on, self.webcam)
        self.title_line(right, self.t("save"))
        save = ttk.Frame(right, style="Panel.TFrame")
        save.pack(fill="x", pady=6)
        ttk.Entry(save, textvariable=self.output).pack(side="left", fill="x", expand=True)
        ttk.Button(save, text=self.t("browse"), style="Soft.TButton", command=self.browse_output).pack(side="left", padx=(10, 0))
        grid = ttk.Frame(right, style="Panel.TFrame")
        grid.pack(fill="x")
        self.field(grid, self.t("name"), self.prefix, 0, 0)
        self.combo(grid, self.t("format"), self.format, ["mp4", "mkv"], 0, 2)
        self.combo(grid, self.t("fps"), self.fps, [15, 24, 30, 60], 1, 0)
        self.combo(grid, self.t("quality"), self.quality, ["Light", "Balanced", "High"], 1, 2)
        self.combo(grid, self.t("encoder"), self.encoder, ["H.264 CPU", "H.264 NVIDIA", "H.264 AMD", "H.264 Intel"], 2, 0, 3)
        self.field(grid, self.t("countdown"), self.countdown, 3, 0)
        self.field(grid, self.t("limit"), self.limit, 3, 2)

    def device_row(self, parent, label, toggle, var):
        row = ttk.Frame(parent, style="Panel.TFrame")
        row.pack(fill="x", pady=6)
        ttk.Checkbutton(row, text=label, variable=toggle).pack(side="left")
        combo = ttk.Combobox(row, textvariable=var, state="readonly", width=40)
        combo.pack(side="left", fill="x", expand=True, padx=10)
        return combo

    def field(self, p, label, var, r, c):
        ttk.Label(p, text=label, style="Panel.TLabel").grid(row=r, column=c, sticky="w", padx=8, pady=7)
        ttk.Entry(p, textvariable=var).grid(row=r, column=c + 1, sticky="ew", padx=8, pady=7)

    def combo(self, p, label, var, values, r, c, span=1):
        ttk.Label(p, text=label, style="Panel.TLabel").grid(row=r, column=c, sticky="w", padx=8, pady=7)
        ttk.Combobox(p, textvariable=var, values=values, state="readonly").grid(row=r, column=c + 1, columnspan=span, sticky="ew", padx=8, pady=7)

    def library_ui(self, tab):
        frame = self.panel(tab)
        frame.pack(fill="both", expand=True, pady=8)
        self.title_line(frame, self.t("recent"))
        self.listbox = tk.Listbox(frame, height=18, bd=0, highlightthickness=1, font=("Segoe UI", 10))
        self.listbox.pack(fill="both", expand=True)
        actions = ttk.Frame(frame, style="Panel.TFrame")
        actions.pack(fill="x", pady=(12, 0))
        for text, cmd in [(self.t("refresh"), self.refresh_library), (self.t("play"), self.play_selected), (self.t("delete"), self.delete_selected), (self.t("use"), self.use_selected)]:
            ttk.Button(actions, text=text, style="Soft.TButton", command=cmd).pack(side="left", padx=(0, 8))
        self.refresh_library()

    def tools_ui(self, tab):
        frame = self.panel(tab)
        frame.pack(fill="both", expand=True, pady=8)
        self.title_line(frame, self.t("video_tools"))
        row = ttk.Frame(frame, style="Panel.TFrame")
        row.pack(fill="x", pady=(0, 12))
        ttk.Entry(row, textvariable=self.tool_file).pack(side="left", fill="x", expand=True)
        ttk.Button(row, text=self.t("choose_video"), style="Soft.TButton", command=self.choose_video).pack(side="left", padx=(10, 0))
        tools = ttk.Frame(frame, style="Panel.TFrame")
        tools.pack(fill="x", pady=6)
        for text, cmd in [(self.t("trim"), self.trim), (self.t("convert"), self.convert), (self.t("compress"), self.compress), (self.t("audio_out"), self.extract_audio), (self.t("shot"), self.snapshot), (self.t("zoom"), self.zoom_export)]:
            ttk.Button(tools, text=text, style="Soft.TButton", command=cmd).pack(side="left", padx=(0, 8))
        ttk.Label(frame, textvariable=self.log, style="Panel.TLabel", wraplength=980).pack(fill="x", pady=(12, 0))

    def privacy_ui(self, tab):
        frame = self.panel(tab)
        frame.pack(fill="both", expand=True, pady=8)
        self.title_line(frame, self.t("privacy"))
        ttk.Label(frame, text=self.t("local"), style="Panel.TLabel", wraplength=940).pack(anchor="w", pady=8)
        ttk.Label(frame, text=self.t("source"), style="Panel.TLabel", wraplength=940).pack(anchor="w", pady=8)
        row = ttk.Frame(frame, style="Panel.TFrame")
        row.pack(fill="x", pady=8)
        ttk.Label(row, text=self.t("lang"), style="Panel.TLabel").pack(side="left")
        ttk.Combobox(row, textvariable=self.lang, values=["en", "ar"], state="readonly", width=8).pack(side="left", padx=10)
        ttk.Button(row, text=self.t("refresh"), style="Soft.TButton", command=self.rebuild_ui).pack(side="left")
        ttk.Checkbutton(frame, text=self.t("encrypt"), variable=self.encrypt).pack(anchor="w", pady=8)
        actions = ttk.Frame(frame, style="Panel.TFrame")
        actions.pack(fill="x", pady=8)
        ttk.Button(actions, text=self.t("apply"), style="Primary.TButton", command=lambda: self.efs(True)).pack(side="left", padx=(0, 8))
        ttk.Button(actions, text=self.t("remove"), style="Soft.TButton", command=lambda: self.efs(False)).pack(side="left", padx=(0, 8))
        ttk.Button(actions, text=self.t("cleanup"), style="Soft.TButton", command=self.cleanup).pack(side="left", padx=(0, 8))
        ttk.Button(actions, text=self.t("uninstall"), style="Danger.TButton", command=self.uninstall).pack(side="left")

    def bottom(self, root):
        bar = ttk.Frame(root, padding=(0, 14, 0, 0))
        bar.pack(fill="x")
        self.dot = tk.Canvas(bar, width=14, height=14, bg="#FFFFFF", highlightthickness=0)
        self.dot.create_oval(2, 2, 12, 12, fill=GREEN, outline=GREEN, tags=("dot",))
        self.dot.pack(side="left")
        ttk.Label(bar, textvariable=self.status).pack(side="left", padx=8)
        ttk.Button(bar, text=self.t("open"), style="Soft.TButton", command=self.open_folder).pack(side="right", padx=(8, 0))
        ttk.Button(bar, text=self.t("last"), style="Soft.TButton", command=self.play_last).pack(side="right", padx=(8, 0))
        self.stop_btn = ttk.Button(bar, text=self.t("stop"), style="Danger.TButton", command=self.stop_recording, state="disabled")
        self.stop_btn.pack(side="right", padx=(8, 0))
        self.pause_btn = ttk.Button(bar, text=self.t("pause"), style="Soft.TButton", command=self.toggle_pause, state="disabled")
        self.pause_btn.pack(side="right", padx=(8, 0))
        self.start_btn = ttk.Button(bar, text=self.t("start"), style="Primary.TButton", command=self.start_recording)
        self.start_btn.pack(side="right", padx=(8, 0))

    def refresh_devices(self):
        if not self.ffmpeg:
            self.log.set("FFmpeg not found.")
            return
        def worker():
            try:
                p = subprocess.run([self.ffmpeg, "-hide_banner", "-list_devices", "true", "-f", "dshow", "-i", "dummy"], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=10, creationflags=subprocess.CREATE_NO_WINDOW)
                audio, video, sec = [], [], ""
                for line in (p.stderr or p.stdout).splitlines():
                    low = line.lower()
                    if "video devices" in low: sec = "v"
                    elif "audio devices" in low: sec = "a"
                    else:
                        m = re.search(r'"([^"]+)"', line)
                        if m and not m.group(1).startswith("@device_"):
                            (video if sec == "v" else audio if sec == "a" else []).append(m.group(1))
                self.after(0, lambda: self.apply_devices(audio, video))
            except Exception as e:
                self.after(0, lambda: self.log.set(str(e)))
        threading.Thread(target=worker, daemon=True).start()

    def apply_devices(self, audio, video):
        self.mic_combo.configure(values=audio)
        self.system_combo.configure(values=audio)
        self.webcam_combo.configure(values=video)
        if audio and not self.mic.get(): self.mic.set(audio[0])
        if audio and not self.system_audio.get(): self.system_audio.set(next((d for d in audio if "stereo" in d.lower() or "loopback" in d.lower()), audio[0]))
        if video and not self.webcam.get(): self.webcam.set(video[0])
        self.log.set(f"Devices: {len(audio)} audio, {len(video)} camera. Hotkeys: Ctrl+Shift+R/S/P.")

    def pick_region(self):
        p = RegionPicker(self, self.t("choose_area"))
        self.wait_window(p)
        if p.result:
            self.region = p.result
            x, y, w, h = p.result
            self.region_text.set(f"{w} x {h} at {x},{y}")

    def browse_output(self):
        folder = filedialog.askdirectory(initialdir=self.output.get())
        if folder: self.output.set(folder)

    def path_out(self):
        folder = Path(self.output.get())
        folder.mkdir(parents=True, exist_ok=True)
        if self.encrypt.get(): self.efs(True, quiet=True)
        return folder / f"{clean_name(self.prefix.get())}_{dt.datetime.now():%Y-%m-%d_%H-%M-%S}.{self.format.get()}"

    def build_cmd(self, target):
        cmd = [self.ffmpeg, "-hide_banner", "-y", "-f", "gdigrab", "-framerate", str(self.fps.get()), "-draw_mouse", "1" if self.cursor.get() else "0"]
        if self.mode.get() == "Select area":
            if not self.region: raise RuntimeError("Choose an area first.")
            x, y, w, h = self.region
            cmd += ["-offset_x", str(x), "-offset_y", str(y), "-video_size", f"{w}x{h}", "-i", "desktop"]
        else:
            cmd += ["-i", "desktop"]
        audio_count = 0
        for on, dev in [(self.mic_on.get(), self.mic.get()), (self.system_on.get(), self.system_audio.get())]:
            if on and dev:
                cmd += ["-f", "dshow", "-i", f"audio={dev}"]
                audio_count += 1
        webcam_index = 1 + audio_count if self.webcam_on.get() and self.webcam.get() else None
        if webcam_index:
            cmd += ["-f", "dshow", "-framerate", str(self.fps.get()), "-i", f"video={self.webcam.get()}"]
            cmd += ["-filter_complex", f"[{webcam_index}:v]scale=260:-1[cam];[0:v][cam]overlay=W-w-24:H-h-24[v]", "-map", "[v]"]
        else:
            cmd += ["-map", "0:v"]
        if audio_count == 1:
            cmd += ["-map", "1:a", "-c:a", "aac", "-b:a", "160k"]
        elif audio_count == 2:
            mix = "[1:a][2:a]amix=inputs=2:duration=longest[aout]"
            if "-filter_complex" in cmd:
                idx = cmd.index("-filter_complex") + 1
                cmd[idx] += ";" + mix
            else:
                cmd += ["-filter_complex", mix]
            cmd += ["-map", "[aout]", "-c:a", "aac", "-b:a", "192k"]
        codec = {"H.264 CPU": "libx264", "H.264 NVIDIA": "h264_nvenc", "H.264 AMD": "h264_amf", "H.264 Intel": "h264_qsv"}.get(self.encoder.get(), "libx264")
        cmd += ["-c:v", codec]
        if codec == "libx264":
            crf = {"Light": "30", "Balanced": "24", "High": "20"}.get(self.quality.get(), "24")
            cmd += ["-preset", "veryfast", "-crf", crf, "-pix_fmt", "yuv420p"]
        else:
            cmd += ["-b:v", "8M"]
        if self.format.get() == "mp4": cmd += ["-movflags", "+faststart"]
        cmd.append(str(target))
        return cmd

    def start_recording(self):
        if self.proc or not self.ffmpeg: return
        try:
            target = self.path_out()
            cmd = self.build_cmd(target)
            limit = float(self.limit.get()) if self.limit.get().strip() else None
        except Exception as e:
            messagebox.showerror(APP, str(e)); return
        delay = max(0, int(self.countdown.get() or 0))
        self.after(delay * 1000, lambda: self.launch(cmd, target, limit))

    def launch(self, cmd, target, limit):
        try:
            self.proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="replace", creationflags=subprocess.CREATE_NO_WINDOW)
        except Exception as e:
            messagebox.showerror(APP, str(e)); return
        self.current = target
        self.started = time.monotonic()
        self.status.set(f"Recording {target.name}")
        self.dot.itemconfigure("dot", fill=RED, outline=RED)
        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        self.pause_btn.configure(state="normal")
        if self.minimize.get(): self.iconify()
        if self.mini_on.get(): self.mini = MiniBar(self)
        threading.Thread(target=self.read_logs, daemon=True).start()
        if limit and limit > 0: self.after(int(limit * 60000), self.stop_recording)

    def read_logs(self):
        for line in self.proc.stderr:
            if line.strip(): self.logq.put(line.strip())

    def toggle_pause(self):
        if not self.proc: return
        fn = "NtResumeProcess" if self.paused else "NtSuspendProcess"
        handle = ctypes.windll.kernel32.OpenProcess(0x0800, False, self.proc.pid)
        if handle:
            getattr(ctypes.windll.ntdll, fn)(handle)
            ctypes.windll.kernel32.CloseHandle(handle)
            if self.paused:
                self.paused_total += time.monotonic() - self.paused_at
                self.paused = False
                self.pause_btn.configure(text=self.t("pause"))
            else:
                self.paused_at = time.monotonic()
                self.paused = True
                self.pause_btn.configure(text=self.t("resume"))
            self.dot.itemconfigure("dot", fill=ORANGE if self.paused else RED, outline=ORANGE if self.paused else RED)

    def stop_recording(self):
        if not self.proc: return
        if self.paused: self.toggle_pause()
        try:
            self.proc.stdin.write("q\n"); self.proc.stdin.flush()
        except Exception:
            pass
        threading.Thread(target=self.wait_stop, args=(self.proc,), daemon=True).start()

    def wait_stop(self, proc):
        try: proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            proc.terminate()
            try: proc.wait(timeout=4)
            except subprocess.TimeoutExpired: proc.kill()
        self.after(0, self.done)

    def done(self):
        self.proc = None
        self.started = None
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        self.pause_btn.configure(state="disabled", text=self.t("pause"))
        self.dot.itemconfigure("dot", fill=GREEN, outline=GREEN)
        if self.mini: self.mini.destroy(); self.mini = None
        if self.current and self.current.exists():
            self.status.set(f"Saved {self.current.name}")
            self.tool_file.set(str(self.current))
        self.refresh_library()

    def tick(self):
        while True:
            try: line = self.logq.get_nowait()
            except queue.Empty: break
            if "frame=" in line or "error" in line.lower(): self.log.set(line[-260:])
        if self.proc and self.started:
            now = self.paused_at if self.paused else time.monotonic()
            self.timer.set(hms(now - self.started - self.paused_total))
            if self.mini: self.mini.label.configure(text=self.timer.get())
            if self.proc.poll() is not None: self.done()
        else:
            self.timer.set("00:00:00")
        self.after(300, self.tick)

    def refresh_library(self):
        if not hasattr(self, "listbox"): return
        self.listbox.delete(0, "end")
        for file in sorted(Path(self.output.get()).glob("*.*"), key=lambda p: p.stat().st_mtime, reverse=True):
            if file.suffix.lower() in [".mp4", ".mkv", ".webm", ".gif", ".mp3", ".png"]:
                self.listbox.insert("end", f"{file.name}   {file.stat().st_size / (1024*1024):.1f} MB")

    def selected(self):
        sel = self.listbox.curselection()
        if not sel: return None
        path = Path(self.output.get()) / self.listbox.get(sel[0]).split("   ")[0]
        return path if path.exists() else None

    def play_selected(self):
        p = self.selected()
        if p: os.startfile(str(p))

    def play_last(self):
        if self.current and self.current.exists(): os.startfile(str(self.current))
        else: self.play_selected()

    def delete_selected(self):
        p = self.selected()
        if p and messagebox.askyesno(APP, f"Delete {p.name}?"):
            p.unlink(missing_ok=True); self.refresh_library()

    def use_selected(self):
        p = self.selected()
        if p: self.tool_file.set(str(p))

    def choose_video(self):
        f = filedialog.askopenfilename(initialdir=self.output.get())
        if f: self.tool_file.set(f)

    def tool(self):
        p = Path(self.tool_file.get())
        if not p.exists(): raise RuntimeError("Choose a video first.")
        return p

    def run_tool(self, cmd, msg):
        def worker():
            try:
                p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=3600, creationflags=subprocess.CREATE_NO_WINDOW)
                self.after(0, lambda: self.log.set(msg if p.returncode == 0 else (p.stderr or p.stdout)[-700:]))
                self.after(0, self.refresh_library)
            except Exception as e:
                self.after(0, lambda: messagebox.showerror(APP, str(e)))
        threading.Thread(target=worker, daemon=True).start()

    def trim(self):
        try:
            src = self.tool(); out = src.with_name(src.stem + "_trim" + src.suffix)
            self.run_tool([self.ffmpeg, "-y", "-ss", "0", "-i", str(src), "-t", "60", "-c", "copy", str(out)], f"Saved {out.name}")
        except Exception as e: messagebox.showerror(APP, str(e))

    def convert(self):
        try:
            src = self.tool(); out = src.with_name(src.stem + "_converted.mp4")
            self.run_tool([self.ffmpeg, "-y", "-i", str(src), "-c:v", "libx264", "-preset", "veryfast", "-crf", "23", "-c:a", "aac", str(out)], f"Saved {out.name}")
        except Exception as e: messagebox.showerror(APP, str(e))

    def compress(self):
        try:
            src = self.tool(); out = src.with_name(src.stem + "_compressed.mp4")
            self.run_tool([self.ffmpeg, "-y", "-i", str(src), "-c:v", "libx264", "-preset", "veryfast", "-crf", "29", "-c:a", "aac", "-b:a", "96k", str(out)], f"Saved {out.name}")
        except Exception as e: messagebox.showerror(APP, str(e))

    def extract_audio(self):
        try:
            src = self.tool(); out = src.with_name(src.stem + "_audio.mp3")
            self.run_tool([self.ffmpeg, "-y", "-i", str(src), "-vn", "-c:a", "libmp3lame", "-q:a", "3", str(out)], f"Saved {out.name}")
        except Exception as e: messagebox.showerror(APP, str(e))

    def snapshot(self):
        try:
            src = self.tool(); out = src.with_name(src.stem + "_snapshot.png")
            self.run_tool([self.ffmpeg, "-y", "-ss", "1", "-i", str(src), "-frames:v", "1", str(out)], f"Saved {out.name}")
        except Exception as e: messagebox.showerror(APP, str(e))

    def zoom_export(self):
        try:
            src = self.tool(); out = src.with_name(src.stem + "_zoom.mp4")
            self.run_tool([self.ffmpeg, "-y", "-i", str(src), "-vf", "crop=iw/1.5:ih/1.5:iw/6:ih/6,scale=iw*1.5:ih*1.5", "-c:v", "libx264", "-preset", "veryfast", "-crf", "22", "-c:a", "copy", str(out)], f"Saved {out.name}")
        except Exception as e: messagebox.showerror(APP, str(e))

    def open_folder(self):
        Path(self.output.get()).mkdir(parents=True, exist_ok=True); os.startfile(self.output.get())

    def efs(self, enable, quiet=False):
        folder = Path(self.output.get()); folder.mkdir(parents=True, exist_ok=True)
        try:
            p = subprocess.run(["cipher", "/e" if enable else "/d", str(folder)], capture_output=True, text=True, timeout=60, creationflags=subprocess.CREATE_NO_WINDOW)
            self.log.set("Encryption updated." if p.returncode == 0 else (p.stderr or p.stdout))
        except Exception as e:
            if not quiet: messagebox.showerror(APP, str(e))

    def cleanup(self):
        n = 0
        for f in Path(tempfile.gettempdir()).glob("luma_*"):
            try: f.unlink(); n += 1
            except Exception: pass
        self.log.set(f"Temporary files removed: {n}")

    def uninstall(self):
        if not messagebox.askyesno(APP, "Remove this portable app folder and recordings?"): return
        bat = Path(tempfile.gettempdir()) / "uninstall_luma_recorder.cmd"
        bat.write_text(f'@echo off\ntimeout /t 2 /nobreak >nul\nrmdir /s /q "{self.base}"\ndel "%~f0"\n')
        subprocess.Popen(["cmd", "/c", str(bat)], creationflags=subprocess.CREATE_NO_WINDOW)
        self.destroy()

    def load(self):
        try: data = json.loads(self.settings.read_text(encoding="utf-8"))
        except Exception: return
        for k, v in data.items():
            var = getattr(self, k, None)
            if isinstance(var, (tk.StringVar, tk.IntVar, tk.BooleanVar)):
                try: var.set(v)
                except Exception: pass

    def save(self):
        data = {k: v.get() for k, v in vars(self).items() if isinstance(v, (tk.StringVar, tk.IntVar, tk.BooleanVar))}
        try: self.settings.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception: pass

    def close(self):
        self.save()
        if self.hotkeys: self.hotkeys.stop()
        if self.proc:
            if not messagebox.askyesno(APP, "Stop recording and close?"): return
            self.stop_recording(); self.after(1000, self.destroy); return
        self.destroy()


if __name__ == "__main__":
    App().mainloop()
