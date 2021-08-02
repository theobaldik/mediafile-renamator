import datetime
import traceback
import constants

def log_error():
    """Logs last occured error to log file."""
    try:
        with open(constants.LOG_PATH, "a+") as fil:
            fil.write(
                "================================================================================\n"
            )
            fil.write(str(datetime.datetime.now()))
            fil.write("\n")
            traceback.print_exc(file=fil)
    except PermissionError:
        traceback.print_exc()    
        print("\nMFR needs permissions to write here. " \
            "Run MFR as administrator or move the MFR folder to another directory for proper functionality.\n")            
        input('Press Enter to continue...')

def get_log():
    """
    Returns log file contents.
    :returns: contents of log file or None if file doesn't exist"""
    try:
        with open(constants.LOG_PATH, 'r') as fil:
            return fil.read()
    except:
        return None

def clear_log():
    """Removes content from log file or creates empty log file if doesn't exists."""
    try:
        with open(constants.LOG_PATH, 'w') as fil:
            fil.write("")
    except:
        return

if __name__ == "__main__":
    pass
