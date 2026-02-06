# Launch backend and frontend from the correct nested paths
$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$appRoot = Join-Path $repoRoot "Health-Harbor-main" | Join-Path -ChildPath "vitalplunder"
$backendDir = Join-Path $appRoot "backend"
$frontendDir = Join-Path $appRoot "frontend"
$pythonExe = Join-Path $repoRoot "Health-Harbor-main" | Join-Path -ChildPath ".venv\Scripts\python.exe"
if (-not (Test-Path $pythonExe)) { $pythonExe = "python" }

Write-Host "Starting backend from $backendDir"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location `"$backendDir`"; & `"$pythonExe`" app.py"

Write-Host "Starting frontend from $frontendDir"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location `"$frontendDir`"; npm run dev -- --host"
