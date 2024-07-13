import re
import hashlib
from glob import glob
from datetime import datetime
from .models import Log
from os import getenv, environ

DEBUG = False

def parse_log_line(line):
    """
    Matches the log pattern in the log file

    Args:
        line (str): a line from log file

    Returns:
        - str: time when the log was registered
        - str: type of the registered log
        - str: description
        
    """
    LOG_PATTERN = r'^(INFO|DEBUG|WARNING|ERROR|CRITICAL) (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) (.*)$'
    match = re.match(LOG_PATTERN, line)
    if match:
        time = datetime.strptime(match.group(2), '%Y-%m-%d %H:%M:%S,%f')
        log_type = match.group(1)
        description = match.group(3)
        return time, log_type, description
    return None

def hash_file(file_path, algorithm='sha256'):
    """
    Hashes a file using the specified algorithm and returns the hex digest.

    Parameters:
    - file_path (str): The path to the file to be hashed.
    - algorithm (str): The name of the hash algorithm to use (default is 'sha256').

    Returns:
    - str: The hexadecimal hash digest of the file.
    """
    # Create a hash object
    hash_obj = hashlib.new(algorithm)
    
    with open(file_path, 'rb') as f:
        chunk = f.read(8192)
        while chunk != b'': # It is guaranteed to stop, as the end of should always be reached
            hash_obj.update(chunk)
            chunk = f.read(8192)
    
    # Return the hexadecimal digest of the hash
    return hash_obj.hexdigest()

def read_log_file(log_file_path, previous_log_file_hash_filepath, current_line_filepath):
    """
    Reads a log file if there are any changes detected and commits them into the database.

    Args:
        log_file_path (str):                   Path to the log file, should be defined as an environmental variable in Docker container.
        previous_log_file_hash_filepath (str): Path to last hash of the log file, can be defined as an environmental variable in Docker container. 
        current_line_filepath (str):           Path to the file containing index of the last line read from server.log. 
                                               Can be defined as an environmental variable. This file solution in this case can be replaced with an environmental variable containing the number
    """
    # Get the previous hash if it exists
    previous_log_file_hash = None
    if glob(previous_log_file_hash_filepath):
        with open(previous_log_file_hash_filepath, 'r') as file_with_hash:
            previous_log_file_hash = file_with_hash.read().strip()
    
    # Get the current line tracker position
    line_tracker = 0
    if glob(current_line_filepath):
        with open(current_line_filepath, 'r') as current_line_file:
            line_tracker = current_line_file.read().strip()
    line_tracker = int(line_tracker) if line_tracker else 0

    # Calculate the new file hash
    new_file_hash = hash_file(log_file_path)
    
    # Check if the log file was modified
    log_file_modified = previous_log_file_hash != new_file_hash
    # Scan the file only if it was modified
    if log_file_modified:
        # Read the file and update it in the database
        log_objects = []
        with open(log_file_path, 'r') as log_file:
            # Skip to the current line
            for i in range(line_tracker):
                line = log_file.readline()
                if not line:
                    # If the log file was somehow modified, for instance some lines would get deleted,
                    # this would start from the last line that was left in the file
                    line_tracker = i
                    break
            
            for line in log_file:
                line_tracker += 1
                log_entry = parse_log_line(line)
                if DEBUG and log_entry is not None:
                    time, level, message = log_entry
                    log_objects.append(Log(log_date_time=time, level=level, message=message))
                    Log.objects.create(log_date_time=time, level=level, message=message)
                if not DEBUG and log_entry is not None:
                    time, level, message = log_entry
                    log_objects.append(Log(log_date_time=time, level=level, message=message))
        if not DEBUG and len(log_objects) > 0:
            # for elem in log_objects:
            #     print(elem.log_date_time)
            Log.objects.bulk_create(log_objects,batch_size=len(log_objects))
        
    # Update the line tracker
    if log_file_modified or line_tracker:
        with open(current_line_filepath, 'w') as current_line_file:
            current_line_file.write(str(line_tracker))
        
    # Write new hash to the hash file if server.log was modified or hash file does not exist
    if log_file_modified or previous_log_file_hash is None:
        with open(previous_log_file_hash_filepath, 'w') as file_with_hash:
            file_with_hash.write(new_file_hash)
