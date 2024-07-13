@echo off 

:: Check if the current machine is running Linux
FOR /f "tokens=2 delims==" %%i IN ('wmic os get Caption /value 2^>nul') DO set "osName=%%i"

IF /i "%osName%"=="Linux" (
    echo You are running a linux machine, run the server using run.sh instead
    exit /b
)

setlocal enabledelayedexpansion


set LOGBAG_HOST="localhost"
set LOGBAG_PORT=8000

:parse_args
if "%~1"=="" goto args_parsed
set "arg=%~1"
set "value=%~2"
if "%arg%"=="/p" (
    set "LOGBAG_PORT=%value%"
) else if "%arg%"=="/h" (
    set "LOGBAG_HOST=%value%"
) else if "%arg%"=="/f" (
    set "LOG_FILE_PATH=%value%"
) else (
    echo Invalid argument: %arg%
    goto :help
)
shift
shift 
goto parse_args

:args_parsed

:: To make sure the CD .. command will go to the main directory
IF EXIST scripts (
    CD scripts
)

CD ..

:: Check if the virutal environment exists, if not, create one
IF NOT EXIST env (
    virtualenv env
)

:: Start the virtual environment
IF EXIST env\Scripts (
    call env\Scripts\activate
) ELSE (
    ECHO "A problem has occurred while setting up the virtual environment"
    exit /b 2
)

CD application

:: Install python dependencies
START "" /b python -m pip install -r requirements_windows.txt

:: Migrate to the database and start the application
START "" /b python .\manage.py makemigrations
START "" /b python .\manage.py migrate
START "" /b python .\manage.py runserver %LOGBAG_HOST%:%LOGBAG_PORT%

:: Check for changes in the logs every second
:log_tracker_loop
python .\manage.py log_tracker
timeout /t 100
GOTO log_tracker_loop

:help
echo Usage:
echo ./run.bat -f ^<file path^> [-h ^<host name or IP^>] [-p ^<port number^>]
echo     -f: Specifies the path to the log file.
echo     -h: Sets the default host for the application (default host is localhost).
echo     -p: Sets the default port for the application host (default port is 8000).
pause
exit /b 1