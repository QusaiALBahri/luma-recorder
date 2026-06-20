# Luma Recorder

**A portable Windows screen recorder for people who want to press record, explain clearly, and keep the file.**

Luma Recorder is made for tutorials, lessons, product demos, walkthroughs, support videos, bug reports, and quick knowledge sharing. It stays local, feels lightweight, and gives you the useful recording tools without turning the app into a studio cockpit.

Published by **albahri.org**.

Official source only:

- <https://github.com/albahri-org>
- <https://github.com/QusaiALBahri?tab=repositories>

---

## Why Luma Recorder Exists

Most screen recorders fall into one of two traps: too simple to be useful, or so packed with panels that recording feels like work before the work begins.

Luma Recorder tries to sit in the better middle:

- open it
- choose what matters
- record your screen, voice, and camera
- polish the result when needed
- keep everything on your own machine

No account. No upload step. No cloud dashboard. Just a clean recorder that respects the moment.

## What You Can Record

| Need | Luma Recorder Gives You |
| --- | --- |
| A full tutorial | Screen + microphone + webcam overlay |
| A quick bug report | Screen capture with fast local saving |
| A polished walkthrough | Floating controls, pause/resume, and simple edits |
| A private local workflow | Portable files, local recordings, optional folder encryption |
| Admin-level app demos | Separate admin launcher with a visible Windows UAC prompt |
| Arabic or English usage | Built-in language switch |

## Feature Tour

### Record Clearly

- Full-screen recording
- Selected-area recording
- Microphone capture
- System audio capture when Windows exposes a loopback device
- Webcam overlay for presenter-style videos
- Cursor capture
- Countdown before recording
- Auto-stop timer
- Pause and resume
- Floating recording control bar

### Move Fast

- Portable `.exe`
- No installer required
- Recent recordings library
- Open output folder instantly
- Play the last recording
- Global hotkeys:

| Shortcut | Action |
| --- | --- |
| `Ctrl + Shift + R` | Start recording |
| `Ctrl + Shift + S` | Stop recording |
| `Ctrl + Shift + P` | Pause or resume |

### Polish the Result

- Trim video
- Convert video
- Compress video
- Export a snapshot
- Extract audio
- Zoom/focus export for highlighting a specific area of the video

### Keep It Local

- No account sign-in
- No upload feature
- No cloud sync
- No telemetry
- No background service
- No network feature

Recordings and settings stay inside the portable app folder unless you choose a different output folder.

## Download And Run

From this repository, use:

- `LumaRecorder.exe` for normal recording
- `LumaRecorder_Admin.exe` when you need to record apps that are already running as administrator

The default save location is:

```text
recordings/
```

## The First Minute

1. Open `LumaRecorder.exe`.
2. Pick **Full screen** or **Select area**.
3. Turn on **Microphone** if you want narration.
4. Turn on **Webcam overlay** if you want your camera in the recording.
5. Press **Record**.
6. Stop when finished.
7. Find the video in `recordings/`.

That is the whole loop.

## Admin Launcher

Some Windows apps run with elevated permissions. A normal recorder may not capture those apps correctly.

For that case, use:

```text
LumaRecorder_Admin.exe
```

Windows will show a standard UAC prompt. After approval, the recorder opens with elevated privileges.

Admin mode is not a bypass tool. It does not record Windows secure desktops, login screens, protected/DRM video, or operating-system privacy-protected surfaces.

## Privacy And Safety

Luma Recorder is designed as a local-first portable app.

The Privacy tab includes optional Windows EFS encryption for the recordings folder. EFS encrypts files for the current Windows user account. Availability depends on the Windows edition, drive format, and system policy.

For transparency, the portable package also includes:

- `TRUST_AND_SAFETY.txt`
- `SECURITY.md`
- `Uninstall_LumaRecorder.cmd`

## System Audio Notes

System audio recording depends on Windows exposing a loopback audio source. Depending on your audio driver, it may appear as:

- `Stereo Mix`
- `What U Hear`
- `Loopback`
- a virtual audio cable device

If no loopback device appears, microphone recording still works normally.

## Project Layout

```text
.
├─ LumaRecorder.exe
├─ LumaRecorder_Admin.exe
├─ src/
│  ├─ luma_recorder.py
│  └─ admin_launcher.py
├─ packaging/
│  ├─ version_main.txt
│  └─ version_admin.txt
├─ recordings/
├─ build.ps1
├─ BUILDING.md
├─ SECURITY.md
├─ TRUST_AND_SAFETY.txt
├─ Uninstall_LumaRecorder.cmd
└─ LICENSE
```

## Build From Source

Requirements:

- Windows 10 or later
- Python
- PyInstaller
- FFmpeg available on `PATH`

Build:

```powershell
.\build.ps1
```

More details are in [BUILDING.md](BUILDING.md).

## Trust

Windows file details identify the publisher as **albahri.org** and include the official source links.

For public distribution at scale, sign release builds with a code-signing certificate issued to the publisher. Metadata helps people understand what they are running; code signing is the Windows standard for verified publisher identity.

## License

Released under the MIT License. See [LICENSE](LICENSE).
