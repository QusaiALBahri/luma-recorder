# Building From Source

## Requirements

- Windows 10 or later
- Python 3.14 or compatible Python 3 version
- PyInstaller
- FFmpeg available on `PATH`

Install PyInstaller:

```powershell
python -m pip install pyinstaller
```

Install FFmpeg from a trusted source and make sure `ffmpeg.exe` is available on `PATH`.

## Build

From the repository root:

```powershell
.\build.ps1
```

The build outputs:

- `dist\LumaRecorder.exe`
- `dist\LumaRecorder_Admin.exe`

## Publisher Metadata

Windows file details are embedded at build time from:

- `packaging\version_main.txt`
- `packaging\version_admin.txt`

The publisher/developer identity is listed as **albahri.org** and the official source links are included in the executable metadata.

## Code Signing

For public distribution, sign release builds with a code-signing certificate issued to the publisher. Metadata improves transparency, but code signing is the standard Windows mechanism for verified publisher identity.
