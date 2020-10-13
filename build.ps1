Write-Information "Starting build.ps1..."
Write-Information "Checking for venv in $(Get-Location)"
IF (-NOT (Test-Path -Path ".\venv")) {
    Write-Information "Not Found: Creating new venv!"
    python -m venv venv
}

Write-Information "Starting up venv..."
.\venv\scripts\activate

Write-Information "Upgrading pip..."
python -m pip install --upgrade pip

IF (Test-Path -Path ".\requirements.txt") {
    Write-Information "Installing packages from requirements.txt..."
    pip install -r requirements.txt
}

IF (-NOT (Test-Path "config.yaml")) {
    Write-Information "File not found: config.yaml. Now creating default config file..."
    Get-Content defaults.yaml > config.yaml
}

Write-Information "Closing down venv..."
deactivate

Write-Information "build.ps1 finished!"