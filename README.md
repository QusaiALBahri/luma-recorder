<div align="center">

![Luma Recorder hero](assets/luma-hero.svg)

# Luma Recorder

### A portable Windows screen recorder for clear tutorials, demos, lessons, support videos, and local-first capture.

[![Windows](https://img.shields.io/badge/Windows-10%2B-0078D4?style=for-the-badge&logo=windows&logoColor=white)](#)
[![Portable](https://img.shields.io/badge/Portable-No_Installer-34C759?style=for-the-badge)](#download-and-run)
[![Privacy](https://img.shields.io/badge/Privacy-Local_Only-111827?style=for-the-badge)](#privacy-first)
[![Languages](https://img.shields.io/badge/UI-English_%2F_Arabic-0A84FF?style=for-the-badge)](#interface-languages)
[![License](https://img.shields.io/badge/License-MIT-F5A623?style=for-the-badge)](LICENSE)

**Published by albahri.org**

Official source only:

[github.com/albahri-org](https://github.com/albahri-org) · [github.com/QusaiALBahri](https://github.com/QusaiALBahri?tab=repositories)

</div>

---

## The Idea

Luma Recorder is for the moment when you need to show something clearly.

Not after creating an account.  
Not after setting up a cloud workspace.  
Not after learning a full editing suite.

Open it, choose the screen area, add your voice or camera if needed, record, and keep the file on your own machine.

![Luma Recorder workflow](assets/luma-flow.svg)

## What Makes It Feel Good

<table>
  <tr>
    <td width="33%">
      <h3>Fast To Start</h3>
      <p>Portable executable, no installer, no background service, and a simple first screen built around recording.</p>
    </td>
    <td width="33%">
      <h3>Made For Explaining</h3>
      <p>Capture screen, microphone, system audio, and webcam overlay for tutorials, bug reports, lessons, and demos.</p>
    </td>
    <td width="33%">
      <h3>Local By Design</h3>
      <p>No account, no upload feature, no telemetry, no cloud sync. Your recordings stay where you put them.</p>
    </td>
  </tr>
  <tr>
    <td width="33%">
      <h3>Useful After Recording</h3>
      <p>Trim, convert, compress, extract audio, save snapshots, and export zoomed focus clips.</p>
    </td>
    <td width="33%">
      <h3>Presenter Friendly</h3>
      <p>Floating controls, countdown, pause/resume, webcam overlay, and global hotkeys keep the flow smooth.</p>
    </td>
    <td width="33%">
      <h3>Ready For Real Windows Work</h3>
      <p>Use the admin launcher when you need to record normal apps that are running with elevated permissions.</p>
    </td>
  </tr>
</table>

## Download And Run

| File | Use It For |
| --- | --- |
| `LumaRecorder.exe` | Normal screen recording |
| `LumaRecorder_Admin.exe` | Recording normal elevated/admin apps after a visible Windows UAC prompt |
| `recordings/` | Default output folder |
| `Uninstall_LumaRecorder.cmd` | Clean removal of the portable folder after confirmation |

The simplest path:

```text
LumaRecorder.exe -> Record -> Stop -> recordings/
```

## First-Minute Walkthrough

1. Open `LumaRecorder.exe`.
2. Pick **Full screen** or **Select area**.
3. Enable **Microphone** if you want narration.
4. Enable **Webcam overlay** if you want a presenter view.
5. Press **Record**.
6. Press **Stop** when finished.
7. Open `recordings/`.

## Feature Map

| Record | Present | Polish | Protect |
| --- | --- | --- | --- |
| Full screen | Webcam overlay | Trim video | Local-only workflow |
| Selected area | Floating bar | Convert video | Optional EFS encryption |
| Microphone | Countdown | Compress video | Clean uninstall helper |
| System audio where available | Pause/resume | Extract audio | Trust and safety notes |
| Cursor capture | Hotkeys | Snapshot export | Admin launcher clarity |

## Hotkeys

| Shortcut | Action |
| --- | --- |
| `Ctrl + Shift + R` | Start recording |
| `Ctrl + Shift + S` | Stop recording |
| `Ctrl + Shift + P` | Pause or resume |

## Privacy First

Luma Recorder is built around a plain promise: the recording belongs to the user.

- No sign-in
- No upload feature
- No telemetry
- No cloud sync
- No background service
- No network feature

The Privacy tab includes optional Windows EFS encryption for the recordings folder. EFS encrypts files for the current Windows user account. Availability depends on the Windows edition, drive format, and system policy.

## Admin Launcher

Some Windows applications run with elevated permissions. A normal recorder may not capture those apps correctly.

Use:

```text
LumaRecorder_Admin.exe
```

Windows will show a standard UAC prompt, then open the recorder elevated.

Admin mode is not a bypass tool. It does not record Windows secure desktops, login screens, protected/DRM video, or operating-system privacy-protected surfaces.

## Interface Languages

Luma Recorder includes:

- English
- Arabic

Switch language from the **Privacy** tab.

## System Audio Notes

System audio recording depends on Windows exposing a loopback audio source. Depending on the audio driver, it may appear as:

- `Stereo Mix`
- `What U Hear`
- `Loopback`
- a virtual audio cable device

If no loopback device appears, microphone recording still works normally.

## Repository Layout

```text
.
├─ LumaRecorder.exe
├─ LumaRecorder_Admin.exe
├─ assets/
│  ├─ luma-hero.svg
│  └─ luma-flow.svg
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
