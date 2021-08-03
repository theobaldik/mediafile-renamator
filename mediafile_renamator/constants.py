import os
import json
import logger

VERSION = '0.0.2'

MFR_ROOT = os.path.join(os.getenv('APPDATA'), 'Fat Camel Studio', 'Mediafile Renamator')
try:
    os.makedirs(MFR_ROOT)
except FileExistsError:
    pass

LOG_PATH = os.path.join(MFR_ROOT, 'error.log')
CONFIG_PATH = os.path.join(MFR_ROOT, 'config.json')

video_ext = ['.mp4', '.m4v', '.mkv', '.avi', '.mov']
audio_ext = ['.mp3', '.ogg', '.flac']
subtitles_ext = ['.srt', '.sub']
formats = ['plex']

DEFAULT_FORMATTING = 'plex'
DEFAULT_SUBTITLES_LANG = 'cs'

TMDB_API_KEY = ''

def create_default_config():
    """Creates configuration file using default setting."""
    config_dict = {
        'default-formatting': DEFAULT_FORMATTING,
        'default-subtitles-lang': DEFAULT_SUBTITLES_LANG,
        'tmdb-api-key' : TMDB_API_KEY
    }
    try:
        with open(CONFIG_PATH, 'w') as fil:
            json.dump(config_dict, fil)
    except:
        logger.log_error()

def load_constants():
    """Loads settings from configuration file."""
    global DEFAULT_FORMATTING, DEFAULT_SUBTITLES_LANG, TMDB_API_KEY
    try:
        with open(CONFIG_PATH, 'r') as fil:
            json_fil = json.load(fil)
            DEFAULT_FORMATTING = json_fil['default-formatting']
            DEFAULT_SUBTITLES_LANG = json_fil['default-subtitles-lang']
            TMDB_API_KEY = json_fil['tmdb-api-key']
    except FileNotFoundError:
        create_default_config()
    except:
        logger.log_error()

def reset_config():
    """Recover default settings."""
    try:
        os.remove(CONFIG_PATH)
        load_constants()
    except:
        load_constants()

load_constants()