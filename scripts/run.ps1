# Take the keyword arguments
param (
    [string]$LogFilePath = 'server.log',
    [string]$Host_N = 'localhost',
    [int]$Port = 8000
)

$HOST_N = $Host_N 
$PORT = $Port
$Env:LOG_FILE_PATH = $LogFilePath


### Useless as we need to provide parameters first...
# Check if the script runs on the correct machine
# $osInfo = Get-CimInstance -ClassName Win32_OperatingSystem

# if ($osInfo.Caption -match "Linux") {
#     Write-Output "You are running a linux machine, run the server using run.sh instead"
# }




# Same cleanup as with bash script to free the port
function Cleanup {
    $managePyProcesses = Get-Process | Where-Object { $_.ProcessName -like "python" -and $_.Path -match "manage.py" }
    foreach ($proc in $managePyProcesses) {
        Stop-Process -Id $proc.Id -Force
    }
    exit 7
}

# Register the cleanup function to run on exit
Register-EngineEvent PowerShell.Exiting -Action { Cleanup }

function Show-Help {
    Write-Host "Usage:"
    Write-Host "./run.ps1 [-LogFilePath <file path>] [-Host <host name or IP>] [-Port <port number>]"
    Write-Host "`t-LogFilePath: Specifies the path to the log file. (default server.log should be inside of the application directory)"
    Write-Host "`t-Host_N: Sets host name for the application. (default host is localhost)."
    Write-Host "`t-Port: Sets the port number for the application host. (default port is 8000)."
}


# Script assumes it starts from /scripts directory
Set-Location ..

# Check if the virutal environment exists, if not, create one
if (-Not (Test-Path -Path "./env" -PathType Container)) {
    virtualenv env
}

# Start the virtual environment
if (Test-Path -Path "./env/Scripts") {
    . ./env/Scripts/Activate.ps1
} else {
    Write-Output "A problem has occurred while setting up the virtual environment"
    exit 2
}

Set-Location ./application

# Install python dependencies
python -m pip install -r requirements_windows.txt

# Migrate to the database and start the application
Start-Process -NoNewWindow -FilePath "python" -ArgumentList "manage.py makemigrations"
Start-Process -NoNewWindow -FilePath "python" -ArgumentList "manage.py migrate"
Start-Process -NoNewWindow -FilePath "python" -ArgumentList  "manage.py", "runserver", "$($HOST_N):$($PORT)"

# Check for changes in the logs every second
while ($true) {
    python manage.py log_tracker
    Start-Sleep -Seconds 1
}