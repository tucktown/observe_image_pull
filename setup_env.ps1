# Check if virtual environment folder exists
if (-Not (Test-Path -Path "venv")) {
    # Create virtual environment
    python -m venv venv
}

# Activate virtual environment
try {
    .\venv\Scripts\Activate.ps1
} catch {
    Write-Error "Failed to activate virtual environment."
    exit 1
}

# Install required packages
try {
    .\venv\Scripts\python.exe -m pip install -r requirements.txt
} catch {
    Write-Error "Failed to install required packages."
    exit 1
}

# Run the main script
try {
    .\venv\Scripts\python.exe main.py
} catch {
    Write-Error "Failed to run main.py."
    exit 1
}

# Deactivate virtual environment
deactivate
