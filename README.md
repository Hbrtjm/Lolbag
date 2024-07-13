
# Log Bag

## Short description

This application monitors a given log file, collects changes in the database, and displays them in a chart. The user can request a specific timeframe of data, select log entry levels, or search for specific parts of messages.


## Setup 

### API

#### Windows

To set up the application for Windows, please make sure you have Python 3.x installed first. To check it, you can open a command line and type:
```batch
python --version
```
or
```batch
python3 --version
```

The version of Python on your local machine should be displayed. If that's not the case, refer to the Python installation guide:
https://www.python.org/downloads/

Once that is ready, you can launch the application from the Batch Command Line or PowerShell command line. It will activate the virtual environment and install the necessary Python packages, then run the application.

Open command line and navigate to .\scripts directory:

```batch
cd %YOUR_PARENT_DIRECTORY%\logbag\scripts
```

Then run one of the scripts 

```batch
.\run.ps1
```
or
```batch
start run.bat
```

#### Linux

To set up the application for Linux, please make sure you have Python 3.x installed first. To check it, you can open a command line and type:
```sh
python --version
```
or
```sh
python3 --version
```
The version of Python on your local machine should be displayed. If that's not the case, install it with your package manager. For Debian-based systems:
```sh
sudo apt-get python pip
```
or

```sh
sudo apt-get python3 pip
```

Once that is ready, you can launch the application from the Bash Command Line. It will activate the virtual environment and install the necessary Python packages, then run the application.

Navigate to the scripts directory:

```bash
cd $YOUR_PARENT_DIRECTORY/logbag/scripts
```

Change privileges for the run.sh script:
```sh
chmod *+x run.sh 
```

Then run the script 

```sh
./run.sh
```
#### Disclaimer

Make sure that server.log exists in the application/ directory, or specify a different path using arguments -f <file path> for bash, /f <file path> for batch and -LogFilePath <file path> for powershellscipt 

### Database

#### Windows

Please follow the steps in the TimescaleDB installation guide for Windows:
https://docs.timescale.com/self-hosted/latest/install/installation-windows/

#### Linux
Please follow the steps in the TimescaleDB installation guide for Linux:
https://docs.timescale.com/self-hosted/latest/install/installation-linux/
