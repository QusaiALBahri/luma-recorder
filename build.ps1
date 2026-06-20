$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$DistDir = Join-Path $ProjectRoot "dist"
$BuildDir = Join-Path $ProjectRoot "build"
$MainSource = Join-Path $ProjectRoot "src\luma_recorder.py"
$AdminSource = Join-Path $ProjectRoot "src\admin_launcher.py"
$MainVersion = Join-Path $ProjectRoot "packaging\version_main.txt"
$AdminVersion = Join-Path $ProjectRoot "packaging\version_admin.txt"
$Ffmpeg = (Get-Command ffmpeg.exe -ErrorAction Stop).Source

New-Item -ItemType Directory -Force -Path $DistDir | Out-Null

python -m PyInstaller `
  --noconfirm `
  --clean `
  --windowed `
  --onefile `
  --name "LumaRecorder" `
  --distpath "$DistDir" `
  --workpath (Join-Path $BuildDir "main") `
  --specpath "$ProjectRoot" `
  --version-file "$MainVersion" `
  --add-binary "$Ffmpeg;." `
  "$MainSource"

python -m PyInstaller `
  --noconfirm `
  --clean `
  --windowed `
  --onefile `
  --uac-admin `
  --name "LumaRecorder_Admin" `
  --distpath "$DistDir" `
  --workpath (Join-Path $BuildDir "admin") `
  --specpath "$ProjectRoot" `
  --version-file "$AdminVersion" `
  "$AdminSource"

Write-Host "Build complete:"
Write-Host (Join-Path $DistDir "LumaRecorder.exe")
Write-Host (Join-Path $DistDir "LumaRecorder_Admin.exe")
