import ctypes
import sys
from pathlib import Path
from tkinter import messagebox


def main():
    base = Path(sys.executable).resolve().parent if getattr(sys, "frozen", False) else Path(__file__).resolve().parent
    recorder = base / "LumaRecorder.exe"
    if not recorder.exists():
        messagebox.showerror("Luma Recorder Admin", f"Could not find:\n{recorder}")
        return 1
    result = ctypes.windll.shell32.ShellExecuteW(None, "runas", str(recorder), None, str(base), 1)
    if result <= 32:
        messagebox.showerror("Luma Recorder Admin", "Windows did not allow the admin launch.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
