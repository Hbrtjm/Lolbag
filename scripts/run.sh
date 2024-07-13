#!/bin/bash


# Check if running on a Windows machine
if type -t wevtutil &> /dev/null; then 
    echo "You are running a Windows machine, run the server using run.ps1 or run.bat instead"
    exit 1
fi

# Cleanup
function cleanup()
{
    kill -9 `ps aux | grep manage.py | awk '{print $2}' | head -n -1` # Ignore the last one, as this one contains the grep itself
    exit 7
}
trap cleanup EXIT

function help()
{
    printf "Usage:\n./run.sh [arguments]\n\t-f <file path>:\t\tSpecifies the path to the log file.\n\t-h <host name or IP>:\tSets the host for the application. (default host is localhost or 127.0.0.1)\n\t-p <port number>:\tSets the default port for the application host (default port is 8000)\n"
}

LOGBAG_HOST='localhost'
LOGBAG_PORT=8000

# Only for path argument for now, verbose can be added later
while getopts ":p:f:" opt; do
  case $opt in
    p)

        LOGBAG_PORT=$OPTARG
        ;;
    h)
        LOGBAG_HOST=$OPTARG
        ;;
    f)
        export LOG_FILE_PATH=$OPTARG
        ;;
    \?)
        echo "Invalid option: -$OPTARG" >&2
        help
        ;;
    :)
        echo "Option -$opt requires an argument." >&2
        help
        ;;
  esac
done

cd ..

# Check if the virutal environment exists, if not, create one
if [ ! -d env ]; then
    virtualenv env 
fi

# Start the virtual environment
if [ -d ./env/bin ]; then
    source ./env/bin/activate
else
    echo "A problem has occurred while setting up the virtual environment"
    exit 2
fi 

cd ./application

# Install python dependencies
python -m pip install -r requirements_linux.txt || { echo "Failed to install requirements"; exit 3; }

# Migrate to the database and start the application
python manage.py makemigrations || { echo "makemigrations failed"; exit 4; }
python manage.py migrate || { echo "migrate failed"; exit 5; }
python manage.py runserver ${LOGBAG_HOST}:${LOGBAG_PORT} &

# Check for changes in the logs every second
while true; do 
    python manage.py log_tracker || { echo "log_tracker failed"; exit 6; }
    sleep 1
done
