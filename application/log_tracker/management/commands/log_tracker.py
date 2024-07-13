from django.core.management.base import BaseCommand
from log_tracker.utils import read_log_file
from os import getenv

class Command(BaseCommand):
    help = 'Read log file and store logs in database'

    def handle(self, log_file_path = getenv('LOG_FILE_PATH', './server.log'), previous_log_file_hash = getenv('LOG_FILE_HASH_PATH', './log_file_hash.txt'), current_line_filepath = getenv('CURRENT_LOG_FILE_LINE_FILEPATH', './log_file_current_line.txt'), *args, **kwargs):
        # This will run on the level of manage.py, so in the application directory, if the server.log is present, this should work
        try:
            read_log_file(log_file_path, previous_log_file_hash,current_line_filepath)
        except FileNotFoundError:
            raise FileNotFoundError("server.log file not found. To fix this define environmental variable LOG_FILE_PATH or change the file path in ./application/log_tracker/management/log_tracker.py")