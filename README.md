# Luma Recorder

**Luma Recorder** is a portable Windows screen recorder built for clean tutorials, product demos, support videos, lessons, walkthroughs, and everyday screen capture. It keeps the workflow simple: open the app, choose what to record, add microphone or webcam if needed, and save the result locally.

Published by **albahri.org**.

Official source:

- <https://github.com/albahri-org>
- <https://github.com/QusaiALBahri?tab=repositories>

## Highlights

- Portable Windows app with no installer required
- Full-screen and selected-area screen recording
- Microphone recording
- System-audio recording when Windows exposes a loopback audio device
- Webcam overlay for presenter-style recordings
- Floating recording control bar
- Global hotkeys for record, stop, and pause
- Recent recordings library
- Video trimming, conversion, compression, snapshots, audio extraction, and zoom export
- Arabic and English interface
- Optional Windows EFS encryption for the recordings folder
- Clean uninstall helper included
- Local-first design with no upload, telemetry, cloud sync, or network feature

## Files

| File | Purpose |
| --- | --- |
| `LumaRecorder.exe` | Main portable recorder |
| `LumaRecorder_Admin.exe` | Launches the recorder with a visible Windows admin prompt |
| `recordings/` | Default folder for saved recordings |
| `TRUST_AND_SAFETY.txt` | Publisher, source, privacy, and safety notes |
| `Uninstall_LumaRecorder.cmd` | Removes the portable app folder after confirmation |

## Quick Start

1. Download the repository or release package.
2. Open `LumaRecorder.exe`.
3. Choose full screen or selected area.
4. Enable microphone, system audio, or webcam overlay if needed.
5. Press **Record**.
6. Saved videos appear in the `recordings/` folder.

For apps that run as administrator, use `LumaRecorder_Admin.exe`. Windows will show a normal UAC prompt before opening the recorder with elevated privileges.

## Privacy

Luma Recorder is designed as a local portable app.

- No account sign-in
- No upload feature
- No cloud sync
- No telemetry
- No background service
- No network feature

Recordings and settings stay inside the portable app folder unless you choose another output folder.

## Security Notes

The Privacy tab includes optional Windows EFS encryption for the recordings folder. EFS encrypts files for the current Windows user account. Availability depends on the Windows edition, drive format, and system policy.

Admin mode helps record elevated applications more reliably, but it does not bypass Windows secure desktops, login screens, protected/DRM video, or operating-system privacy protections.

## Interface Languages

Luma Recorder includes:

- English
- Arabic

Switch language from the **Privacy** tab.

## Hotkeys

| Shortcut | Action |
| --- | --- |
| `Ctrl + Shift + R` | Start recording |
| `Ctrl + Shift + S` | Stop recording |
| `Ctrl + Shift + P` | Pause or resume |

## System Audio

System audio recording on Windows depends on the audio driver exposing a loopback source such as:

- Stereo Mix
- What U Hear
- Loopback
- Virtual audio cable device

If no loopback device appears, microphone recording will still work normally.

## Trust

Windows file details identify the publisher as **albahri.org** and include the official source links above.

For broad public distribution, the recommended next step is code signing with a certificate issued to the publisher. Code signing is the standard Windows trust mechanism for verified publisher identity.

## License

Released under the MIT License. See [LICENSE](LICENSE).
